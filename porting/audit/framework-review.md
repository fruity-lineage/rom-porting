# Framework port review

This is the reviewer snapshot before final integration. The port is now committed;
see [verification.md](verification.md) for subsequent corrections, checks and limitations.

Reviewed 2026-11-08, LineageOS 24 / Android 17, Tokay. Project: `frameworks/base`,
branch `port/evolution-spoofing`; target base `7c7188f8585e20c035eb43fed72df5e717614b38`.
Work remains uncommitted for the parent agent to validate and commit. No builds or test
execution were performed by this reviewer.

## Sources and provenance

Framework content is pinned to Evolution-X/frameworks_base
`ddce89c4142f89e85830bf3cd2980cf7f472f705` (`evolution-port/cnb` locally).
The Settings-value subset was relocated from Evolution-X/vendor_extras
`1a97709e05739e0d4b05b37583a01eaa4df7cac8`, `sdk/ax_sandbox/{common,server}/src`.
`framework-feature-history.json` records checked path histories and authors.

Relevant source commits:

| Source commit | Behavior | Original author |
| --- | --- | --- |
| [afc187acf2791fb989a9471780c46cc21586f990](https://github.com/Evolution-X/frameworks_base/commit/afc187acf2791fb989a9471780c46cc21586f990) | Original PIF hooks, including platform signature in PackageManager | rmp22 <195054967+rmp22@users.noreply.github.com> |
| [5d0749b93bacc19b049c3b3adb322e9c8eda5ebd](https://github.com/Evolution-X/frameworks_base/commit/5d0749b93bacc19b049c3b3adb322e9c8eda5ebd) | ROM/root package filter and launcher exemption | rmp22 <195054967+rmp22@users.noreply.github.com> |
| [9937b3386ca84ed115d8eeebd0f6003ef76c0c18](https://github.com/Evolution-X/frameworks_base/commit/9937b3386ca84ed115d8eeebd0f6003ef76c0c18) | Core-UID hiding, resolver guards, shared-user enumeration filtering | Pranav Vashi <neobuddy89@gmail.com> |
| [d9c14c420da011ab5c504ef9af404f21768a0f5b](https://github.com/Evolution-X/frameworks_base/commit/d9c14c420da011ab5c504ef9af404f21768a0f5b) | Aurora-only installer reporting | Vincent Vidal <vincent@vidal.pm> |
| [cfc61294374887d034c509b2efd8b0818d049b18](https://github.com/Evolution-X/frameworks_base/commit/cfc61294374887d034c509b2efd8b0818d049b18) | Aurora/FakeStore/PlayStore server installer metadata | Oliver Scott <olivercscott@gmail.com>, coauthors in original message |
| [9cc141509ce7907bee153c72ea2ab9b8050f7103](https://github.com/Evolution-X/vendor_extras/commit/9cc141509ce7907bee153c72ea2ab9b8050f7103) | SDK migration supplying the Settings-value repository/service/client/storage subset | rmp22 <195054967+rmp22@users.noreply.github.com> |

PIF history also includes the numeric CANARY release fix `a6cac1b5`, static-final Build
write fix `cbcf722e`, early-load retry/logging `417d5b0d`, native staging refresh
`fae99b93`, TrickyStore/PIF fixes `0dc95b52`, and package namespace move `2143bd58`.
These are reflected in the pinned imported helpers; do not replace them with the initial
PIF commit alone. Duck's connected framework history is separately recorded in
`duck-framework-history.json` (`cc7c326c`, `45cccc16`, `3d18d8eb`, `f5f6a391`).

## Completed review changes

- Ported ROM/root package rules in AppsFilterBase, including `lineageos.platform` on a
  core UID. Filtering precedes the cached visibility/core-target exemptions. Core
  callers, privileged/system apps, privileged shared users and current default launchers
  retain access. Same-app access is preserved in both ordinary filtering and resolver
  helpers; the resolver exemption fixes a missing same-app check in upstream.
- Added `Computer.getDefaultHome`, using the current role provider instead of the
  upstream snapshot-local cache. This avoids retaining an obsolete launcher exemption
  after a role change. No new lock is taken across the role query.
- Added explicit activity, package-restricted activity, post-resolution and shared-user
  enumeration guards. Package filtering remains coordinated with stock instant-app and
  cross-profile behavior.
- Reloaded the system_server PIF parser on configuration change/clear. PackageManager
  otherwise kept old signature-spoof flags after UI edits despite the JSON cache changing.
- Added platform signature metadata for exact GMS callers only, conditional on PIF's
  `spoofSignature` setting. Legacy and modern signature fields respect requested flags,
  and both are prepared before assignment. LineageOS microG signature handling remains.
- Completed server Aurora installer reporting alongside the existing client hook.
  The upstream null dereference is avoided; the Play package must be installed for the
  queried user before the broader Aurora Services/FakeStore substitution is used.
- Reviewed the Settings-value Binder path: writes/read-management require
  WRITE_SECURE_SETTINGS and resolved user access; setters reject package suffix injection
  and unsupported settings; direct spoof-read callers must own the package and user.
  SettingsProvider validates its package before forwarding as system UID.
- Added `resetSandboxSpoofSettings(userId)` / `AxSettingsSpoofManager.resetSpoofSettings`.
  Only matching user entries are removed. After successful persistence AMS force-stops
  affected apps outside repository locks to discard app-side Settings caches. Settings
  UI integrates it with Pixel target/model reset while preserving enable toggles/keyboxes.
- Settings repository reads and reload publication are synchronized. Saving failures
  surface through Binder and reload the persisted map instead of retaining an unsaved
  in-memory selection. Unsupported stored setting names are discarded. JSON storage
  preserves other config sections. Fixed save indentation.
- Initialized the Settings repository before publishing the service, made factory
  publication volatile/idempotent, and removed unused AMS/WMS/PM injection surface from
  this deliberately scoped service subset.
- Added class-level `@hide` to PixelDeviceRepository; checked imported public Android
  helper classes for SDK visibility. Their process-sensitive state remains excluded
  through the preloaded-class denylist.
- Boot hash probes now run only in system_server. Boot-state persistence already used
  system-only writes and private DAC modes; reads now use AtomicFile recovery semantics.
  No app access to private system boot-state files is required.
- Restricted diagnostic revocation-cache file reads/writes to system_server. Hooked apps
  retain live diagnostic checks; no app SELinux access is needed for this private cache.
  The diagnostic HTTP input stream/connection now close on success, early return or error.

## Deliberately excluded unrelated changes

The full AxSandbox package-detach, arbitrary package hiding, app-lock and installation
source controls are separate product features with unported service dependencies. Their
ComputerEngine changes were not copied. Only the Settings-value SDK subset is imported.
The AssetManager change in `5d0749b9` merely renames a local constant with the same APK
path, so it is not a behavior dependency. The cache allocation/boot chunking changes in
`e8cd9edf` and AppsFilterImpl are separate memory tuning, not spoofing requirements.

## Validation and remaining work

Passed `git diff --check` after final edits, including whitespace normalization for new
Java/AIDL/BP imports. Static declaration checks found all 15 selected spoof/Duck Binder
methods implemented in AMS, and all imported public android.* helper classes have
class-level `@hide`. Scoped skill preflight on `services/duck_rkp` returned 0 errors and
0 warnings; it contains no PRODUCT_PACKAGES and this result does not establish Android
build or policy success.

Added three regression cases to PackageManagerServiceServerTests/AppsFilterImplTest:
core-UID ROM hiding before cache access, hidden-app self-resolution, and current-user
launcher exemption removal after a role change. These tests have not been executed.

Parent must run scoped framework/Settings/AIDL/API validation and meaningful Android
unit tests after all shared edits settle. External BouncyCastle EC/ECDSA provider
registrations are a confirmed transitive requirement for CertificateGenerator and
KeyBoxManager and are being ported by the parent. The source providers are intentionally
retained rather than silently substituted.

Tokay's Trusty/Citadel external-key signing remains a separate firmware capability
investigation. These framework changes retain the capability gate. They do not establish
hardware-backed Duck signing on Tokay or prove remote integrity acceptance.

Settings-value UI excludes com.android.*, com.google.android.* and android, matching
provider exemptions. Main reset restores built-in Pixel profile/targets but preserves
feature enable toggles, keyboxes and other users' Settings-value selections.

## Suggested logical commit groups

1. Portable Pixel/GameProps/PIF entry points and package-feature reporting, including
   constants, internal helpers and process preload exclusions.
2. TrickyStore keybox/attestation plumbing, keystore hooks and system-owned boot state.
3. ROM/root package visibility and Aurora installer reporting, with PM regressions.
4. Settings-value service subset, permission-checked Binder APIs and provider interception.
5. Duck RKP state/provisioning/AIDL integration, preserving the Tokay capability gate.

Factory/SystemServer/AMS wiring and shared constants may need staged hunks across groups;
keep dependencies in order. A single coherent framework feature commit is also reasonable
if splitting would leave intermediate commits uncompilable. Preserve upstream author
credit and source URLs plus porter trailers according to workspace skills. Root agent
owns commits and final validation results.
