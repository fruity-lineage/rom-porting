# Native, configuration and SELinux history audit

This is the reviewer snapshot before final integration. The provider dependency and
port commits are now complete; see [verification.md](verification.md) for final results.

Reviewed 2026-11-08 UTC against the recorded source pins. This is the child audit for
`bionic`, `vendor/lineage`, `system/core/init`, and `device/lineage/sepolicy`.
No Android builds, commits, pushes or publication were performed by this auditor.
The parent owns final integration, validation and commits.

## Result

- All 15 originally imported bionic feature files matched Evolution X
  `57ae6d98c1c1aec194cbe0cde12f55f6731e7523` byte-for-byte before the local follow-up below.
  This includes syscall renames, close/dup/fcntl metadata handling, the loader TLS fix,
  DroidGuard staging, overlay access fixes, canonical proc paths and stat metadata fallback.
- The actual `SYSCALLS.TXT` parser accepts all entries, produces six internal syscall
  entry points and no remaining generated public `fstat*`, `readlinkat` or `statx` entry points
  that would collide with the new C++ wrappers. The public symbols remain in `libc.map.txt`.
- All recently referenced STATX mask flags exist in the target Android 17 UAPI header;
  capture falls back to STATX_ALL if an older kernel rejects new bits.
- `libc_bionic` feeds `libc_common`, shared/static libc, and `libc_nomalloc` used by the
  linker. Caller-owned property buffers avoid loader ELF TLS. Internal filtering uses raw
  syscalls so public open/stat/property hooks do not recurse through themselves.
- SELinux staging wiring is complete: `system_internal_prop(pif_prop)`, typed prefix
  `persist.sys.pif.`, system_server write/read, gmscore_app read, and debug-only shell read.
  **The GMS rule is an untracked file**, `common/private/gmscore_app.te`; it must be staged
  when committing. It was not missing merely because ordinary `git diff` omitted it.
- Target gmscore_app is coredomain; the `com.google.android.gms.*` seapp rule includes
  `com.google.android.gms.unstable`. Its read does not conflict with the internal-system
  property neverallow. No broad app reads or GMS property writes were added.
- `AxSpoofManager` and bionic agree on product/build staging keys, generic property slot
  prefix, exact-before-wildcard ordering and the 32-slot limit.
- Optional `SPOOF_FIRST_API_LEVEL_32` is wired through vendor Soong defaults and init,
  is **unset for Tokay**, and leaves its shipping API 34 intact. The optional override is
  inserted before read-only publication and skipped in recovery.

## Concrete local correction

The upstream `filter_readonly_file()` dereferenced `path[0]` before checking the app
process gate or its low-address guard. Consequently `open((char*)1, O_RDONLY)` could crash
before the kernel returned EFAULT, including in non-app processes.

Changed `libc/bionic/open.cpp` to reject low addresses before dereference and exit before
path inspection when filtering does not apply. Moved `is_app_process()` before the path
inspection in `custom_rom_hide_should_block()` as well. Added
`tests/fcntl_test.cpp: open_invalid_path_pointer`, covering open/open64/openat/openat64.

This is a follow-up to upstream, not part of the identical import. The test has **not
been compiled or executed**. These guards do not solve arbitrary unmapped pointers in
app contexts; pre-syscall pathname inspection remains an upstream limitation.

## Required transitive dependency found outside edit ownership

`external/bouncycastle` needs the EC provider registration port. This was missed by the
initial feature-keyword inventory because the diff contains provider registrations but no
spoofing keyword.

Target `repackaged_platform/bcprov/src/main/java/com/android/internal/org/bouncycastle/jcajce/provider/asymmetric/EC.java`
comments out EC factories/generators and SHA256withECDSA. Imported `CertificateGenerator`
explicitly selects a new `BouncyCastleProvider` for EC issuer signatures. `KeyBoxManager`
also selects that provider to verify imported EC keybox signing pairs. These calls otherwise
fail with a provider/algorithm error despite a successful framework compile.

