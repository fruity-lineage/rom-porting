# Tokay live Play Integrity and RKP investigation

Verified directly over the forwarded ADB server on 2026-11-08 UTC. No Play
Integrity verdict has been obtained in this session. The checker was identified
and opened, but the device remained locked with its display off. Unlock and a
fresh checker result are pending.

## Installed configuration

- Root ADB access succeeds; transport is explicitly selected as Tokay. The local
  ADB server is available through `127.0.0.1:50096`. This is ADB forwarding, not
  fastboot forwarding.
- Active slot is `_a`; Android SDK is 37; Lineage version is
  `24.0-20261108-UNOFFICIAL-tokay`. SELinux is Enforcing. Hardware boot state is
  orange and the bootloader is unlocked.
- Mounted `/product/etc/build.prop` contains both
  `ro.lineage.duckrkp.trusty_import=true` and the production RKP hostname. Its
  SHA-256 is `f8229a2e54274f52f60832cef304ee6551b4ad20298b8a5e2c1ef9963f87b859`,
  equal to the recorded build/target-files output. The missing installed property
  discrepancy is resolved for this installation; a reboot check is still pending.
  No duplicate property should be added to the wrapper.
- `spoof_activated=1` and `spoof_duck_rkp_enabled=1`. The PIF and TrickyStore
  master settings are unset, which the current sources interpret as enabled.
  The PIF profile is present, has a fingerprint and enables `spoofProps`.
  `spoofProvider` is absent; current framework code defaults it to false.
  Effective process behavior has not been measured during a checker request.
- The target list contains GMS and Play Store. Duck's read-only Binder state
  reports available/enabled/active, a keybox, stage ready, revision 3, no error
  and no active operation. This does not independently repeat signing/injection.
- GMS 26.11.36, Play Store 53.9.23-34 and GSF 17 are installed. The checker is
  `gr.nikolasspyr.integritycheck`, version 2.2 (22), installed and initiated by
  Play Store. Installer provenance alone does not establish server licensing.

## Image provenance

| Image | Installed evidence |
| --- | --- |
| boot_a | SHA-256 `aa821d73612b49dde79f34dd4b0a42d2bbd6c9f70c6f5034267e9bca81eb2bd7`; exactly matches the built boot image |
| init_boot_a | SHA-256 `272381db6297b597b092adcb7ceed1770eb7859b04f3fa3234b74c147b12e66c`; exactly matches target-files IMAGES/init_boot.img |
| vbmeta_a | SHA-256 `09729d5d0d93ab5717b743d56e1901fa03582a28da69d8cfbccf3adef2c07fb1`; equals target-files vbmeta plus zero partition padding |
| abl_a | First 2,224,128 bytes match the checked-in abl.img, SHA-256 `19accd9e6fd423e79bac7741e6710cf3303b7a388d85dd31094fa00269e6c70a`; the rest of its partition was not compared |

The un-packaged init_boot output has a different hash. Both images contain the
same 36 CPIO entries and file data; compared differences are four device-node
permission modes (0644 versus 0755), plus archive/compression/signing metadata.
The installed image matches the packaged image. This is not evidence of a root
patch or a mismatched installed init_boot.

Boot's header v4 OS/version word is zero. Init_boot's is 570425771, encoding
legacy patch 2026-11. Both boot and installed init_boot have AVB patch properties
`2026-10-05`. The packaged image set passes recursive avbtool signature,
hash and hashtree verification. That check reads local artifacts, not every
installed partition.

