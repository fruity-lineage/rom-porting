import importlib.util
from pathlib import Path
import struct
import subprocess
import unittest
from unittest import mock


spec = importlib.util.spec_from_file_location("integrity_check", Path(__file__).with_name("check-play-integrity.py"))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class IntegrityEvidenceTests(unittest.TestCase):
    def test_adb_timeout_does_not_expose_device_serial(self):
        command = ["adb", "-s", "private-device-serial", "get-state"]
        with mock.patch.object(checker.sys, "argv", ["check", "--serial", "private-device-serial"]), \
                mock.patch.object(checker.subprocess, "run", side_effect=subprocess.TimeoutExpired(command, 15)):
            with self.assertRaises(RuntimeError) as caught:
                checker.main()
        self.assertNotIn("private-device-serial", str(caught.exception))

    def test_api_error_is_not_a_failed_verdict(self):
        result = checker.verdict_summary({"error": {"code": 400, "status": "INVALID_ARGUMENT", "message": "private"}})
        self.assertFalse(result["verdict_available"])
        self.assertTrue(all(value is None for value in result["labels"].values()))
        self.assertNotIn("private", str(result))

    def test_decoded_response_filters_request_and_private_fields(self):
        result = checker.verdict_summary({"tokenPayloadExternal": {
            "requestDetails": {"nonce": "private_nonce"},
            "accountDetails": {"appLicensingVerdict": "UNLICENSED"},
            "deviceIntegrity": {"deviceRecognitionVerdict": ["MEETS_DEVICE_INTEGRITY"]},
            "privateKey": "private_key",
        }})
        self.assertTrue(result["labels"]["MEETS_DEVICE_INTEGRITY"])
        self.assertFalse(result["labels"]["MEETS_STRONG_INTEGRITY"])
        self.assertEqual(result["app_licensing"], "UNLICENSED")
        self.assertNotIn("private_", str(result))

    def test_empty_device_verdict_is_a_real_response(self):
        result = checker.verdict_summary({"deviceIntegrity": {}})
        self.assertTrue(result["verdict_available"])
        self.assertTrue(all(value is False for value in result["labels"].values()))

    def test_sdk_attributes_are_nested_under_device_integrity(self):
        result = checker.verdict_summary({"deviceIntegrity": {
            "deviceRecognitionVerdict": ["MEETS_BASIC_INTEGRITY"],
            "deviceAttributes": {"sdkVersion": 37},
        }})
        self.assertEqual(result["server_sdk_version"], 37)

    def test_malformed_labels_rejected(self):
        with self.assertRaises(ValueError):
            checker.verdict_summary({"deviceIntegrity": {"deviceRecognitionVerdict": "MEETS_STRONG_INTEGRITY"}})

    def test_pif_fields_are_selected_and_missing_flags_not_invented(self):
        for raw in ('{"FINGERPRINT":"public","spoofProvider":true,"privateKey":"private"}',
                    'FINGERPRINT=public\nspoofProvider=1 # comment\nprivateKey=private'):
            result = checker.pif_summary(raw)
            self.assertTrue(result["fingerprint_present"])
            self.assertTrue(result["flags"]["spoofProvider"])
            self.assertIsNone(result["flags"]["spoofSignature"])
            self.assertNotIn("private", str(result))

    def test_zero_patch_is_absent_not_an_invalid_date(self):
        header = bytearray(64)
        header[:8] = b"ANDROID!"
        struct.pack_into("<I", header, 40, 4)
        self.assertIsNone(checker.boot_summary(header)["legacy_patch"])
        struct.pack_into("<I", header, 16, (17 << 25) | ((2026 - 2000) << 4) | 10)
        self.assertEqual(checker.boot_summary(header)["legacy_patch"], "2026-10")

    def test_truncated_boot_header_rejected(self):
        with self.assertRaises(ValueError):
            checker.boot_summary(b"ANDROID!")


if __name__ == "__main__":
    unittest.main()
