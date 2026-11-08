# Settings spoofing port review

This is the reviewer snapshot before final integration. Settings is now committed;
see [verification.md](verification.md) for final checks and outstanding runtime validation.

Reviewed 2026-11-08 UTC. Scope: `packages/apps/Settings` on
`port/evolution-spoofing`. This review preserves the imported work and does not
commit, push, or build Android. Framework changes are owned by the separate
framework review.

## Source provenance and integration

- Evolver source: [Evolution-X/packages_apps_Evolver at
  17ba8bbbc530c305efcc3c102bbc9d6f97e99f4d](https://github.com/Evolution-X/packages_apps_Evolver/commit/17ba8bbbc530c305efcc3c102bbc9d6f97e99f4d).
  The imported spoofing screens live under
  `src/org/evolution/settings/fragments/miscellaneous` upstream and under
  `src/com/android/settings/spoof` locally. Keep upstream file notices and
  author attribution when making the port commit.
- Settings-value UI/backup reference: [Evolution-X/packages_apps_Sandbox at
  db3d493ae3bd988e3df682c81941867c0f81b5b2](https://github.com/Evolution-X/packages_apps_Sandbox/commit/db3d493ae3bd988e3df682c81941867c0f81b5b2),
  notably `src/com/android/axion/sandbox/io/BackupManager.kt`.
- Framework reference: [Evolution-X/frameworks_base at
  ddce89c4142f89e85830bf3cd2980cf7f472f705](https://github.com/Evolution-X/frameworks_base/commit/ddce89c4142f89e85830bf3cd2980cf7f472f705).
- The Settings System dashboard opens the spoofing hub. The hub/search XML and
  SettingsGateway register eight destinations: hub, PIF, TrickyStore,
  TrickyStore targets, Pixel profiles, Tensor targets, app/game profiles,
  and per-app Settings-value overrides.
- Settings already uses platform APIs and holds WRITE_SECURE_SETTINGS and
  FORCE_STOP_PACKAGES. Compose dependencies come through
  `Settings-core -> SpaPrivilegedLib -> SpaLib`; no `ax_compose` dependency is
  needed for these screens.
- The scrollbar copy supports Material 3 1.5.0-alpha16 using existing Compose
  foundation/UI 1.12.0-alpha01 APIs. Its AOSP notice and upstream-copy comment
  remain. Replace with the library API when the prebuilt supports it.

## Fixes completed in this review

- Settings-value controls now serialize writes/imports/exports, disable all
  relevant controls while loading or writing, cancel superseded refreshes,
  catch refresh/package-loading failures, and avoid detached-fragment toasts.
  Restored app selections are discarded if no longer in the installed picker.
- Settings-value backup import is capped at 1 MiB, supports Sandbox version 1,
  scopes writes to this user and installed eligible packages, validates all
  applicable entries before the first write, rejects duplicate entries and
  non-boolean values, and treats missing supported keys as false. Unrelated
  Sandbox fields are ignored. Known eight keys match the framework API.
- The Settings-value picker excludes `android`, `com.android.*`, and
  `com.google.android.*`, matching the target SettingsProvider exemptions.
- PIF, keybox, and target-list documents are read on IO dispatchers with 1 MiB
  limits. PIF normalization also runs on IO. Superseded document imports are
  refused if the stored value changed during the read/validation.
- TrickyStore remote reads are bounded: 1 MiB for roots/keybox, 8 MiB for the
  revocation list. An in-flight keybox download does not replace a newer
  imported/generated value or install after Duck was enabled.
- Hub reset now calls the new `AxSettingsSpoofManager.resetSpoofSettings(userId)`
  API to clear only this user's Settings-value selections. The framework
  implementation restarts affected apps after persistence.
- Hub reset also restores the default Pixel target/model configuration and
  restarts installed apps from the union of previous and default Pixel
  targets. The framework package is excluded; Settings itself is stopped last
  if explicitly targeted. Reset writes finish before these restarts.
- Reset runs off the UI thread, blocks duplicate reset requests, and shows
  errors. The confirmation describes the expanded reset while retaining
  keybox and enable toggles, including Photos/Snapchat.
- Added the omitted upstream `ts_added_installed_count` plural and replaced
  the missing dashboard drawable with Lineage's existing about-device icon.
  Removed an imported trailing-whitespace line.
- The unrecognized-root dialog now names the Google attestation roots used by
  its validator rather than claiming ROM-specific trust roots.

## Static validation

- Three changed/imported XML files parsed successfully.
- 296 resource references from all imported Kotlin/UI/XML paths resolve in
  Settings or the existing SettingsLib resources.
- All 244 imported default-value resource names are unique and do not
  collide with existing Settings default values.
- Eight destination classes exist and are registered in SettingsGateway.
- 179 Compose imports were matched against current prebuilt source archives;
  generated Material icon imports use the existing extended-icons dependency.
- 34 non-stock framework dependency symbols are present in the working tree,
  including KeyBoxManager, TrickyStoreService, PixelDeviceRepository,
  PixelPropsUtils, AxSettingsSpoofManager, and the Duck IActivityManager APIs.
- `ActivityManager.forceStopPackage()` delegates to the context's user ID;
  existing shared/PIF/TrickyStore restart calls retain correct current-user
  scope. Duck's device-wide restart helper explicitly uses USER_SYSTEM.
- Tracked changes pass `git diff --check`. The 18 imported/untracked files
  were also checked for trailing whitespace and merge conflict markers.

These are source and resource checks, not compiler, instrumentation, device,
network-service, attestation, or SELinux validation. Parent work owns scoped
build validation and clean commits.

## Remaining runtime checks and limits

- Exercise app switching during refresh, imports/exports, rotation/back
  navigation during IO, service failure, and a removed saved app.
- Exercise valid Sandbox backups; malformed late entries; non-boolean values;
  unknown versions; duplicate app entries; missing keys; oversized files;
  secondary-user records; and uninstalled/exempt packages. Parse failures must
  leave all app settings unchanged.
- Import writes use individual Binder setters. A service/persistence failure
  after successful parsing can still leave a partial import; there is no
  batch transaction API. The UI reports the error and reloads actual state.
- Hub reset spans several settings and a Binder operation, so a service or
  provider failure can leave a partial reset. Verify persistence and affected
  app restarts with the final framework implementation.
- Verify document-provider failures and concurrent edits/downloads do not
  replace newer settings, and check chosen remote limits against live data.
- No Trusty external-key signing backend or Tokay hardware success has been
  demonstrated. Duck UI remains gated by framework `available`, restricts
  actions to the owner, respects busy/imported/retry states, and maps errors.
  No Qualcomm requirement was relabeled as Tokay support. Tensor targets
  remain hidden on Tensor Pixels, and Pixel identity spoofing retains the
  framework's mainline-Pixel exclusion.

Suggested commit grouping: one attributed Settings integration commit for the
imported screens/resources/navigation and one follow-up for IO/lifecycle,
backup validation, and expanded reset behavior. The first integration depends
on the matching framework APIs; the follow-up also depends on the per-user
reset API. No local commit hash exists from this review.
