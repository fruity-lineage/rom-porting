# Workspace memory

Updated 2026-11-08 UTC after verifying the user's Tokay build outputs and publishing its follow-up fixes.

## Setup

- Workspace: /serverhive4/fruitzail/evox; Android Repo workspace, not a root Git checkout.
- Manifest: LineageOS lineage-24.0, Android android-17.0.0_r1.
- Device: Pixel 9, tokay, platform zumapro.
- Network source downloads succeeded.
- Workspace create/read/delete and GitHub HTTPS passed after access was restored.
- The user connects over remote SSH. ADB network access is permitted, but configured
  and default local endpoints refused connections; no device enumeration succeeded.
  Hardware validation requires a reachable ADB server or tunnel to the local device host.
- User Git identity: fuzailmansuri <mfm9875@gmail.com>.
- Publication authorized under fruity-lineage, limited to ported work. Ten source forks
  now have verified main tips and default branch main. Original authors and user coauthor
  credit are retained; publication messages include references and omit Gerrit Change-Id.
  Source trees are identical to the local topic commits. The mapping is in
  porting/audit/publication-commits.json. Handoff repository: fruity-lineage/rom-porting.
- The complete initial handoff is published on main at d6a940198b57eedadb5333ad2a7a940626d14c1e.
  All 57 tracked files and the tree match the local commit; all ten source fork tips
  were rechecked at that point. See porting/audit/handoff-publication-verification.json.
  Subsequent documentation commits record publication status without altering source forks.
- fruity-lineage/.github/main contains a device-neutral organization profile linking
  the handoff and disclosing AI assistance, as required by the ROM development skill.
- Read taste.md, tasks.md, spoofing-inventory.md and the final verification report before continuing.

## Tokay sources

All five projects were synced from matching lineage-24.0 branches through
.repo/local_manifests/tokay.xml.

| Local path | Upstream | Role |
| --- | --- | --- |
| device/google/tokay | LineageOS/android_device_google_tokay | Wrapper/extraction entry point |
| device/google/caimito | LineageOS/android_device_google_caimito | Pixel 9 family tree; tokay/ holds this device's extraction lists |
| device/google/zumapro | LineageOS/android_device_google_zumapro | Shared platform |
| device/google/caimito-kernels | LineageOS/android_device_google_caimito-kernels | Kernel modules/output destination |
| vendor/google/tokay | TheMuppets/proprietary_vendor_google_tokay | Proprietary blobs/firmware |

Vendor is shallow. All 15 LFS files were downloaded and initially passed git lfs fsck.
No device/vendor firmware edits were made during this verification.

## Kernel

- Nested Repo workspace: out-kernel/google/gs-6.1; all 18 projects initially synced.
- Manifest: LineageOS/android_kernel_google_gs-6.1_manifest, lineage-24.0.
- Common kernel: common/gki, android14-6.1-2026-03_r25, Linux 6.1.162.
- Device config: private/devices/google/caimito; modules: private/google-modules.
- The .out-dir marker excludes the nested workspace from Android source scans.
- caimito/device-tokay.mk selects caimito and google/gs-6.1.
- vendor/lineage/build/envsetup.sh initializes and builds the nested workspace, copying
  output into device/google/caimito-kernels/6.1.
- Do not invoke lunch to inspect configuration: it can trigger kernel work.
- No Android/kernel build was run during this verification. Existing output directories
  are not evidence of a successful validation of these commits.

## Port and verification checkpoint

The active Evolution X cnb manifest uses the same Android 17 tag and LineageOS 24 base.
Its vendor_evolution and device_evolution_sepolicy map to vendor/lineage and
device/lineage/sepolicy. Complete source snapshots are in /tmp/evo-spoofing-upstream;
additional compared text blobs are in /tmp/native-extra-sources. These temporary paths
are investigation caches; durable pins and evidence are in porting/audit.

The initial twelve-commit checkpoint covers nine projects on port/evolution-spoofing:
bionic, external/bouncycastle, vendor/lineage, system/core, device/lineage/sepolicy,
frameworks/base, packages/apps/Settings, system/security and device/google/caimito.
All nine were clean at that checkpoint. The user's build fixes were subsequently
amended into three local topic tips; those active checkouts remain untouched.
The same source trees are published through separate follow-up commits and isolated
worktrees. Pre-existing build/soong changes remain outside the port. There are now seventeen source commits
across ten published forks; original checkpoint hashes remain recorded below.