[AOSP's boot header specification](https://source.android.com/docs/core/architecture/bootloader/boot-image-header)
requires GKI v4 boot's `os_version` field to be zero and expects the bootloader
to obtain version information from AVB properties. A zero header is therefore
not, by itself, a packaging defect. Do not fill it with a guessed date.

## Direct RKPD and CSR evidence

`cmd remote_provisioning certify default` fails with HTTP 400. The server log
explicitly rejects `boot_patch_level=20000000` as an invalid YYYYMMDD/YYYYMM date.
A fresh `cmd remote_provisioning csr default` also contains:

```json
{
  "vb_state": "orange",
  "os_version": "170000",
  "security_level": "tee",
  "boot_patch_level": 20000000,
  "bootloader_state": "unlocked",
  "system_patch_level": 202611,
  "vendor_patch_level": 20261005
}
```

Only selected decoded fields are retained. CSR signatures were not independently
verified in this check; raw CSR/DICE material and request identifiers are not
published. The error has now been independently reproduced, rather than only
reported by the user.

## AVB verification lead and prepared experiment

Installed and packaged top-level vbmeta have **flags 3**, disabling both
hashtrees and verification. Zumapro's existing BoardConfig selects these flags
when `WITH_AVB` is not `true`. No new source toggle is needed.

In libavb, the VERIFICATION_DISABLED bit branches out before descriptor
processing, skipping chained boot metadata, and also suppresses the usual
AVB kernel parameters. This agrees with the absent live vbmeta-size/hash/verity
properties. Boot's valid patch property is in its chained image, not the root
vbmeta. This is a concrete explanation to test for the missing boot patch;
the exact proprietary bootloader fallback has not been disassembled/proven.

Prepared local artifacts are in
`out/porting-tests/tokay-avb-metadata/` in the Android workspace:

- `vbmeta-original-a.img`: full active-slot backup, hash recorded above.
- `vbmeta-flags1.img`: signed candidate clearing only VERIFICATION_DISABLED,
  retaining HASHTREE_DISABLED; SHA-256
  `54e76b6dbda4c6aaba87e564505083dbc27413ae83491d57b04bba5d1c506502`.
- `verification.json`: the original/candidate signatures and root descriptors
  verify; the signing public key, rollback index/location and all 15 descriptors
  match. avbtool reordered existing descriptors without changing their content.

This preparation signs existing metadata and does not compile Android or a kernel.
**Nothing has been flashed or rebooted.** The candidate is an experiment, not a
validated fix. Applying it requires the user's approval and local USB fastboot
recovery access: the ADB tunnel cannot restore a phone that fails to boot. Do not
relock, wipe data, change slots or alter firmware as part of this experiment.
Before any authorized write, recheck device identity, active slot, original hash
and backup availability. After reboot, obtain the new CSR date, RKPD result,
ordinary Keystore behavior and real checker JSON. Restore the original on failure.

For a future complete build, the existing `WITH_AVB=true` option selects normal
AVB rather than flags 3. Its boot/runtime effects still need device validation.
Enabling metadata verification alone does not establish BASIC/DEVICE/STRONG.
Google's [verdict requirements](https://developer.android.com/google/play/integrity/verdicts)
require actual locked/manufacturer-certified boot for DEVICE on Android 13+;
STRONG adds update requirements. Optional labels also depend on requester
configuration/licensing. Rewritten certificate fields do not prove acceptance.

## Source pins and diagnostic validation

| Project | Inspected revision and relevant path |
| --- | --- |
| device/google/zumapro | c03df81e8fed84aeb4f2d26e9cef2ea5762d7c3f; BoardConfig-common.mk WITH_AVB gate |
| external/avb | 01ecfc9c3df4fbe3e785185742f3313252e70a18; libavb/avb_slot_verify.c verification-disabled branches |
| system/keymint | cfeefc94bf8c4f19d19dca193d376a1fc05e8e3e; ta/src/rkp.rs boot_info CSR field and ta/src/lib.rs early-boot/root-of-trust gates |

Android userspace cannot repair an already-established trusted boot-info value
by setting a property or editing signed CSR bytes. KeyMint's source rejects
changed/repeated boot info and updates after early boot.

The read-only collector is [check-play-integrity.py](../tools/check-play-integrity.py).
Nine unit tests pass, including missing/error versus empty verdict, sensitive
field filtering, optional fields, nested SDK attributes and zero/truncated boot
headers. It does not request or authenticate Play Integrity tokens. Use:

```sh
python3 porting/tools/check-play-integrity.py --server-port 50096 --serial DEVICE_SERIAL \
  --checker gr.nikolasspyr.integritycheck --boot-headers
python3 porting/tools/check-play-integrity.py --offline --verdict-json decoded-response.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s porting/tools -p test_check_play_integrity.py -v
```

The installed checker exposes a JSON response menu. Its APK inspection confirms
that missing labels display crosses, including when deviceIntegrity is absent;
the actual JSON/API error is needed to interpret its icons. Its APK and screenshots
remain temporary and are not included in the handoff. No Android source, manifest,
firmware or device configuration was changed during this investigation.
