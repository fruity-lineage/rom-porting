# Evolution X spoofing and Duck RKP port inventory

Updated 2026-11-08 UTC after the Tokay import-attestation source commits.

Targets: LineageOS lineage-24.0 / Android 17, Pixel 9 (tokay, zumapro) and
Pixel 10 (frankel, laguna).
Source: [Evolution X repositories](https://github.com/orgs/Evolution-X/repositories),
active cnb sources and the supplied device commits.

Fifteen source commits cover the shared stack and device import configuration. Static checks pass with
the qualifications in [verification.md](porting/audit/verification.md). Tokay Duck signing,
Android compilation, compiled policy and device behavior remain unverified.

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

Evolution vendor coverage: vendor/lineage contains the optional API-32 Soong change.
The audited global Pixel Beta fingerprint override explicitly excludes Tokay upstream
and was not applied. No separate Duck signing daemon was found in vendor_evolution.
The import adapter uses the existing Trusty HAL selected by the shared device product.

## Published forks

All ten forks are public under fruity-lineage, with verified main tips and default
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
| frameworks/base | [android_frameworks_base](https://github.com/fruity-lineage/android_frameworks_base/commit/474ebc595d120aa3025f6ec0e95acb9a2112e85e) |
| packages/apps/Settings | [android_packages_apps_Settings](https://github.com/fruity-lineage/android_packages_apps_Settings/commit/19a7e7263ff77194412e7aff729ab3d9b924e6b3) |
| system/security | [android_system_security](https://github.com/fruity-lineage/android_system_security/commit/52f9343c51950fcb5b10d0e485c7f044250cdc93) |
| device/google/caimito | [android_device_google_caimito](https://github.com/fruity-lineage/android_device_google_caimito/commit/2f7cc304134f77b3858da6e9d2390a5b22fbc467) |
| device/google/muzel | [android_device_google_muzel](https://github.com/fruity-lineage/android_device_google_muzel/commit/9c4bad6692c8275790bff334263914ddbd2a59e5) |

Bouncy Castle is a fork of Evolution-X/external_bouncycastle, which contains the
verified Android 17 base. LineageOS's GitHub Bouncy Castle mirror stops at older
Android branches. The other nine forks use their corresponding LineageOS parents.

[publication-commits.json](porting/audit/publication-commits.json) maps all fifteen local
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
  attribution were checked. The current active caimito property edit is preserved.
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
  were published from isolated worktrees; 100 combined snapshot hashes pass. The active
  Tokay edit is preserved, and the active muzel checkout is unchanged.

These checks do not establish Java/Kotlin type checking, native linking, compiled policy,
hardware signing or remote acceptance. Android/bionic tests remain unexecuted. C++ parser
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
RKPD import gap fixed and the existing service/init/VINTF/policy traced. Production CA
constraints, firmware import support and consumer behavior remain unverified. It adds
an imported CA, not direct external-key CSR certification. See
[tokay-duck-import.md](porting/audit/tokay-duck-import.md) and
[tokay-duck-import-verification.json](porting/audit/tokay-duck-import-verification.json).
