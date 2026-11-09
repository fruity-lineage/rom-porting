# Tokay live Play Integrity and RKP investigation

Verified directly over the forwarded ADB server on 2026-11-08 UTC. The authorized
AVB metadata test resolves RKPD's invalid boot patch date and validates remote
provisioning, hardware imported-key issuance and ordinary TEE signing. A fresh
checker request after provisioning completes still shows BASIC/DEVICE/STRONG Fail.
This is a working provisioning path with unresolved consumer acceptance.

## Installed configuration and actual verdict

- Tokay, active slot `_a`, SDK 37, Lineage `24.0-20261108-UNOFFICIAL-tokay`.
  SELinux is Enforcing. Actual hardware state remains orange/unlocked.
- Forwarded root ADB uses `127.0.0.1:50096`; this does not provide fastboot recovery.
- Mounted `/product/etc/build.prop` SHA-256 is
  `f8229a2e54274f52f60832cef304ee6551b4ad20298b8a5e2c1ef9963f87b859`,
  matching build/target-files output. The reboot confirms
  `ro.lineage.duckrkp.trusty_import=true` persists and the production RKP hostname
  remains selected. No wrapper property edit is required.
- Duck is available/enabled/active, ready, not busy, with no error and a keybox.
  Fresh provisioning after reboot succeeds; revision is 1 since reboot.
- GMS 26.11.36, Play Store 53.9.23-34 and GSF 17 are installed. The checker is
  `gr.nikolasspyr.integritycheck` 2.2 (22), installed through Play Store.
- Fresh baseline, DroidGuard-restart and post-AVB requests all display three Fail
  icons. The final sequential request runs after completed Duck provisioning;
  its response timestamp changed, confirming a new response rather than a stale dialog.
- `deviceIntegrity` exists, but `deviceRecognitionVerdict` is omitted. App recognition
  and licensing are UNEVALUATED; SDK attributes are absent. Raw requests, nonces and
  timestamps are not retained. Checker-backend token authenticity was not verified.
- DroidGuard logs show configuration/keybox load. The observed load does not establish
  its returned attestation chain or Google acceptance. The user's earlier targeted-app
  issuer proof remains reported evidence; no new targeted-app chain was collected here.

## Original image provenance

| Image | Evidence before the authorized experiment |
| --- | --- |
| boot_a | SHA-256 `aa821d73612b49dde79f34dd4b0a42d2bbd6c9f70c6f5034267e9bca81eb2bd7`; exactly matches built boot |
| init_boot_a | SHA-256 `272381db6297b597b092adcb7ceed1770eb7859b04f3fa3234b74c147b12e66c`; exactly matches packaged target-files image |
| original vbmeta_a | SHA-256 `09729d5d0d93ab5717b743d56e1901fa03582a28da69d8cfbccf3adef2c07fb1`; target-files vbmeta plus zero padding |
| abl_a | First 2,224,128 bytes match checked-in abl.img, SHA-256 `19accd9e6fd423e79bac7741e6710cf3303b7a388d85dd31094fa00269e6c70a`; remaining partition bytes not compared |

The un-packaged init_boot output differs from the packaged image in four CPIO
node modes and archive/compression/signing metadata. All 36 CPIO entries and file
contents match; the installed image matches the packaged image. This is not evidence
of an installed init_boot mismatch. Packaged images pass recursive avbtool checks;
that verification reads local artifacts, not every installed partition.