- Introduction: [e75ae35c6171](https://github.com/Evolution-X/external_bouncycastle/commit/e75ae35c6171d391613a675bde54561965eefb1f),
  Abhay Singh Gill `<abhaygill017@gmail.com>`.
- Required follow-up/current source: [56e5dac75158](https://github.com/Evolution-X/external_bouncycastle/commit/56e5dac751581c7bd6dbe363d7ba3f8e8862c5bf),
  rmp22 `<195054967+rmp22@users.noreply.github.com>`; signed off by Dmitrii.
- Net target-to-current source: restore the EC/ECDSA/EC(DH/C) key factory registrations,
  EC/ECDSA generators and SHA256withECDSA registration while retaining the surrounding
  Android-disabled algorithms. The net diff is eight inserted lines.
- Verified blob/source file is available under `/tmp/native-extra-sources/external_bouncycastle/`.
  Full original author metadata and patches are retained in `native-upstream-commits.json`.
  The parent was notified to make a separate project commit. This auditor did not modify it.

## Source history and dependencies

`native-config-path-history.json`, `native-extra-path-history.json` and
`native-bouncycastle-history.json` preserve pinned path histories. `native-upstream-commits.json`
contains actual single-commit patches, parents, URLs and original author metadata. No large
Git histories were fetched. Histories returning 100 commits are bounded and do not imply
complete ancient AOSP history; the feature introductions and relevant follow-ups are included.

The bionic import is the accumulated current implementation, not a fresh cherry-pick of the
initial hook. In particular, do not revive the old dynamic ELF TLS buffer, recovery hiding,
config-file allowlists, direct overlay-open blocking, or the old faccessat error-order regression.

### Bionic introduction and fixes

| Commit | Upstream change | Original author |
| --- | --- | --- |
| [3514d83d74e6](https://github.com/Evolution-X/bionic/commit/3514d83d74e6d6483d533c391cf0c7adc19cd5c1) | Add hooks for custom rom hide | rmp22 |
| [102b320256b0](https://github.com/Evolution-X/bionic/commit/102b320256b07bccbed0a1a14db7c19bcef32379) | custom_rom_hide: hide VINTF names | Dmitrii |
| [7668573fc9f4](https://github.com/Evolution-X/bionic/commit/7668573fc9f4a287291ab6911ab86a0f769798e0) | fixing adb service spoofing | rmp22 |
| [35b13b591f48](https://github.com/Evolution-X/bionic/commit/35b13b591f48aff41d468e47ef03063302c7cf2e) | custom_rom_hide: guard against invalid pointer args across all entry points | Dmitrii |
| [c7047aad5276](https://github.com/Evolution-X/bionic/commit/c7047aad5276252f19768e16e696e9dae7d5ec8e) | custom_rom_hide: improve spoofing | shutter-cat |
| [f0ff168ea7e3](https://github.com/Evolution-X/bionic/commit/f0ff168ea7e3996e8dfa8c2ea93a1c879ac713b2) | custom_rom_hide: fix potential crashes from invalid pointer dereferences | Joey |
| [68e2b8d2c256](https://github.com/Evolution-X/bionic/commit/68e2b8d2c256688958d06d4747367b2aae82bfd4) | custom_rom_hide: Fixing adb root hiding | rmp22 |
| [b7c7cdc2d0e1](https://github.com/Evolution-X/bionic/commit/b7c7cdc2d0e1ef59b1249a50c6da7fb89f00cec3) | custom_rom_hide: Remove recovery paths | Pranav Vashi |
| [e81d19e883d4](https://github.com/Evolution-X/bionic/commit/e81d19e883d4d54b95c72a4b8c71ea01cf3ff88f) | hardcoding custom rom hide app white list | rmp22 |
| [a060f6ca4de7](https://github.com/Evolution-X/bionic/commit/a060f6ca4de70c0a22cf0becf1fd8e87dbad1593) | custom_rom_hide: additional intercepts | rmp22 |
| [9b0480adcae4](https://github.com/Evolution-X/bionic/commit/9b0480adcae45933ccb5ef1d63c5a6e0e068cdd6) | spoofing improvements | shutter-cat |
| [72b62665f67c](https://github.com/Evolution-X/bionic/commit/72b62665f67c160456bd028ba00e4f916ae9db1f) | bionic: custom_rom_hide: perf pass | Dmitrii |
| [df6d4284bddd](https://github.com/Evolution-X/bionic/commit/df6d4284bdddf06dea75336cb9ed3b8100453e3c) | bionic: fix regressions | Dmitrii |
| [7ba6adb9329e](https://github.com/Evolution-X/bionic/commit/7ba6adb9329eb5dfafd9d90e5e800e1b239493d2) | [bugfix] fixing custom rom hide sysprop | crash issues | rmp22 |
| [0fe98e0d800a](https://github.com/Evolution-X/bionic/commit/0fe98e0d800a8d50e4a2e428f35c68d93f9c00c2) | custom_rom_hide: Mirror staged PIF product props | Joey |
| [1773bf1e1079](https://github.com/Evolution-X/bionic/commit/1773bf1e10796a0bd04a3ab4a5122a0921ac9bca) | bionic: Keep dynamic property overrides out of loader ELF TLS | johnmart19 |
| [859bb722ac77](https://github.com/Evolution-X/bionic/commit/859bb722ac77d5ec468ca0856c0e310d8752dd83) | custom_rom_hide: Serve PIF props to DroidGuard only | Joey |
| [cf6e2a93fe4a](https://github.com/Evolution-X/bionic/commit/cf6e2a93fe4a38d3ab76d99d6c01ef90398b9d8f) | custom_rom_hide: Serve build description, type and tags to DroidGuard | Joey |
| [fc6ec955259c](https://github.com/Evolution-X/bionic/commit/fc6ec955259cac19248ee332be94cea00377ff65) | custom_rom_hide: Fix custom rom artifacts detection | Pranav Vashi |
| [3d4169372eac](https://github.com/Evolution-X/bionic/commit/3d4169372eaccc2e1ebf5467e1da8bc1d0e31fca) | custom_rom_hide: Exempt zygotes for custom rom path | Pranav Vashi |
| [33095e6025fb](https://github.com/Evolution-X/bionic/commit/33095e6025fbe836ba24f89c8078bea5e31100fe) | custom_rom_hide: Hide ROM-named RRO overlays from apps | Pranav Vashi |
| [f8b37b8c5b5c](https://github.com/Evolution-X/bionic/commit/f8b37b8c5b5cdc7c69a01107fbbb56b2a8ae8420) | custom_rom_hide: Do not spoof /data/local/tmp | Pranav Vashi |
| [fff925319a38](https://github.com/Evolution-X/bionic/commit/fff925319a388a70cc5794e039cb6f23d90c8c1b) | custom_rom_hide: Only hide ROM-named overlays from listings | Quince |
| [6ec7500214a4](https://github.com/Evolution-X/bionic/commit/6ec7500214a43eef1e813e188aa8da42e1c6aeb5) | custom_rom_hide: Spoof st_dev for partition roots on fstat/statx | Pranav Vashi |
| [9ac5d72c4ebd](https://github.com/Evolution-X/bionic/commit/9ac5d72c4ebd450a01c550729e73cedcb0bc5724) | custom_rom_hide: Harden custom ROM hiding and improve filesystem handling | Pranav Vashi |
| [2c208d8ca219](https://github.com/Evolution-X/bionic/commit/2c208d8ca219ecbca9118487349742b03f42567e) | custom_rom_hide: Mask blocked paths and null-name reads consistently | Pranav Vashi |
| [553c077ee3d1](https://github.com/Evolution-X/bionic/commit/553c077ee3d1f5191883728e39c72fa73e400345) | custom_rom_hide: Keep substituting files opened with O_NOFOLLOW | Quince |
| [57ae6d98c1c1](https://github.com/Evolution-X/bionic/commit/57ae6d98c1c1aec194cbe0cde12f55f6731e7523) | custom_rom_hide: Preserve canonical proc paths for substituted files | Quince |

The property staging chain begins with framework
`fae99b931fd7573b921998597bc8b2ad06a21533` and bionic `0fe98e0d800a`.
`1773bf1e1079` removes its loader TLS regression. `859bb722ac77` scopes dynamic overrides
to finalized DroidGuard process names; `cf6e2a93fe4a` plus framework
`e8c40db31314eafb6ef0b41d8723b7484dee8a42` stage description/flavor/type/tags.
Policy `9803439b43b3970d66a88a96e045b91132dbb551` labels the complete staging prefix.

Legacy get/read property APIs intentionally apply fixed overrides; dynamic staging is served
by read_callback/serial. That matches current upstream and avoids re-entering dynamic lookup
when reading `persist.sys.pif.*`. No blanket API-consistency rewrite was made.

### Configuration and policy ports

| Source | Port decision |
| --- | --- |
| vendor `c038ebc877323ba8ba70c4d70de6305e3510839b` | Optional API-32 defaults ported with target `soong_config_set_bool`; feature remains unset on Tokay. |
| init `3e62fd208f81cda79d9b43a999881fdfc7cdb0e4` | Only the optional first-api effect adapted; set the map before read-only publication rather than depend on global override weakening. |
| policy `9803439b43b3970d66a88a96e045b91132dbb551` | Complete staging type/writer/reader rules ported. Explicit `prefix string` retained in target contexts. |
| vendor `d732f5cd1a983da525769570076470fc816b53f6` | Global Pixel Beta fingerprint override explicitly excludes Tokay in upstream; not applied. |
| policy `36a8e9c81315029b06cc4e763ded10eb6e9ba01f` | Legacy ro.product.fingerprint labeling for Qualcomm qtidataservices; no native consumer established on Tokay. |
| policy `f66548e3b14e25fdb4c9981387d4d9580ba06b2a` | Historical /data/adb → /data/system config migration. Current upstream removed those file types/rules and uses framework settings/Binder configuration. Do not import obsolete broad app reads. |

`AttestationUtils` still persists system-side boot fallbacks under `/data/system/tricky_store`
with system-only writes and central `getSystemBootState()` reads. It does not require the old
app-readable file policy. `TrickyStoreService` still has a logging-only revocation cache under
`/data/system/trickystore`; unprivileged processes cannot access it. The framework reviewer
was notified to gate file access rather than grant app-wide system-data access.

### Other upstream mechanisms inspected and deliberately excluded

These are actual spoof/history instances, not negative-search claims. Their current code and
relevant introducing/fixing patches were read and captured. They are independent global ROM
choices rather than prerequisites of the staged app process implementation.

| Area / commits | Current upstream effect | Reason excluded from this Tokay port |
| --- | --- | --- |
| init `c6d08cd4f334`, `bc4262ac9f12`, `8061efc37a92`, `95b9fe1ac479`, `6b0377ffb0b8`, `05dc6f5f18ab`, `58f6da70a9d9`, `786008410ada` | Globally rewrites boot/debug/type/encryption/warranty props. | Changes values seen by system services; bionic already supplies selected values to apps. |
| init `3a49ee85437f`, `5ffb7848c1f6` | Exempts ro.boot.vbmeta., persist.sys., logpersistd from property MAC checks, weakens read-only state; adds runtime debug/root toggle. | Dedicated pif_prop policy supplies the needed staging write without broad permission bypass. |
| init `c51ca391d870` | Generates fallback vbmeta digest from std::hash seed and supplies size fallback. | No evidence Tokay lacks its actual digest; a generated hash is not firmware-backed boot evidence. |
| init `f77168df7b3d`, `091ad8c95d1e` | Hide-adbd introduction and later revert. | The adbd fake state was reverted upstream; dynamic DroidGuard callback hiding remains in bionic. |
| init `06651c729df4` | Removes sys.oem_unlock_allowed override from global spoofing. | Preserve actual system value; import no older override. |
| init `8218c71ea862` | Drops persistent network-ADB enable at reboot. | A separate ADB policy change, not spoofing dependency. |
| init `ea0752d2d09c` | Checks native property update failure. | General correctness follow-up, not required by optional map insertion/staging writes; not mixed into this feature commit. |
| build `1e673c879370` | Forces non-eng partition build types to user. | Global debug identity change; app-scoped native overrides already participate. |
| build `724bab4e67e0`, Soong `960208aec456` | Unconditionally clamp product and board first API to 32. | Would contradict Tokay shipping API 34 and the intentionally unset compatibility option. |
| Soong `d8945eb052e0` | Uses DeviceName in flavor, description and product name instead of lineage_ product prefix. | Global generated identity choice; PIF staging supplies chosen identity to DroidGuard. |
| Soong `2b339acfa4e3` | Emits release-keys for non-test signing configuration. | Global signing metadata policy; no new signing keys or release identity established for this port. |
| Soong `f3f6ce6eb7a2`, `926a2697d9bf` | Synchronizes system fingerprint/description when only generic override exists. | Global fingerprint override is excluded for Tokay upstream; no needed override introduced here. |
| Soong `89adce50baa4` | Appcompat green verifiedbootstate on non-eng builds. | Independent global property-area override; native app scope already covers the selected boot values. |
| Soong `f3d75d0edb13`, `d23dc673b8dd` | Disables debug/checkjni defaults. | General runtime debug behavior; not a feature dependency. |
| build `5376b6d4acbd` | Raises non-ro property length check from 91 to 120. | Native PROP_VALUE_MAX remains 92 bytes; not a sound prerequisite. Read-only props already permit long values in AOSP. |
| fs_mgr `b254041abb41`, `419432cc6bde` | Removes remount bootloader-state check. | Staged app-only spoofing leaves fs_mgr real state unchanged. |
| libfs_avb `dbc7c2e5f04d`, `0472f120038c` | Optional FASTBOOT_BYPASS_LOCK_STATE permits green for Fenrir-patched LK. | Qualcomm/legacy bootloader option, no Tokay trusted backend established. |

## Broader source coverage

Full pinned local trees for native/AV/libcore/SDK/LineageParts/system policy were searched
with both exact feature terms and generic spoof terms. Generic matches in native/AV/libcore
are byte-identical to target; the others have no generic spoof match. This is recorded in
`native-negative-coverage.json`.

| Project | Pin | Exact feature matches | Generic spoof files |
| --- | --- | --- | --- |
| frameworks_native | `cb8303a432fc2eb4ea3bf57ec450501e18f2cced` | 0 | 1 |
| frameworks_av | `2dc99a751a66141e3b5a24ae53fee412cb29a3ff` | 0 | 2 |
| libcore | `45606a215025ddad56fbb088fc1f0124ffc82413` | 0 | 2 |
| lineage-sdk | `a870f420bd1495160c83e0dcf0309c2a366b196f` | 0 | 0 |
| packages_apps_LineageParts | `21f90730a8de06e9275e82e270a5808503a2c296` | 0 | 0 |
| system_sepolicy | `dd9d56abe0590484ae145337ae1e728db9b2d57a` | 0 | 0 |

Additional complete API trees were compared by blob identity to the target. Only differing
text files were downloaded for existing target projects; vendor config sources and small
historical app/config text were inspected separately. 332 downloaded text blobs match their
recorded Git blob hashes. Changed-line searches alone were insufficient: the EC provider
registration and global build properties above required targeted reads of the whole diffs.
Coverage and source URLs are recorded in `native-extra-tree-coverage.json` and
`native-extra-content-review.json`.

| Additional source | Pin | Total blobs | Target differing blobs |
| --- | --- | --- | --- |
| build | `75f33f854b8f750c46b5fd666457cea5c3636a65` | 1680 | 20 |
| build_soong | `541d7c2ccbb7c6cfdf370da58314a8dd03607a5f` | 1482 | 20 |
| external_bouncycastle | `56e5dac751581c7bd6dbe363d7ba3f8e8862c5bf` | 3048 | 1 |
| hardware_google_pixel | `8e3a91851a182c6be19cd9d8809ec636b77e179e` | 361 | 3 |
| hardware_interfaces | `c626eb9ba04891cb0f7248251b84bd7fbd4afcf2` | 18093 | 33 |
| system_fs_fs_mgr | `0472f120038c831c27eed7fbd3745131ce18a74c` | 290 | 4 |
| vendor_gms | `e059bf57756d7d8e814cd152b13d4d51a9e0bb9e` | 416 | no target project |
| vendor_gms-mosey | `931dc880a8f4c76b6a55a37cf53b7fd449094e24` | 13 | no target project |
| packages_apps_Pif | `fc1a93ac0a9657aea358f8fd61bed4305eebbad2` | 8 | no target project |
| vendor_certification | `91bbc30a9457a0b7b805b2883aec8718380cfe47` | 4 | no target project |

- hardware/interfaces has no changed KeyMint/RKP files and no Duck AIDL addition; the
  changed interfaces are audio, camera, light, health, Wi-Fi and compatibility matrices.
- hardware/google/pixel changes only thermal helper/watcher code.
- Current vendor/gms config text has no Duck/TrickyStore/PIF/custom ROM hiding implementation.
  Standard GMS prebuilts are runtime consumers, not spoofing service sources. This audit did
  not reverse engineer the full proprietary GMS APK set. The current LineageOS device/vendor
  configs do not inherit vendor/gms; installed GMS availability is a separate runtime prerequisite.
- vendor/gms-mosey supplies a QuickShareExtension IMoseyService, with optional inclusion false
  by default; no caller from the spoofing stack was found.
- Archived `packages_apps_Pif` (vic) is the old PixelPropsUtils/PPU_SPOOF_BUILD_GMS_ARRAY
  fingerprint UI, initialized by `fc1a93ac0a96`. It is absent from active cnb manifest, whose
  new UI lives in Evolver and was adapted by the Settings reviewer.
- Archived `vendor_certification` (vic) only ships PifPrebuilt APK and product inclusion.
  It is absent from cnb manifest; no current source dependency references it. Its 33-commit
  update history was recorded; the APK was not loaded or imported.
- vendor/extras `9cc141509ce7907bee153c72ea2ab9b8050f7103` migrates the Sandbox SDK.
  Relevant AxSettingsSpoofManager, SettingsSpoofService and SettingsSpoofRepository now
  participate in the framework/Settings port. The broad sandbox isolation/vault/app-lock
  implementation is not required merely to spoof selected settings values.

This establishes bounded evidence for the named repositories. It does not assert that every
file in all 101 organization repositories or all historical branches has been exhaustively
reverse engineered. Dormant historical code and proprietary runtime checks remain separate
from the connected active source port.

## Validation and commit grouping

Completed locally:

- `git diff --check` in bionic, vendor/lineage and device/lineage/sepolicy, and scoped to init
  in system/core: pass.
- `SysCallsTxtParser.parse_file('bionic/libc/SYSCALLS.TXT')`: pass; six renamed entry points
  with LP32/LP64 mapping and no duplicate generated public wrappers.
- Cherry-picking skill static preflight scoped to device/lineage/sepolicy with module dirs
  vendor/lineage, bionic and system/core/init: **0 errors, 0 warnings**. This is a static
  checker and not full compiled SELinux or Soong validation.
- Relevant definitions, masks, loader linkage, property read recursion, process gates,
  source blob identities, policy domains and first-API config checked by inspection.

Pending parent validation: compilation/linking, compiled SELinux neverallows, execution of
`fcntl.open_invalid_path_pointer`, native callback/property/FD lifecycle tests, Settings
integration, and all Tokay hardware behavior. This auditor claims no hardware attestation
success and no supported external-key signing backend in Tokay Trusty.

Recommended clean local groups, preserving upstream author credit:

1. bionic accumulated hook/property import at `57ae6d98c1c1`, retaining all copyright notices
   and citing the original introduction plus important fixes/co-authors from the table.
2. bionic local pathname guard regression follow-up with the new fcntl regression test.
3. vendor/lineage optional API-level Soong defaults (`c038ebc87732`, AnierinB).
4. system/core init optional map-before-publication adaptation (`3e62fd208f81`, AnierinB).
5. device/lineage/sepolicy staging property access (`9803439b43b3`, Joey), including untracked
   gmscore_app.te. No obsolete file types or broad GMS/system property grants.
6. external/bouncycastle EC provider dependency, citing `e75ae35c6171` and `56e5dac75158`.

The parent's commit record in spoofing-inventory.md should distinguish the static passes
above from pending compiled/runtime checks. No commit hashes exist for these groups yet.
