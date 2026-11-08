# Final source verification

Verified 2026-11-08 UTC after the existing reviewers finished, then committed and checked
the final source trees. This report supersedes the earlier uncommitted-work status.

The baseline source review and scoped static checks pass after corrections. A subsequent
Tokay import-attestation adapter is committed and statically checked; its details are in
[tokay-duck-import.md](tokay-duck-import.md). The user's subsequent Tokay build produced
a verified OTA after three fixes. Compiled Settings, Keystore2, runtime libc and policy
outputs exist; [tokay-build-followups.md](tokay-build-followups.md) records the fixes and
artifact checks. Full acceptance remains pending: Android tests, hardware signing,
device behavior and Frankel compilation have no verified result.

## Scope and corrections

Reviewed the 94 changed/new feature files across bionic, external/bouncycastle,
vendor/lineage, system/core, device/lineage/sepolicy, frameworks/base and Settings.
Read the earlier framework, Settings and native/history reports and checked their
findings against the current sources. All source pins and commits are in the inventory.

Corrections made during this verification:

1. Restored the internal EC factories/generators and SHA256withECDSA provider required
   by CertificateGenerator and KeyBoxManager.
2. Applied the same supported-backend check to Duck availability, enablement, manual
   provisioning and automatic scheduling. Direct calls cannot bypass Tokay's gate.
3. Refused to replace malformed sandbox_config JSON during an update.
4. Bounded keybox, revocation, profile and Flash API response reads; closed streams/connections.
5. Checked refresh persistence failures and rechecked feature/config state after network work.
   Background keyboxes now undergo the actual framework validation before storage.
6. Added EC provider/keybox mismatch/truncated-refresh and Duck capability regressions.
7. Added and ran synthetic ELF extraction tests, and verified the selected firmware hashes.

The earlier reviewers' package filtering, lifecycle, import-validation and native
low-pointer corrections were retained. The bionic import and its local correction
were committed separately. Other project commits keep connected dependencies together.

## Checks and evidence

| Check | Result | Evidence/qualification |
| --- | --- | --- |
| Source/commit identity | Baseline 94 files; follow-up 99 combined files checked | verification-source-hashes.json; verification-duck-import-source-hashes.json |
| Git state | Nine port projects clean; twelve local commits checked | port-commits.json; original authors/coauthors and user sign-off |
| Whitespace/conflicts | Pass for committed patches and new files | verification-whitespace.json; existing untouched whitespace is not a new defect |
| Managed source syntax | 41 Java and 16 Kotlin parses pass | verification-managed-syntax.json; Tree-sitter wheels isolated in /tmp/tokay-spoofing-parsers |
| Resources | 353 references resolve, 244 names unique | verification-resources.json |
| Navigation | Eight destinations exist and are registered | verification-resources.json |
| ActivityManager API | 276 old signatures preserved; 15 additions implemented | AIDL --apimapping on old/current inputs; verification-ams-api.json |
| Frozen Duck API | --checkapi=equal and version-1 hash pass | VINTF structured check; hash cd81fee8f3ef4a488c0020e2e0e4fd6e5e1f0bf4 |
| Syscalls | Six private entry points; no colliding public generated wrappers | Actual SysCallsTxtParser; verification-syscalls.json |
| Feature preflight | Zero errors, zero warnings | Skill checker on policy plus selected module directories |
| Tokay preflight | Zero errors, zero warnings | porting/tools/preflight-tokay.py; qualifications below |
| Extractor tests | Eight tests pass | test_extract_trusty_apps.py; ELF32/64, both byte orders, truncation, segment/header bounds |
| Firmware identity | tzsw.img plus five selected payloads match recorded hashes | tokay-trusty-selected.json; extraction uses original image without changes |
| Import adapter follow-up | Five final Java parses and two Rust rustfmt checks pass | tokay-duck-import-verification.json; parsing/formatting, not type checking |

The native parser attempt in verification-syntax.json encounters Android C++ macros and
Clang C atomic extensions, including constructs with identical failures in the stock
files. It is not a clean C++ compiler result. Native symbol/syscall checks and the prior
inspection support the static assessment. Subsequent Tokay build outputs provide
native compilation/linking evidence; runtime acceptance remains pending.

AIDL --checkapi is intended for structured stable interfaces and rejected the stock
unstructured ActivityManager dependencies. The successful --apimapping checks were used
for that interface instead. Frozen Duck AIDL was checked with --structured --stability=vintf.
No source code was changed to silence checker errors.

## Tokay preflight qualification

The generic checker initially reported the same IHealth/default instance in vendor and
recovery XML. The module definitions explicitly use soc_specific:true and recovery:true,
respectively: they belong to separate images. Its extraction-list warning also came from
scanning the caimito root instead of caimito/tokay.

The wrapper uses the Tokay extraction lists and checks normal and recovery manifests
separately: 76 normal manifests and two recovery manifests. Synthetic assertions verify
that equivalent instances in separate images pass while duplicates within one image fail.
The shipped health modules/firmware were not changed.

