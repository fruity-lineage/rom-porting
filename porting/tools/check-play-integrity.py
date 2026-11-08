#!/usr/bin/env python3
"""Collect read-only configuration and selected fields from decoded verdict JSON."""

import argparse
import json
from pathlib import Path
import re
import struct
import subprocess
import sys


LABELS = ("MEETS_BASIC_INTEGRITY", "MEETS_DEVICE_INTEGRITY", "MEETS_STRONG_INTEGRITY")
PACKAGES = ("com.google.android.gms", "com.android.vending", "com.google.android.gsf")
PROPERTIES = (
    "ro.product.device", "ro.lineage.version", "ro.build.version.sdk",
    "ro.lineage.duckrkp.trusty_import", "remote_provisioning.hostname",
    "ro.boot.verifiedbootstate", "ro.boot.flash.locked", "ro.boot.vbmeta.device_state",
    "ro.boot.slot_suffix", "ro.build.version.security_patch",
    "ro.vendor.build.security_patch", "ro.bootimage.build.version.security_patch",
)
SETTINGS = (
    ("secure", "spoof_activated"), ("system", "spoof_pif_enabled"),
    ("system", "spoof_trickystore_enabled"), ("secure", "spoof_duck_rkp_enabled"),
)
FLAGS = ("spoofBuild", "spoofProps", "spoofProvider", "spoofSignature")


def scalar(value):
    return value if isinstance(value, (str, int, bool)) else None


def verdict_summary(data):
    if not isinstance(data, dict):
        raise ValueError("Provide decoded verdict JSON, not a signed token")
    data = data.get("tokenPayloadExternal", data)
    if not isinstance(data, dict):
        raise ValueError("Invalid decoded verdict payload")
    device = data.get("deviceIntegrity")
    if not isinstance(device, dict):
        error = data.get("error", {})
        error = error if isinstance(error, dict) else {}
        return {
            "verdict_available": False,
            "labels": {label: None for label in LABELS},
            "error_code": scalar(error.get("code", data.get("errorCode"))),
            "error_status": scalar(error.get("status")),
        }
    labels = device.get("deviceRecognitionVerdict", [])
    if not isinstance(labels, list) or any(not isinstance(x, str) for x in labels):
        raise ValueError("Malformed deviceRecognitionVerdict")
    account = data.get("accountDetails", {})
    app = data.get("appIntegrity", {})
    attributes = device.get("deviceAttributes", {})
    return {
        "verdict_available": True,
        "labels": {label: label in labels for label in LABELS},
        "app_licensing": scalar(account.get("appLicensingVerdict")) if isinstance(account, dict) else None,
        "app_recognition": scalar(app.get("appRecognitionVerdict")) if isinstance(app, dict) else None,
        "server_sdk_version": scalar(attributes.get("sdkVersion")) if isinstance(attributes, dict) else None,
        "authenticity": "Decoded input supplied by operator; token authenticity not verified here",
        "label_semantics": "Flags show presence in the response; optional labels also depend on requester settings and licensing",
    }


def pif_summary(raw):
    if raw.strip() in ("", "null"):
        return {"present": False}
    if raw.lstrip().startswith("{"):
        fields = json.loads(raw)
        if not isinstance(fields, dict):
            raise ValueError("PIF config is not an object")
    else:
        fields = {}
        for line in raw.splitlines():
            line = line.split("#", 1)[0].strip()
            if "=" in line:
                key, value = line.split("=", 1)
                if value.strip():
                    fields[key.strip()] = value.strip()
    return {
        "present": True,
        "fingerprint_present": bool(fields.get("FINGERPRINT")),
        "flags": {name: (str(fields[name]).lower() in ("1", "true"))
                  if name in fields else None for name in FLAGS},
    }


def boot_summary(header):
    if len(header) < 44 or header[:8] != b"ANDROID!":
        raise ValueError("Missing Android boot header")
    version = struct.unpack_from("<I", header, 40)[0]
    offset = 16 if version >= 3 else 44
    if len(header) < offset + 4:
        raise ValueError("Truncated boot header")
    word = struct.unpack_from("<I", header, offset)[0]
    patch = word & 0x7ff
    return {"header_version": version, "os_version_word": word,
            "legacy_patch": f"{2000 + (patch >> 4):04d}-{patch & 15:02d}" if patch else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serial", help="Explicit device; omitted when only one device is attached")
    parser.add_argument("--server-port", type=int, default=5037)
    parser.add_argument("--checker", help="Installed checker package name")
    parser.add_argument("--verdict-json", type=Path, help="Local file containing an already decoded response")
    parser.add_argument("--offline", action="store_true", help="Inspect only the supplied decoded JSON")
    parser.add_argument("--boot-headers", action="store_true", help="Read 64 bytes from active boot/init_boot; requires root")
    args = parser.parse_args()
    if not 1 <= args.server_port <= 65535:
        parser.error("Invalid ADB server port")
    if args.checker and not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)+", args.checker):
        parser.error("Invalid checker package name")
    output = {"read_only": True, "verdict": None}
    if args.verdict_json:
        output["verdict"] = verdict_summary(json.loads(args.verdict_json.read_text()))
    if args.offline:
        if not args.verdict_json:
            parser.error("--offline requires --verdict-json")
        print(json.dumps(output, indent=2))
        return
    adb = ["adb", "-H", "127.0.0.1", "-P", str(args.server_port)]
    if args.serial:
        adb += ["-s", args.serial]

    def run(*command, binary=False):
        try:
            result = subprocess.run(adb + list(command), capture_output=True, timeout=15)
        except subprocess.TimeoutExpired:
            raise RuntimeError("ADB request timed out; check the selected transport/server locally") from None
        if result.returncode:
            raise RuntimeError("ADB command failed; check the selected transport/server locally")
        return result.stdout if binary else result.stdout.decode(errors="replace").strip()

    run("get-state")
    output["properties"] = {name: run("shell", "getprop", name) for name in PROPERTIES}
    output["settings"] = {key: run("shell", "settings", "--user", "0", "get", namespace, key)
                          for namespace, key in SETTINGS}
    output["pif_config"] = pif_summary(run("shell", "settings", "--user", "0", "get", "secure", "spoof_pif_config"))
    output["selinux"] = run("shell", "getenforce")
    output["packages"] = {}
    for package in dict.fromkeys(PACKAGES + ((args.checker,) if args.checker else ())):
        dump = run("shell", "dumpsys", "package", package)
        selected = {}
        for key in ("versionCode", "versionName", "installerPackageName", "initiatingPackageName"):
            match = re.search(r"\b" + key + r"=([^\s]+)", dump)
            selected[key] = match.group(1) if match else None
        selected["installed"] = bool(re.search(r"Package \[" + re.escape(package) + r"\]", dump))
        output["packages"][package] = selected
    output["product_properties_sha256"] = run("shell", "sha256sum", "/product/etc/build.prop").split()[0]
    if args.boot_headers:
        slot = output["properties"]["ro.boot.slot_suffix"]
        if slot not in ("_a", "_b"):
            raise ValueError("Unexpected boot slot; refusing block-device read")
        output["boot_headers"] = {
            name: boot_summary(run("exec-out", "head", "-c", "64", "/dev/block/by-name/" + name + slot, binary=True))
            for name in ("boot", "init_boot")
        }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        print("Collection incomplete: " + str(error), file=sys.stderr)
        sys.exit(1)