The port includes PIF, TrickyStore, game/device identity, package visibility, Aurora
installer reporting, per-app Settings-value overrides, their Settings UI, native hooks,
property staging and Duck framework/AIDL. The broader Sandbox feature set is excluded
because it is not a dependency of the selected Settings-value overrides.

Verified: 94 committed source hashes; 41 Java/16 Kotlin parses; 353 resource references;
244 unique names; eight destinations; 276 preserved plus 15 implemented AMS signatures;
frozen Duck AIDL/hash; six private syscall replacements; zero-error/warning scoped
preflight; eight extractor tests; five selected firmware payload hashes.
The follow-up verifies 99 combined committed source hashes (88 baseline files unchanged),
five final Java parses, two Rust rustfmt checks and zero-error/warning Tokay preflight.

Review closed missing EC provider registration, direct Duck gate bypass, destructive
malformed-config updates, unbounded network reads, unchecked refresh writes and stale
background downloads. Added Android/bionic tests remain unexecuted. The subsequent
user build provides Tokay compilation and compiled-policy evidence, recorded below;
hardware behavior remains pending.

[verification.md](porting/audit/verification.md) records exact checks and limitations.
[spoofing-inventory.md](spoofing-inventory.md) contains source pins and all commit hashes.
Published revisions differ from local hashes because commit metadata was cleaned. Local
topic branches and backup/pre-fruity-publication-20261108 remain available. The overlay
at porting/manifests/tokay.xml selects all nine main forks, four unchanged Tokay dependencies
and the handoff repository, linking the root notes and porting tools into the workspace.

## Frankel and active build checkpoint

- User added Pixel 10 frankel as a target and requested device-neutral GitHub descriptions.
- Wrapper: device/google/frankel. Actual family tree: device/google/muzel; shared platform: laguna.
- All three source trees were synced from lineage-24.0; their pins are in frankel-import-verification.json.
- Laguna selects Rust Trusty KeyMint, ships API 36, and already sets TEE RKP-only.
- The isolated Frankel product port selects the same standard import-attestation adapter
  and supplies the missing RKP hostname default. It is published in android_device_google_muzel/main
  at 2b195b35d051eb63c9dcc6b02ff66a9e5c1a6a61, with source/property checks passing.
  The current main tip is 9c4bad6692c8275790bff334263914ddbd2a59e5 after moving
  device properties to PRODUCT_PRODUCT_PROPERTIES, matching the generic-system layout.
- caimito/main is now 2f7cc304134f77b3858da6e9d2390a5b22fbc467 with the same
  product-partition correction captured independently of the active build checkout.
- The active muzel checkout remains at its upstream pin; the change is in /tmp/frankel-duck-port.
  Use the public main tip as the durable copy. The user's Tokay build produced an OTA;
  the agent preserved active sources and manifests during publication and verification.
- Frankel vendor and muzel-kernel dependencies exist upstream but were not synced here.
  Complete device preflight, compilation, hardware import and production CA acceptance are pending.
- New overlays select either family or both via porting/manifests. Install one overlay
  after active builds finish; do not install overlapping overlays together.
- The handoff's actual Git checkout is agent-memory. Root notes and porting are linked into it.
- Ten remote forks and their source credits/trees are verified through the API. The
  HTTPS Git endpoint subsequently returned HTTP 403 despite verified push permissions;
  the two product-property commits were uploaded through Git data APIs with identical
  commit IDs. Do not expose credentials in troubleshooting or handoff notes.

## Tokay firmware constraint

The three Xiaomi HAL references use libkeymasterdeviceutils.so, Qualcomm commands
0x311e/0x3122 and a vendor object ABI. Tokay uses Rust Trusty KeyMint,
com.android.trusty.keymint and tee_device at /dev/trusty-ipc-dev0. AOSP KeyMint's secure
RKP path validates MACed CSR keys; raw external keys are not an equivalent request.

The initial tree lacked Duck AIDL/callers; the framework/AIDL port now supplies them.
Evolution X's available Trusty sources did not provide an equivalent external-key
extension. The Qualcomm HAL and its VINTF/policy were not installed on Tokay.

tzsw.img and five selected ELF payloads were re-extracted/hash-verified. Service-name
hints identify leads, not capabilities. No supported direct external-key CSR signing
entry point is verified. The alternative import adapter retains a capability gate.

Targeted disassembly now confirms the shipped HWBCC sign and BCC callbacks reject
the non-secure peer UUID before signing. KeyMint's UUID selects a separate GSA use case.
The app loader verifies signatures and signing-key policy; Android bootloader unlock
does not establish that a modified trusted app can load.