The underlying checker still scans family makefiles statically; it is not a fully evaluated
Tokay product graph. The separate policy-scoped preflight does not compile SELinux or prove
neverallow success. Keep those distinctions when reusing the zero-error result.

## Pending tests and known risks

No agent-run Android or kernel build was used. The initial static review preceded the
user's Tokay build; the subsequent OTA and compiled outputs were inspected read-only.
The applicable
[ROM skill](/serverhive4/fruitzail/.agents/skills/rom-device-dev/SKILL.md) states:
“Nothing gets built to test — work must be right by inspection, symbol checking and
scripts/preflight.py.” The
[cherry-picking skill](/serverhive4/fruitzail/.agents/skills/reverse-engineering-cherry-picking/SKILL.md)
also requires this static-only workflow. The user did not explicitly request a build
in this verification turn. Syntax/resource/preflight results do not imply compiled success.

Added Android/bionic regressions are present but unexecuted:

- PackageManagerServiceServerTests: ROM/core UID filtering, hidden-app self-resolution and
  launcher role changes.
- FrameworksCoreTests: internal EC keybox loading, mismatched keys and truncated refreshes.
- RemoteProvisioningServiceTests: renewal/retry behavior and supported-backend gating.
- FrameworksServicesTests: native CSR challenge/key binding, signatures and malformed input.
- bionic fcntl test: open/open64/openat/openat64 with a low invalid pathname pointer.

Concrete remaining limits:

- Arbitrary unmapped pathname pointers can still be dereferenced by the imported native
  hooks in app contexts. The local low-address/process-order guard is a partial fix.
- Settings imports and reset span individual Binder/provider writes; a persistence/service
  failure can partially apply a parsed import or reset.
- Background refreshes reject observed edits after downloads, but separate settings writes
  offer no cross-process compare-and-swap; a narrow final write race remains.
- Response size bounds need comparison with live data and document-provider behavior.
- Runtime GMS availability is not established by this LineageOS product configuration.
- Tokay's subsequent build provides compilation and compiled-policy evidence; Android
  tests and actual device behavior remain pending. Frankel compilation is unverified.

## Tokay Duck backend

Tokay uses Rust Trusty KeyMint. The Xiaomi HAL relies on Qualcomm commands and ABI.
The target secure CSR path requires authenticated/MACed keys. No equivalent external-key
signing command has been established from the available Trusty sources or firmware leads.

The five extracted payload identities were reverified; names and signatures in an ELF
inventory are evidence of artifacts, not proof of a signing capability. The Qualcomm
HAL/service/VINTF/policy were not installed on Tokay.

The standard import-attestation adapter now uses the existing Keystore/Trusty KeyMint
services, with import issuer selection and chain processing fixed. Tokay selects it and
supplies the missing RKP hostname default. Availability requires the hostname and
standard service declarations, and the master setting remains opt-in. The full chain
validator still rejects inadequate production CA path lengths, usage or roots.

No Tokay external-key signing, hardware attestation success or remote acceptance is claimed.
Source-history coverage is bounded to the connected active stack and stored queries, not
every file in all 101 organization repositories or all historical branches.

Subsequent targeted disassembly verifies shipped HWBCC peer-UUID rejection before
signing and app-loader signature/policy checks. Standard imported-key attestation's
Keystore/RKPD integration gap is fixed, while production CA constraints remain unverified. See
[tokay-backend-investigation.md](tokay-backend-investigation.md) for source pins,
addresses and exact limits. These additional static findings do not complete the backend.

## Handoff

Twelve local commits are recorded in [the inventory](../../spoofing-inventory.md).
All nine port projects are clean and 99 committed files match the current review hashes.
The pre-existing build/soong modifications remain outside the port. Root Markdown and
porting artifacts persist as workspace memory; the root is not a Git repository.

Publication follow-up: ten source forks now use main, with original authors and user
coauthor credit retained, reference URLs included, and identical source trees. The
Frankel device configuration adds one separately checked file and was prepared in an
isolated worktree while the user reported a Tokay build. Its full device preflight and
hardware validation are pending. Source mappings and remote verification are recorded
in publication-commits.json and publication-verification.json. Agent notes and porting
artifacts now reside in their own Git repository, linked from the Android root.

Both device configurations now place their properties in the product partition. Fifteen
source commits were published, and 100 snapshot files were checked at that checkpoint,
including the isolated Frankel file. The active caimito property edit was preserved;
published source corrections were prepared separately. The HTTPS Git
endpoint returned HTTP 403, while GitHub API permissions and publication succeeded.

Build follow-up: seventeen source commits are now public. Security and Settings received
separate fast-forward fixes matching the user's amended build trees; caimito's matching
property fix was already public. All 101 current snapshot files match published trees.
The OTA checksum, ZIP CRC, declared metadata and selected installed artifacts are
verified in tokay-build-followup-verification.json. Active source files, branches and
manifests were preserved. Hardware signing and remote acceptance remain pending.