[AOSP's boot header specification](https://source.android.com/docs/core/architecture/bootloader/boot-image-header)
requires GKI v4 `os_version` to be zero and expects version information through AVB
properties. Both boot and init_boot carry valid `2026-10-05` AVB patch properties.
Do not fill the legacy header word with a guessed date.

## AVB cause and authorized live correction

Original top-level vbmeta flags were 3: HASHTREE_DISABLED and VERIFICATION_DISABLED.
Zumapro selects these when `WITH_AVB` is not true. libavb's verification-disabled
branch skips chained descriptors and the usual AVB kernel parameters. Boot's patch
property is in the chained image. The proprietary bootloader's exact fallback has
not been disassembled; the controlled metadata test establishes this failure's cause.

Before the test, `cmd remote_provisioning certify default` fails with HTTP 400,
rejecting `boot_patch_level=20000000` as an invalid date. A fresh CSR contains it.
The user explicitly authorizes the signed flags-1 write/reboot after recovery
implications are explained. At 22:56:40 UTC, the candidate is written to vbmeta_a
and read back exactly before reboot. Android boots and the installed candidate is
verified again. Only HASHTREE_DISABLED remains; signing public key, rollback fields
and all 15 descriptors are preserved. avbtool reorders descriptors without changing
content. No relock, wipe, slot change or vendor/Trusty firmware modification occurs;
the experiment changes vbmeta boot metadata.

| Selected state | Original flags 3 | Installed flags 1 |
| --- | --- | --- |
| CSR boot_patch_level | 20000000 | 20261005 |
| RKPD certify default | HTTP 400, invalid date | Exit 0, four certificates |
| ro.boot.vbmeta.size | Absent | 19776 |
| ro.boot.vbmeta.hash_alg | Absent | sha256 |
| Hardware boot state | Orange / unlocked | Orange / unlocked |
| Verity | Disabled | Disabled |
| Play Integrity labels | All absent | All absent |

Fresh CSR otherwise retains os_version=170000, system_patch_level=202611,
vendor_patch_level=20261005 and security_level=tee. Only selected fields are retained;
CSR signatures are not independently checked in this decoding step.
Android properties cannot repair already-established trusted boot information.

## Production chain and ordinary Keystore verification

- `certify default` now returns four certificates. OpenSSL verifies the complete
  path and root self-signature. Root SHA-256 is
  `6d9db4ce6c5c0b293166d08986e05774a8776ceb525d9e4329520de12ba4bcc0`,
  matching the official [Google root endpoint](https://android.googleapis.com/attestation/root).
  Duck's existing ROOTS list already contains it; no pin change is needed.
- Fresh Duck provisioning yields five CA certificates. All have CA:TRUE and Certificate
  Sign; the complete chain and root self-signature verify with OpenSSL. Imported cert
  DER SHA-256 is `f0d95fa094aee809b7598376856c97a012f89bec96b958f97266a58fcbfdb55f`.
  Earliest chain expiry is **2026-11-20 09:46:07 UTC**.
- Its Android attestation extension reports version 500, TEE security level,
  purpose ATTEST_KEY=7, origin IMPORTED=2, deviceLocked=false,
  verifiedBootState=UNVERIFIED=2 and boot_patch_level=20261005. These are actual
  hardware claims. The import challenge was not independently rechecked here.
- Existing `/system/bin/keystore_cli_v2` generates a unique temporary TEE RSA-2048 key.
  SHA-256 sign/verify returns `Sign: 256 bytes` and `Verify: OK`. The alias is deleted
  and confirmed absent. No delete-all command is used.
- Only certificate PEM blocks are extracted from the on-phone keybox. Private keys
  and complete XML remain on the phone. Sanitized fingerprints/fields are recorded in
  [tokay-avb-fix-verification.json](tokay-avb-fix-verification.json).
- No post-fix targeted-app, renewal or secondary-user probe is run in this session.
  The new stored chain has five certificates; it differs from the earlier four-CA
  factory path. Earlier consumer-chain counts do not describe this new issuance.

## Source fix and publication

Clean commit [13f60c3](https://github.com/fruity-lineage/android_device_google_zumapro/commit/13f60c3e3a84ace1a311082f134d4a0ab3ae0abd)
changes Zumapro's default AVB argument to `--set_hashtree_disabled_flag`.
This retains disabled dm-verity while preserving chained boot metadata verification.
`WITH_AVB=true` still selects normal AVB. The commit uses the user's identity/sign-off
and includes source references; this is an original fix, not a cherry-pick.

Publication verifies identical blob/tree/commit, upstream parent, controlled fork
and default branch main. The worktree is `/tmp/tokay-avb-port`; active source checkout
and workspace manifests remain unchanged. Tokay/combined handoff overlays now select
the eleventh fork. Frankel's Laguna configuration is unchanged and has no hardware proof.

Scoped make evaluation covers unset/false/true WITH_AVB. Scoped Tokay preflight passes
with zero errors/warnings, separating 76 normal and two recovery manifests. The generic
checker initially combines recovery/normal HALs and uses family extraction lists; those
known wrapper issues are resolved by the existing device-scoped wrapper. Commit whitespace
passes. No ROM/kernel build or lunch is run. Hardware validation uses a signed derivative
of the existing image, rather than an OTA rebuilt from the new source commit.

| Inspected project | Revision / path |
| --- | --- |
| device/google/zumapro | c03df81e8fed84aeb4f2d26e9cef2ea5762d7c3f; BoardConfig-common.mk |
| external/avb | 01ecfc9c3df4fbe3e785185742f3313252e70a18; libavb/avb_slot_verify.c |
| system/keymint | cfeefc94bf8c4f19d19dca193d376a1fc05e8e3e; ta/src/rkp.rs and early-boot gates |

## Preservation and continuation

Server artifacts stay in `out/porting-tests/tokay-avb-metadata/`:

- `vbmeta-original-a.img`: complete original 65,536-byte partition backup, hash above.
- `vbmeta-flags1.img`: unpadded derivative, SHA-256
  `54e76b6dbda4c6aaba87e564505083dbc27413ae83491d57b04bba5d1c506502`.
- `vbmeta-flags1-padded.img`: currently installed partition image, SHA-256
  `777f68b817b2f4d77fa0a37c99bc2ced3d209fc2044af4caa40be5a03b822616`.
- `verification.json` and `live-test-state.json`: artifact/live phase records.

On-phone original vbmeta is `/data/local/tmp/lineage-avb-vbmeta-original-a.img`;
the candidate copy is `/data/local/tmp/lineage-avb-vbmeta-flags1.img`, both mode 0600.
The pre-renewal keybox backup stays at `/data/system/duck_rkp.xml.pre_remote_20261108`,
mode 0600. Keep these backups. The checker dialog is closed, temporary UI dump removed
and temporary USB stay-awake restored to its original global setting 0.

The [read-only collector](../tools/check-play-integrity.py) has nine passing unit tests.
It inspects selected configuration/decoded fields without authenticating signed tokens.
BASIC/DEVICE/STRONG remain incomplete. Google's
[verdict requirements](https://developer.android.com/google/play/integrity/verdicts)
require locked manufacturer-certified boot for DEVICE on Android 13+; STRONG adds
update requirements. Certificate issuance does not establish Google acceptance.