Standard imported-key attestation is now implemented as an alternative source adapter:
Duck generates an EC P-256 key, imports it as ATTEST_KEY through Keystore2's TEE security
level, and validates its certificate chain before producing the existing XML keybox.
Keystore import now honors user/RKPD attestation-key selection, keyblob upgrades and
chain processing. Tokay selects it with ro.lineage.duckrkp.trusty_import=true and an
optional production remote_provisioning.hostname default; this hostname was absent.
Availability requires a hostname plus Keystore2, TEE KeyMint and RKP declarations.
The Duck master setting remains opt-in. No new HAL daemon or Trusty command is needed
for this route; existing init, VINTF and service policy are traced in
[tokay-duck-import.md](porting/audit/tokay-duck-import.md).

Production CA constraints, firmware import acceptance and consumer compatibility remain
unverified. This route adds an imported CA certificate with actual imported origin and
boot state; it is not equivalent to Duck's direct external-key CSR protocol. Existing
RKPD hybrid/factory fallback behavior is retained. Full certificate validation rejects
unusable chains. [tokay-backend-investigation.md](porting/audit/tokay-backend-investigation.md)
records the unchanged firmware constraint. No hardware signing success is claimed.

## User build output verification (2026-11-08)

- Tokay's Android 17 OTA was generated by the user's build; no agent-run build was used.
- Package: `out/target/product/tokay/lineage-24.0-20261108-UNOFFICIAL-tokay.zip` (1,705,536,749 bytes).
- SHA-256: `55f7a4cec8e04562628351d9c685159a864b4d77470aad320a521129d1c86852`.
- ZIP CRC verification passes; embedded metadata declares tokay, SDK 37 and the 2026-11-01 patch level.
- Installed Settings contains the compiled focus-ring helper. Keystore2, runtime libc,
  product properties and compiled vendor policy are present and hash-recorded.
- Signing-key identity and the OTA signature were not verified. A complete source
  manifest was not captured before the user's build.
- Resolved build issues:
  1. `device/google/caimito`: Moved RKP and Duck properties to `PRODUCT_PRODUCT_PROPERTIES` to satisfy generic system artifact path requirements.
  2. `system/security`: Fixed the callback return type to `Result<KeyCreationResult, Error>` and removed premature anyhow context from import.
  3. `packages/apps/Settings`: Restored `src/com/android/settings/widget/InsetFocusRing.kt` for Compose UI focus rings.
- The property correction was already public. The other two fixes are now separate
  fast-forward commits: system/security a39ce2250d6ad58dcefa377bdd9e8465fd83e9c8
  and Settings 233ff319af4e0eb8369b4f1a5f976b3205a591e9. The helper exactly matches
  Joey's upstream file and retains his authorship plus user coauthor credit.
- Current active tips: security 27c3ec5862429ce676e1a396a747caf7c4567da1,
  Settings 53030932d1aa4b763b77c5085b2430709048dbe0,
  caimito bf2174958d133abfd1f233dd559e019939d8f707. Their trees equal the public tips.
- All 101 current snapshot files match the published trees. See
  [tokay-build-followups.md](porting/audit/tokay-build-followups.md) and its verification JSON.

## Known acceptance limits

- Android/bionic regressions and hardware acceptance are pending. Tokay build outputs
  provide compilation/linking and compiled-policy evidence; Frankel compilation is pending.
- Arbitrary unmapped pathname pointers can still crash the imported native app hooks;
  the committed guard fixes low pointers and non-app inspection only.
- Imports/reset span individual Binder/settings writes and can partially apply on failure.
- Background refresh rechecks edits after downloads, but the settings provider offers no
  cross-process compare-and-swap transaction; a final narrow race remains.
- This configuration does not inherit vendor/gms; runtime GMS availability must be verified.
- Coverage is bounded to recorded connected sources/history, not every org repo/branch.

## Scoped validation commands

For the device checks, use the saved
[Tokay runtime verification prompt](porting/audit/tokay-runtime-verification-prompt.md).
It covers ADB access, provisioning, chain validation, actual signing and regressions;
preparing the prompt does not establish a hardware result.

Run from the Android root:

- PYTHONDONTWRITEBYTECODE=1 python3 porting/tools/preflight-tokay.py
- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s porting/tools -p test_extract_trusty_apps.py -v

The first wraps the skill checker to use caimito/tokay extraction lists and separates
normal/recovery manifests. Its underlying product scan is static and includes family
makefiles, not a fully evaluated Tokay build graph. See verification.md before interpreting it.
