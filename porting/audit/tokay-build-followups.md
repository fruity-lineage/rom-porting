# Tokay build fixes and output verification

Verified 2026-11-08 UTC after the user reported build fixes. The user's Android 17
build produced `out/target/product/tokay/lineage-24.0-20261108-UNOFFICIAL-tokay.zip`.
It is 1,705,536,749 bytes; SHA-256 is
`55f7a4cec8e04562628351d9c685159a864b4d77470aad320a521129d1c86852`.
ZIP CRC verification passes. Embedded metadata declares Tokay, SDK 37 and the
2026-11-01 security patch level.

## Fixes and provenance

| Project | Build failure and correction | Published main commit |
| --- | --- | --- |
| device/google/caimito | Generic-system artifact requirement rejects device properties on system; place them on product | [2f7cc30](https://github.com/fruity-lineage/android_device_google_caimito/commit/2f7cc304134f77b3858da6e9d2390a5b22fbc467), already published |
| system/security | Callback expects anyhow::Error while keyblob-upgrade helpers require Keystore Error; specify the concrete callback result and remove premature anyhow context from import | [a39ce22](https://github.com/fruity-lineage/android_system_security/commit/a39ce2250d6ad58dcefa377bdd9e8465fd83e9c8) |
| packages/apps/Settings | Spoofing adapter imports an absent shared focus-ring helper; restore its actual Compose implementation | [233ff31](https://github.com/fruity-lineage/android_packages_apps_Settings/commit/233ff319af4e0eb8369b4f1a5f976b3205a591e9) |

The focus-ring file is byte-identical to Joey's
[upstream commit](https://github.com/Evolution-X/packages_apps_Settings/commit/3c0e5203a323c7d9a3e36e560be6196ee2a01b5c),
blob `ad97c8f1d3700450320ec9088bddcbdce65abb85`. The extracted dependency retains
Joey as author and fuzailmansuri as coauthor and committer. The Keystore follow-up
uses the user's identity and references the original published import change.

Only the two missing changes were appended to public main. No public history was
rewritten. Publication used isolated worktrees and verified exact GitHub blob, tree,
commit, parent and author identities through the Git data API. These shared fixes
also apply to the Frankel source stack; Frankel has no build result here.

## Source and artifact checks

The user's build fixes are present in amended local topic tips:

| Active project | Active commit | Tree equals public main |
| --- | --- | --- |
| system/security | 27c3ec5862429ce676e1a396a747caf7c4567da1 | Yes |
| packages/apps/Settings | 53030932d1aa4b763b77c5085b2430709048dbe0 | Yes |
| device/google/caimito | bf2174958d133abfd1f233dd559e019939d8f707 | Yes |

All 101 current snapshot files match public trees. Compared with the previous
100-file checkpoint, 99 hashes are unchanged; security_level.rs changed and the
widget helper was added. The active muzel checkout remains upstream, with its
device port preserved in the isolated worktree and public main.

Installed outputs include Keystore2, runtime libc, Settings and compiled vendor
policy. Settings' DEX contains `com.android.settings.widget.InsetFocusRingKt`.
Product build.prop contains `ro.lineage.duckrkp.trusty_import=true` and
`remote_provisioning.hostname=remoteprovisioning.googleapis.com`.
Selected artifact hashes and publication checks are in
[tokay-build-followup-verification.json](tokay-build-followup-verification.json);
the complete current feature-file checkpoint is
[verification-build-source-hashes.json](verification-build-source-hashes.json).

## Acceptance limits

The agent inspected the user's outputs and did not launch a build, invoke lunch,
switch active sources or apply manifest overlays. A complete source manifest was
not captured before the build, so this is build-output evidence rather than a
reproducible-build assertion. Signing-key identity and OTA signature verification
were not checked.

At this build-output checkpoint hardware behavior was unverified. The later
[live investigation](tokay-live-integrity-investigation.md) now verifies boot, ordinary
TEE signing, imported ATTEST_KEY issuance and its production CA path after the AVB fix.
Actual Play Integrity acceptance still fails; broader consumers remain unverified. The alternative
import adapter does not resolve the original external-key CSR transport. Added
Android/bionic tests and runtime Settings keyboard-focus checks remain unexecuted.
