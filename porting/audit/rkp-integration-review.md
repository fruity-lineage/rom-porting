# RKP integration review and follow-up fixes

Reviewed on 2026-11-08–09 UTC with three subagents. The documented standard Trusty
import route has no missing dependency identified by this bounded review. The
obsolete Qualcomm-only generation description is corrected and published. Actual
Play Integrity acceptance remains unresolved. The renewal failure classification
is also corrected, with a boot-resume follow-up. These new source changes have not
been rebuilt or tested on hardware.

## Source change

Project: `packages/apps/Settings`.
Commit: [0a2e3c2](https://github.com/fruity-lineage/android_packages_apps_Settings/commit/0a2e3c2c7dd19611e2e0a131c7530573ed59fc1c).
Parent: `233ff319af4e0eb8369b4f1a5f976b3205a591e9`.

`res/values/spoofing.xml`, resource `ts_rkp_provision_summary`, now reads:

> Request a replacement now, or retry paused automatic provisioning.

The removed sentence required compatible Qualcomm firmware. Settings already uses
the backend's availability result to show and enable the generation action:

- `src/com/android/settings/spoof/TrickyStore.kt`: `applyDuckRkpState()` derives
  support/availability from the returned state and combines owner, enabled,
  imported-keybox, busy and cooldown conditions for generation.
- `src/com/android/settings/spoof/TrickyStoreContent.kt`: consumes the summary in
  the generation row inside the supported-backend section.
- `frameworks/base/services/core/java/com/android/server/security/rkp/DuckRkpManager.java`:
  `backendAvailable()` selects the enabled Trusty import adapter; its corresponding
  `supportsBackend()` path uses adapter availability independently of manufacturer.

This is a resource-text correction. Provisioning, certificate processing, actual
boot claims and integrity requests were not changed. The new text has not been
rebuilt or exercised on hardware.

XML parsing passes, all 244 resource names are preserved, exactly one resource text
changed, its existing caller resolves, and commit whitespace passes. The author
and committer are the user's configured identity, with sign-off and references
to the earlier Settings port and framework adapter. Original authors remain in
parent history. Publication verifies identical commit, tree and blob in the
controlled LineageOS fork, with a fast-forward update to default branch `main`.

## Recoverable import failure handling

Framework commit [60153c1](https://github.com/fruity-lineage/android_frameworks_base/commit/60153c127470c3855d4e979a4b60190f6b13bdf5)
fixes a renewal fault: the Trusty adapter previously translated every Keystore
exception to permanent `hal_rejected`, pausing automatic provisioning even when
the RKP key pool was temporarily unavailable.

The adapter now translates documented pre-import pending connectivity (24) to
`network_error`, and transient key exhaustion (25) or backend busy (18) to
`hal_unavailable`. The existing manager supplies validated-network gating and
capped backoff. Update/reboot-required, permanent and ambiguous hardware failures
remain paused. If temporary-alias cleanup fails after a recoverable import error,
`save_failed` takes precedence and prevents retries, retaining the original
error as suppressed diagnostics. Permanent primary errors retain their precedence.

Five focused Android regressions cover eligible/excluded status codes and cleanup
precedence. Java syntax/API/dependency inspection, whitespace and independent peer
review pass. The Android regressions and live renewal fault injection remain
unexecuted. No cancellation, certificate, settings-target or attestation-claim
processing changed.

Syntax validation uses Python 3.12.3, tree-sitter 0.26.0 and tree-sitter-java 0.23.5
from `/tmp/tokay-spoofing-parsers`. Parse both changed Java sources with
`Parser(Language(tree_sitter_java.language()))` and require `not root.has_error`.
Parsing does not establish compilation or Android test execution.

## Boot restoration and generation

Framework commit [4755e22](https://github.com/fruity-lineage/android_frameworks_base/commit/4755e2231cf2ccc5617b310a1fb28583e6cb2f89)
repairs persisted-state recovery across an upgrade. Earlier Trusty imports could
store a permanent `hal_rejected` pause for the temporary statuses 24/25/18.
Startup now migrates only those known states, retaining details/failure count and
later deadlines, applying existing backoff and persisting recovery. Native legacy
recovery cannot override the selected Trusty backend.

An eager Keystore2 binder precheck runs before local key generation, alias work or
import. Its absence safely returns retryable `hal_unavailable`. Lazy KeyMint/RKP
lookup remains intact, and errors after import retain their previous safeguards.
Permanent, cleanup, unknown and update/reboot-required failures stay paused.

The existing SystemServer/factory → AMS/systemReady → Duck construction/load →
network/alarm scheduling path already restores and schedules without opening
Settings. The change preserves disabled/master/manual-keybox gates. Four added
persisted-state tests cover migration, backoff, deadlines and excluded failures.
Peer review, Java parsing/API inspection and whitespace pass; Android execution
and the new cold-boot/OTA behavior remain unverified on hardware.

After building/installing the published revisions, verify boot without opening
Settings, restored valid-key availability, replacement generation for a missing
key after network/services are ready, and renewal/recoverable-failure scheduling.
Preserve backups and prove consumer acceptance separately. Existing wall-clock
revalidation, sleep/Doze alarm delays and update-required recovery remain bounded
unvalidated limits; the patch does not introduce a general recovery loop.

## Device and dependency review

| Scope | Finding | Limit |
| --- | --- | --- |
| Tokay product | caimito supplies persistent Trusty selection and production hostname | Active build inputs were preserved |
| Frankel product | Published muzel configuration supplies the equivalent properties | Active muzel remains upstream; hardware unverified |
| Shared platforms | Zumapro and Laguna select Rust Trusty KeyMint and inherit Trusty packaging | One platform's firmware evidence does not apply to the other |
| Standard adapter | Keystore2, KeyMint/RKP declarations, HAL init/VINTF, RKPD packaging, Binder/device/property policy are present | Bounded source inspection, not a rebuilt graph or firmware capability test |
| Published handoff | Eleven fork tips/tree mappings and three overlays reviewed; overlays parse without duplicate project paths | Source coverage remains bounded to the recorded connected stack |
| Frankel dependencies | vendor/google/frankel, device/google/muzel-kernels and out-kernel/google/gs-6.6 absent locally | Full preflight, compilation and hardware validation remain pending |

The earlier AVB experiment changed vbmeta boot metadata; it did not modify vendor
or Trusty firmware. The live audit's wording was clarified accordingly. The
published Zumapro source correction remains unchanged.

## Current hardware access and acceptance

The generated Duck EC private/public key pair originates locally in Android;
Trusty imports it for attestation. KeyMint/RKPD supplies the certificate path,
potentially using remote Google provisioning or the platform's retained fallback.
This route does not download a premade keybox, and its hardware key origin is
IMPORTED rather than GENERATED. Boot restores a valid stored keybox and generates
a replacement when absent or due; it does not regenerate on every reboot.

The forwarded ADB server at `127.0.0.1:50096` initially enumerated no devices.
After access was restored, a read-only check at 2026-11-08 23:53:32 UTC confirmed
root, persistent Trusty selection/hostname, boot completed, expected default and
StrongBox KeyMint/RKP services, Keystore2 and remote_provisioning. Duck was
available/enabled/active, Ready, not busy and had no error. Automatic provisioning
was neither paused nor waiting for network. Recent sampled logs contained no
known Duck errors, relevant AVC denials or RKP/Keystore HTTP 400 lines.

At 23:59:39 UTC, public certificates alone were extracted on the phone and checked.
The existing five-CA path and root self-signature verify; the imported certificate
and Google root fingerprints match the prior successful issuance. Earliest expiry
is November 20, 09:46:07 UTC; renewal is November 19. Actual boot remains
unlocked/orange and SELinux Enforcing. `imported=false` denotes no manually supplied
keybox, not a different hardware key origin. GMS, Play Store, GSF and the checker
are installed. Unset PIF/TrickyStore toggle values use the source's enabled defaults;
they do not establish missing components.

No private material was exported, and no phone setting, package, key or partition
was changed. No fresh provisioning, private-key signing, consumer, renewal,
secondary-user or integrity request ran in this review. A captured screen was black
and provides no new UI result. The user was told the device could be disconnected
after these live checks finished; further device tests require reconnecting it.

The latest recorded checker request returns no BASIC, DEVICE or STRONG labels.
Successful provisioning and a valid certificate path do not prove consumer
acceptance. The original direct external-key CSR protocol also remains unresolved
on these platforms. No new result closes either limitation.

## Checker and requester evidence

Public checker revision
[ee6316e](https://github.com/1nikolas/play-integrity-checker-app/blob/ee6316e906c7fa948fe688e534c6499f74a919a6/app/src/main/java/gr/nikolasspyr/integritycheck/MainActivity.java)
declares version 2.2/code 22 and maps an omitted `deviceRecognitionVerdict` to an
empty label set and three Fail icons. It does not distinguish optional-label
omission from independently evaluated device failure. Fresh installed-package
metadata matches that version; installed APK equivalence was not established.

The published [backend](https://github.com/1nikolas/play-integrity-checker-server/blob/91178657c076bb6f0aee23c43e014b619a6dcdcc/src/api/check.js)
decodes through Google's authenticated endpoint and returns the decoded payload.
The reviewed client/backend do not explicitly compare returned nonce/freshness with
the expected request before displaying labels. The deployed backend and private requester configuration
remain unverified; no tokens or account data were extracted here.

[Google's verdict documentation](https://developer.android.com/google/play/integrity/verdicts)
allows BASIC on unlocked devices and conditions optional BASIC/STRONG on requester
licensing/configuration on Android 13+. Omitted labels with UNEVALUATED licensing
prove no labels were returned, not that BASIC's device criteria independently
failed. A conclusive test needs trusted request-binding/freshness validation,
requester recognition/licensing and confirmed optional-label configuration.
DEVICE requires attested locked/certified boot on Android 13+; STRONG also requires
DEVICE and recent OS/vendor updates. No passing verdict is established by this review.

## Project PenguinOS comparison

The inspected [celerity manifest](https://github.com/Project-PenguinOS/manifest/blob/25e3127140d9e61d30850d8ad5fcf765db8b0e6c/penguin.xml)
uses Android 17. Its [framework RKP manager](https://github.com/Project-PenguinOS/frameworks_base/blob/559f366bcc8978767bccb03493bd682699934685/services/core/java/com/android/server/security/rkp/DuckRkpManager.java)
requires a Qualcomm/QTI/qcom manufacturer for availability and scheduling. The
inspected RKP directory contains V1/native adapters, without a Trusty import
adapter. AIDL packaging defines the interface rather than a signing implementation.

Its [Keystore2 import path](https://github.com/Project-PenguinOS/system_security/blob/4a467c1d678167f095803897aa7cb5e7fa33240f/keystore2/src/security_level.rs)
ignores the import attestation-key argument and passes no issuer to KeyMint, without
the RKPD-aware shared helper implemented in this port. This bounded comparison
found no additional Pixel-compatible Trusty signing adapter. It does not disprove
reported results on other hardware or establish this port's integrity verdicts.

## Source snapshot and preservation

[verification-rkp-review-source-hashes.json](verification-rkp-review-source-hashes.json)
records 102 files against the selected published revisions. Compared with the
101-file build-followup checkpoint, 96 hashes remain unchanged, the Settings resource
and four framework source/test hashes change, and the published AVB source file is added
to this combined snapshot. Historical snapshots remain unchanged.

[rkp-integration-review-verification.json](rkp-integration-review-verification.json)
records the scoped checks and source publication. All 21 source commits
across eleven forks are mapped in [publication-commits.json](publication-commits.json).

The Settings change is isolated in `/tmp/rom-settings-rkp-wording`. Active Settings
and the prior build-fix worktree remain clean at their original revisions. The renewal
fix is isolated in `/tmp/rom-framework-rkp-import-retry`, with the boot follow-up
in `/tmp/rom-framework-rkp-boot-resume`. Active
source revisions and manifests were not switched or edited.

Local `agent-memory/memory.md` and `tasks.md` reverted to older content during this
review, without a corresponding HEAD change. Those unstaged edits were preserved;
the documentation update was prepared in `/tmp/rom-memory-rkp-review`. The active
handoff checkout was not overwritten. Reconcile those local edits separately
before updating its checkout to published `main`.

The active Keystore2 file also acquired an unstaged reversal of the published
callback-type build fix. Its diff was preserved in `/tmp`; published source remains
correct. These concurrent changes are excluded from the source publication and
must be reconciled before a rebuild.
