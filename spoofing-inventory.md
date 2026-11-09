# Evolution X spoofing and Duck RKP port inventory

Updated 2026-11-09 UTC after live checks and the Settings/renewal/boot fixes.

Targets: LineageOS lineage-24.0 / Android 17, Pixel 9 (tokay, zumapro) and
Pixel 10 (frankel, laguna).
Source: [Evolution X repositories](https://github.com/orgs/Evolution-X/repositories),
active cnb sources and the supplied device commits.

21 source commits in eleven forks cover the shared stack, import configuration
and AVB metadata correction. Earlier static/build evidence remains in the recorded
checkpoints. Tokay now directly passes RKPD certify default, imported ATTEST_KEY
issuance with a five-CA production path and ordinary TEE signing after the authorized
flags-1 vbmeta reboot. The selection property persists. Fresh checker BASIC/DEVICE/STRONG
still fail, with recognition/licensing UNEVALUATED. These hardware results do not apply
to Frankel; its compilation and device checks remain pending.

The [live investigation](porting/audit/tokay-live-integrity-investigation.md) and
[AVB verification](porting/audit/tokay-avb-fix-verification.json) record before/after
boot metadata, certificate fingerprints, actual verdicts and recovery backups.
The Zumapro source fix is published from an isolated worktree; handoff overlays select
its main branch. Active build sources/manifests remain unchanged. No rebuilt OTA with
this source fix was made; the signed metadata derivative was tested on the phone.

The subsequent [Duck status check](porting/audit/tokay-duck-status-followup.json)
recorded Ready/no error following the user's failure report. The later parallel review
found and fixed the obsolete Qualcomm-only Settings description and a recoverable-error
renewal pause. Restored live ADB again confirmed Ready/no error and a valid stored
certificate path. The renewal fix is not yet built or exercised on hardware.
The boot follow-up migrates known temporary legacy pauses and safely defers eager-service
unavailability before import; existing boot restoration requires no Settings visit.
Checker-source review shows omitted labels render as crosses; unevaluated licensing
also affects optional labels, so BASIC's device criteria have not been isolated.
See [RKP integration review](porting/audit/rkp-integration-review.md).

## Supplied device references

- [SM8450](https://github.com/Evolution-X-Devices/device_xiaomi_sm8450-common/commit/6249226dc962b78852097d4612875fc16dd665e5)
- [SM8350](https://github.com/Evolution-X-Devices/device_xiaomi_sm8350-common/commit/05c24b7c09b6191ab36fcee8c8570e721c8c3b8b)
- [SM8150](https://github.com/Evolution-X-Devices/device_xiaomi_sm8150-common/commit/7a897d3132891d74d812496cb52e55b38ab85a79)

These share Duck C++ blob 7024d9ba856be8b359b546b83468c36318bc191f, Qualcomm
commands 0x311e/0x3122 and the vendor C++ object ABI. The Qualcomm HAL, worker
domains and its VINTF instance were not installed on Tokay. MIT notices and
Duck-ToolBox framework provenance are preserved.

## Active source pins and disposition

| Evolution X source | Pin | Target/disposition |
| --- | --- | --- |
| frameworks_base | ddce89c4142f89e85830bf3cd2980cf7f472f705 | frameworks/base; services, hooks and Duck framework/AIDL |
| bionic | 57ae6d98c1c1aec194cbe0cde12f55f6731e7523 | bionic; accumulated hooks and separate pathname correction |
| vendor_evolution | 4d2922ad10997b31aaa6bec9eada2222e1b96e4a | vendor/lineage; optional API-level defaults |
| system_core | ea0752d2d09c1fffdb4e40c048735b1a0a28fd95 | system/core/init; optional API-level publication; no equivalent Duck Trusty extension |
| device_evolution_sepolicy | 4b8d3e4437e40df5eed0e3c6013bde2161f2d424 | device/lineage/sepolicy; restricted staging properties |
| packages_apps_Evolver | 17ba8bbbc530c305efcc3c102bbc9d6f97e99f4d | Spoofing screens adapted into packages/apps/Settings |
| packages_apps_Sandbox | db3d493ae3bd988e3df682c81941867c0f81b5b2 | Settings-value UI/backup reference; broader sandbox excluded |
| vendor_extras | 1a97709e05739e0d4b05b37583a01eaa4df7cac8 | Settings-value SDK subset relocated into framework |
| external_bouncycastle | 56e5dac751581c7bd6dbe363d7ba3f8e8862c5bf | Required internal EC/ECDSA provider registrations |
| packages_apps_Settings | 2b1b584855717b32dff2e3b33fb422b1adede1c6 | Audited; active UI originates in Evolver |

frameworks_native, frameworks_av, libcore, lineage-sdk, packages_apps_LineageParts
and system_sepolicy have recorded negative connected-feature coverage. Additional API
tree/blob comparisons cover build, Soong, hardware/interfaces, hardware/google/pixel,
fs_mgr and GMS configuration. Archived Pif/certification apps are absent from the active
manifest and were not imported. GMS prebuilts are runtime consumers; this LineageOS
configuration does not inherit vendor/gms. Proprietary GMS runtime checks were not audited.

This is bounded evidence, not exhaustive coverage of all 101 public repositories or
every historical branch. Source histories, patches and negative coverage are in porting/audit.

## Local port commits

These are the original local checkpoints on port/evolution-spoofing. Publication
revisions below remove Gerrit-only metadata and add missing implementation references
while retaining identical trees, original authors, human coauthors and user sign-off.
No upstream PR was opened.

| Project | Commit | Change |
| --- | --- | --- |
| external/bouncycastle | 38ec66a303d02bb3a1967ce7c5626bc6391b1303 | Required internal EC/ECDSA providers |
| bionic | 1cc5429a200f25a2042bc68a8bda192c6d191d7f | Accumulated native hooks |
| bionic | f9af17ea14834116d9689fe54e597bf4cef46558 | Pathname guards and low-pointer regression |
| vendor/lineage | 8c9e5f8ea343e0e2aaab001a8547a655d31a4d1c | Optional first-API Soong defaults |
| system/core | f5278125f50e104cb2315d947c721957a6601d81 | Optional first-API map update before publication |
| device/lineage/sepolicy | 2650f11ca9996f7f7faaa61acb14268bb7a60c51 | PIF staging type and scoped access |
| frameworks/base | b2cb692a58995923598768877c0397cdd980a166 | Connected services, keystore hooks, Settings-value APIs and guarded Duck |
| packages/apps/Settings | a2bc940f5c9089ea445f1baaacaa68e307456b45 | Screens, resources, import validation and scoped reset |
| system/security | cc1f9e42200d3e9c7a1aa47e433bd72023162002 | Import attestation-key selection, upgrades and chain processing |
| device/lineage/sepolicy | c9299e36c9738e4048bec188054ea0434e7b1798 | Scoped import-backend selection property |
| frameworks/base | 535d28c54c950b131550796c9829a4e572446df1 | KeyMint import adapter and certificate/backend regressions |
| device/google/caimito | 51ba2449f5180c93f6d2a7b4e6030a93034ed7f4 | Tokay selection and missing RKP hostname default |
| device/google/muzel | 2b195b35d051eb63c9dcc6b02ff66a9e5c1a6a61 | Isolated Frankel selection and RKP hostname default |
| device/google/caimito | 2f7cc304134f77b3858da6e9d2390a5b22fbc467 | Product-partition placement, captured outside the running build |
| device/google/muzel | 9c4bad6692c8275790bff334263914ddbd2a59e5 | Product-partition placement for Frankel |
| system/security | a39ce2250d6ad58dcefa377bdd9e8465fd83e9c8 | Concrete Keystore error type for generation/import callbacks |
| packages/apps/Settings | 233ff319af4e0eb8369b4f1a5f976b3205a591e9 | Missing shared Compose focus-ring dependency; Joey's upstream helper |
| device/google/zumapro | 13f60c3e3a84ace1a311082f134d4a0ab3ae0abd | Preserve chained AVB boot metadata while retaining disabled dm-verity |
| packages/apps/Settings | 0a2e3c2c7dd19611e2e0a131c7530573ed59fc1c | Remove obsolete Qualcomm-only RKP generation description |
| frameworks/base | 60153c127470c3855d4e979a4b60190f6b13bdf5 | Retry recoverable import provisioning failures; stop retry on alias cleanup failure |
| frameworks/base | 4755e2231cf2ccc5617b310a1fb28583e6cb2f89 | Resume known temporary states at boot; defer import until eager Keystore2 is ready |

Evolution vendor coverage: vendor/lineage contains the optional API-32 Soong change.
The audited global Pixel Beta fingerprint override explicitly excludes Tokay upstream
and was not applied. No separate Duck signing daemon was found in vendor_evolution.
The import adapter uses the existing Trusty HAL selected by the shared device product.

## Published forks

All eleven forks are public under fruity-lineage, with verified main tips and default
branch main. Local topic branches and backup refs retain the original checkpoints.
Every published change contains implementation/source references; adapted upstream
ports retain their author and fuzailmansuri's coauthor credit. Locally written fixes
retain their actual author.

| Project | Fork and main tip |
| --- | --- |
| external/bouncycastle | [android_external_bouncycastle](https://github.com/fruity-lineage/android_external_bouncycastle/commit/6d01d24edd9e4838ddde5be7cbcfff7b1d4ea7bc) |
| bionic | [android_bionic](https://github.com/fruity-lineage/android_bionic/commit/32c175151d1b0fd666de2bfa70b32e246d26cbe8) |
| vendor/lineage | [android_vendor_lineage](https://github.com/fruity-lineage/android_vendor_lineage/commit/887e8e0b3ae15e6c84de29953169392cd220a1c8) |
| system/core | [android_system_core](https://github.com/fruity-lineage/android_system_core/commit/19383c870279c12a823f1757ac455961b0973485) |
| device/lineage/sepolicy | [android_device_lineage_sepolicy](https://github.com/fruity-lineage/android_device_lineage_sepolicy/commit/7fc49f44fb98584fc3890f0e77609c246b19c126) |
| frameworks/base | [android_frameworks_base](https://github.com/fruity-lineage/android_frameworks_base/commit/4755e2231cf2ccc5617b310a1fb28583e6cb2f89) |
| packages/apps/Settings | [android_packages_apps_Settings](https://github.com/fruity-lineage/android_packages_apps_Settings/commit/0a2e3c2c7dd19611e2e0a131c7530573ed59fc1c) |
| system/security | [android_system_security](https://github.com/fruity-lineage/android_system_security/commit/a39ce2250d6ad58dcefa377bdd9e8465fd83e9c8) |
| device/google/caimito | [android_device_google_caimito](https://github.com/fruity-lineage/android_device_google_caimito/commit/2f7cc304134f77b3858da6e9d2390a5b22fbc467) |
| device/google/muzel | [android_device_google_muzel](https://github.com/fruity-lineage/android_device_google_muzel/commit/9c4bad6692c8275790bff334263914ddbd2a59e5) |
| device/google/zumapro | [android_device_google_zumapro](https://github.com/fruity-lineage/android_device_google_zumapro/commit/13f60c3e3a84ace1a311082f134d4a0ab3ae0abd) |

Bouncy Castle is a fork of Evolution-X/external_bouncycastle, which contains the
verified Android 17 base. LineageOS's GitHub Bouncy Castle mirror stops at older
Android branches. The other ten forks use their corresponding LineageOS parents.

[publication-commits.json](porting/audit/publication-commits.json) maps all 21 local
and public commits. Only ported code was uploaded; pre-existing build/soong edits remain
outside publication. The handoff repository is
[rom-porting](https://github.com/fruity-lineage/rom-porting); its manifest
overlay selects these forks and the unchanged Tokay dependencies.
Individual or combined overlays also include Frankel's unchanged dependencies.
GitHub descriptions are device-neutral; implementation details remain in the device audits.

The initial complete handoff is published at
[d6a9401](https://github.com/fruity-lineage/rom-porting/commit/d6a940198b57eedadb5333ad2a7a940626d14c1e).
Its 57 tracked files and tree match the local commit, including AGENTS.md, persistent
notes, audits, tools and all three manifest overlays. All ten source fork tips were
rechecked against the inventory. The organization profile is on .github/main at
[8e6a3e1](https://github.com/fruity-lineage/.github/commit/8e6a3e10b04ae67f0c1b112f86400c2b927b3f54).
See [handoff-publication-verification.json](porting/audit/handoff-publication-verification.json).
Publication did not modify the active build's source checkouts or manifests.

## Frankel source integration

The shared stack carries over. Its device product is in muzel, with Laguna selecting
Rust Trusty KeyMint and TEE RKP-only. The isolated five-line configuration selects the
adapter and supplies the hostname. Active Tokay sources and the active muzel checkout
were preserved. Source/property/whitespace checks pass; full vendor/kernel preflight,
compilation, firmware behavior and CA acceptance remain pending. See
[frankel-import.md](porting/audit/frankel-import.md) and its verification JSON.

## Verification

- The baseline 94 files were checked at the initial checkpoint. The follow-up verifies
  all 99 combined files, including 88 unchanged baseline files, against committed trees.
- The initial nine port working trees were clean at verification; commit whitespace and
  attribution were checked. The active build fixes are now in amended local topic tips;
  security, Settings and caimito are clean and match the public build-fix checkpoint.
  The later Settings wording fix is isolated from the active build checkout.
  Active Keystore2 subsequently acquired an unstaged reversal of its build fix;
  that concurrent edit was preserved and is excluded from publication.
- 41 Java and 16 Kotlin sources parse without syntax errors.
- 353 resource references resolve; 244 imported names are unique; eight destinations exist.
- All 276 prior ActivityManager signatures remain; all 15 additions have implementations.
- Frozen Duck AIDL equality/hash pass; syscall parsing finds six private replacements.
- Feature-scoped preflight: zero errors/warnings.
- Tokay preflight with device-specific lists and separate normal/recovery manifests:
  zero errors/warnings.
- Eight synthetic ELF-extractor tests pass; five selected payloads match tzsw.img.
- Import follow-up: five final Java parses and both Rust rustfmt checks pass;
  source/API/service/property inspection and scoped preflight pass. Added tests are unexecuted.
- Current device snapshots use PRODUCT_PRODUCT_PROPERTIES. Both partition corrections
  were published from isolated worktrees; the prior 100 combined snapshot hashes passed.
  Tokay's property edit is now committed in its active topic tip, and the active muzel
  checkout is unchanged.

The initial static checks did not establish compilation. The user's subsequent Tokay OTA
and installed compiled outputs provide build evidence after the three fixes above.
All 101 build-followup source snapshot files matched that checkpoint's public trees;
99 prior hashes were unchanged. The later 102-file combined snapshot records the
Settings, renewal and boot fixes plus the already-published AVB source correction.
See [tokay-build-followups.md](porting/audit/tokay-build-followups.md) for provenance,
artifact hashes and acceptance limits. Tokay hardware import and production chain verification now pass as recorded in
the live audit. Actual Play Integrity acceptance still fails; Frankel remains unverified.
Android/bionic tests remain unexecuted. C++ parser
limitations, non-transactional imports/reset, refresh races and the native invalid-pointer
edge case are detailed in the verification report.

## Tokay backend evidence

- device/google/zumapro/common.mk selects TRUSTY_KEYMINT_IMPL := rust.
- system/core/trusty/keymint/src/keymint_hal_main.rs defines Trusty service/channel framing.
- system/keymint/hal/src/rpc.rs serializes MACed-key requests.
- system/keymint/ta/src/rkp.rs enforces secure-side CSR key MAC validation.
- hardware/interfaces/security/rkp/aidl contains the RKP interface MAC requirements.
- device/google/zumapro/sepolicy/vendor/file_contexts labels Trusty devices/HALs.
- porting/audit/tokay-trusty-selected.json records five bounded, hash-verified payloads.

The raw external-key CSR protocol has no verified Tokay signing implementation. The new
import adapter is selected on Tokay; availability, enablement and provisioning require
its hostname and standard service declarations. The user master setting is opt-in.
Tokay does not enable SPOOF_FIRST_API_LEVEL_32.

Targeted shipped-firmware disassembly confirms HWBCC rejects non-secure signing and
BCC requests before selecting its KeyMint/GSA production path. App-loader signature
and signing-key policy checks also prevent assuming a rebuilt trusted app can load.
[tokay-backend-investigation.md](porting/audit/tokay-backend-investigation.md) records
the inspected source revisions, artifact identities, exact addresses and validation.

Standard imported-key attestation is now a committed alternative adapter, with Keystore's
RKPD import gap fixed and the existing service/init/VINTF/policy traced. Tokay firmware import and its returned production CA path are now directly verified.
Broader consumer behavior and Frankel hardware remain unverified. It adds
an imported CA, not direct external-key CSR certification. See
[tokay-duck-import.md](porting/audit/tokay-duck-import.md) and
[tokay-duck-import-verification.json](porting/audit/tokay-duck-import-verification.json).

## hardened_malloc port (2026-11-09)

Fourteen malloc-related source commits across twelve projects are published in
fruity-lineage forks on main. Every new subject starts with `malloc:`; original
upstream history/authors and human credits are retained. The full publication now
contains 35 source commits across 19 forks. Active Android/kernel inputs were preserved.

| Project | Published tip | New commits |
| --- | --- | --- |
| device/google/caimito | [0d5ae62983fd](https://github.com/fruity-lineage/android_device_google_caimito/commit/0d5ae62983fd9143f3a670ef25537b31ff084d90) | 1 |
| device/google/muzel | [300eef55c0b2](https://github.com/fruity-lineage/android_device_google_muzel/commit/300eef55c0b2bdef00236e2c99832bba29e7c34f) | 1 |
| system/core | [e45de95e2214](https://github.com/fruity-lineage/android_system_core/commit/e45de95e22142dc10a39c9d38c01942b781a357a) | 1 |
| out-kernel/google/gs-6.1/common/gki | [128e563a7b84](https://github.com/fruity-lineage/android_kernel_common_gs-6.1/commit/128e563a7b841cdee51ce79669fee61c99cd0890) | 1 |
| out-kernel/google/gs-6.1/private/devices | [62e7ed384bc4](https://github.com/fruity-lineage/android_kernel_google_gs-6.1_devices/commit/62e7ed384bc4a3ca22b0c2fc1eab1475ada35e2a) | 1 |
| out-kernel/google/gs-6.6/common/gki | [0bf6c56da947](https://github.com/fruity-lineage/android_kernel_common_gs-6.6/commit/0bf6c56da947b485f9c87d29f1c40008155c2420) | 1 |
| out-kernel/google/gs-6.6/private/devices | [0004aefef48d](https://github.com/fruity-lineage/android_kernel_google_gs-6.6_devices/commit/0004aefef48d189152996bc4ef1949e64d1bf161) | 1 |
| build/soong | [5851ab423c8e](https://github.com/fruity-lineage/android_build_soong/commit/5851ab423c8e23d764665e74dc72f9bca5963996) | 1 |
| build/make | [89f1e686f3c1](https://github.com/fruity-lineage/android_build/commit/89f1e686f3c1bfbc9ea0dfa921976c30c11df96b) | 1 |
| external/hardened_malloc | [8fd6c6016ef5](https://github.com/fruity-lineage/hardened_malloc/commit/8fd6c6016ef53cc97ee5bc6f521cf70859342e37) | 2 |
| bionic | [4bf97cec2ff7](https://github.com/fruity-lineage/android_bionic/commit/4bf97cec2ff7787b54e23ca557411efb445e320d) | 2 |
| system/memory/libmemunreachable | [7a95f0c9dee8](https://github.com/fruity-lineage/android_system_memory_libmemunreachable/commit/7a95f0c9dee850ccba4887c3b5b00820f20b0e2e) | 1 |

The [allocator audit](porting/audit/hardened-malloc.md) records the connected libc,
Soong/make, init, device, GKI and heap-inspection changes. Both Android and nested
kernel overlays are required. Thirty-three final modified files have recorded
SHA-256 hashes; GitHub commit/tree objects match prepared local revisions.

Static source, formatting, ABI signatures, architecture/configuration, preserved
native hooks, manifest linkfiles, attribution and publication checks pass. These
checks do not establish Android compilation or boot. The ten new libc test cases,
heap-inspection regression and upstream MTE tests remain unexecuted. Actual
allocator/vendor/MTE/module/FIPS behavior needs a coordinated build and testing.

See [hardened-malloc-publication.json](porting/audit/hardened-malloc-publication.json)
and the component verification reports. The existing RKP and consumer-acceptance
limits remain separate; allocator work does not change those recorded results.

## Active Tokay allocator inputs (2026-11-09)

The published source set is now installed into the actual evox Android and GS 6.1
checkouts. Fifteen existing projects use the publication-map tips on topic branches;
the allocator is a new Repo-managed project at 8fd6c6016ef53cc97ee5bc6f521cf70859342e37.
The installed overlays are .repo/local_manifests/tokay.xml and
out-kernel/google/gs-6.1/.repo/local_manifests/malloc.xml. Original histories, prior
source heads and unrelated Soong edits are preserved.

[Activation verification](porting/audit/hardened-malloc-activation.json) records each
previous/active commit and validation: 30 matching source hashes, unique Android
and kernel manifest paths, valid Repo metadata, successful local sync and zero-error/
warning scoped preflight. The existing OTA and installed device are unchanged; their
old build variables omit allocator opt-in and their old kernel output uses VA39.
Coordinated rebuilding and hardware verification remain pending. Frankel activation
was not performed. Publication and active-build integration are separate states.

[User RKP handover](porting/audit/tokay-rkp-user-handover.md) retains the later ABL and
StrongBox reports without promoting the proposed UNEVALUATED cause to verified fact.

## Full integrity acceptance remains open (2026-11-09)

The user requires actual BASIC/DEVICE/STRONG passing on Tokay. Source review
confirms EC-to-RSA issuer fallback and rules out a straightforward standard RKPD
opaque-key signer. The imported intermediate retains actual boot state; a verified
Tensor external-key signing backend and fresh passing verdicts remain absent.
[tokay-integrity-parity.md](porting/audit/tokay-integrity-parity.md) records exact
source references, configuration namespace correction and required device checks.
The current ADB tunnel refuses connection. No source/backend capability or passing
label was invented, and no phone setting, keybox or partition was changed.

## Tokay PIF runtime follow-ups (2026-11-09)

| Project | Published and active commit | Change |
| --- | --- | --- |
| frameworks/base | 9413fe868c27b3410c054f9a4666eb5d521501fa | Reset parsed flags; owner enable switch; staged/coalesced config restarts |
| frameworks/base | 4c9ed082169abc5dab5391eca7b3b3ffe3defae7 | Apply requested PIF IDs before generated-leaf signing |
| packages/apps/Settings | 31eae4cc1336dd3960acb9c14543df001dc1acf3 | Delegate PIF restarts to framework observer |

All have original contributor credit and fuzailmansuri porter identity. Eight Java/
Kotlin source/test parses, whitespace/hash checks and scoped preflight pass. Thirteen
Android regressions remain unexecuted; source compilation and installed behavior are
pending. Source activation preserved backup/pre-pif-consistency-20261109 in both
projects and changed no running evox build inputs (none was active).

Fresh runtime: missing profile restored, all labels still absent, imported Duck
intermediate still unlocked/orange, RSA-with-EC issuance verified. Provider experiment
restored, probe alias deleted and probe jars removed. Exact server rejection remains
unknown. Reports: porting/audit/tokay-integrity-runtime.md and
tokay-integrity-live-20261109.json, tokay-pif-*-verification.json,
tokay-pif-source-activation.json.

## Tokay confidence validation (2026-11-09)

The [readiness audit](porting/audit/tokay-confidence-readiness.md) verifies 133
Tokay files against recorded hashes and active commits in 16 projects. Scoped
preflight and nine host evidence-collector tests pass. There are no new source
commits in this check; the existing publication-map revisions remain active.
Compilation, Android regressions and hardware acceptance remain pending. Both
checked ADB endpoints reset the protocol; no fresh STRONG result was obtained.

## Allocator header and host-test availability (2026-11-09)

Project: external/hardened_malloc. Active/published commit:
[f09ff6a](https://github.com/fruity-lineage/hardened_malloc/commit/f09ff6af6ec9805b24886623fec7a540b192d1c9).
Parent: 8fd6c6016ef53cc97ee5bc6f521cf70859342e37. The two-file correction supplies
product/vendor header variants, APEX availability and inherited minimum SDK,
and disables the unsupported Windows HMallocTest variant. Existing history and
credits are preserved; the new commit uses the user's identity and malloc: subject.

The exact Tokay Soong graph-generation action succeeds. Generated targets retain
Linux HMallocTest and arm64 memtag_test; Windows HMallocTest is absent. GitHub main
commit/tree match the clean active project. The two new file hashes supersede the
earlier allocator snapshot entries for these paths. Full compilation and hardware
validation remain pending. See [verification](porting/audit/hardened-malloc-soong-availability.json).
