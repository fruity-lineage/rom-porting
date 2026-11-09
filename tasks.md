# Task state

Updated 2026-11-09 UTC after the live review and Settings/renewal/boot fixes. The checker
still has no established passing labels; omitted optional labels need requester validation.

## Completed

- [x] Sync Tokay device/shared trees, vendor blobs and the nested GS 6.1 workspace.
- [x] Verify vendor LFS objects and create root agent memory.
- [x] Read all three supplied Xiaomi Duck commits and trace Tokay Trusty KeyMint.
- [x] Audit the connected active Evolution X stack and relevant feature histories.
- [x] Port framework, Settings UI, native hooks, configuration, restricted policy and Duck AIDL.
- [x] Add the missing internal Bouncy Castle EC provider registrations.
- [x] Finish framework, Settings and native/history reviews.
- [x] Fix manual Duck capability enforcement, malformed-config overwrite, unbounded reads,
  unchecked refresh writes and stale background results found during final review.
- [x] Verify 94 feature files, 57 Java/Kotlin parses, resources, navigation, AIDL and syscalls.
- [x] Pass feature-scoped and Tokay-specific static preflight.
- [x] Execute eight ELF-extractor tests and hash-verify five selected firmware payloads.
- [x] Make eight attributed local commits across seven projects and verify committed contents.
- [x] Update the Markdown handoff after verification.
- [x] Trace shipped HWBCC peer-UUID rejection and app-loader signing-key policy.
- [x] Record the imported-key/RKPD integration gap and certificate constraints.
- [x] Verify restored workspace writes and GitHub HTTPS; save the firmware investigation.
- [x] Implement the alternative KeyMint import-attestation adapter and Keystore RKPD import fix.
- [x] Select the adapter on Tokay and supply the missing production RKP hostname default.
- [x] Trace existing service/init/VINTF/policy and add the scoped selection-property policy.
- [x] Verify five final Java sources, two Rust rustfmt checks, 99 source hashes and static preflight.
- [x] Commit the follow-up in four projects and update the handoff and inventory.
- [x] Publish nine source forks under fruity-lineage with verified main tips and original credit.
- [x] Prepare the fork manifest overlay and publication/local commit mapping.
- [x] Sync Frankel wrapper, muzel and laguna sources; trace the Rust Trusty/RKP configuration.
- [x] Commit and publish the isolated Frankel product configuration in android_device_google_muzel/main.
- [x] Use device-neutral GitHub descriptions and prepare a shared rom-porting handoff.
- [x] Publish both product-partition corrections from isolated worktrees through GitHub APIs.
- [x] Publish AGENTS.md, memory, inventory, audits and all three manifest overlays in rom-porting/main.
- [x] Verify all ten source fork tips and all 57 initial handoff files against their local commits.
- [x] Publish the device-neutral organization profile with the required AI-assistance note.
- [x] Collect the user's Tokay OTA and verify its SHA-256, ZIP CRC, metadata and installed port artifacts.
- [x] Resolved build blockers: keystore2 Rust closure type mismatch, Settings InsetFocusRing widget restoration, and caimito PRODUCT_PRODUCT_PROPERTIES partition placement.
- [x] Publish the two missing fixes as separate fast-forward commits; preserve the helper's upstream author.
- [x] Match all 101 build-followup source snapshot files to public trees and preserve active checkouts.
- [x] Save the AI CLI runtime verification prompt in Markdown, linked from the handoff.
- [x] Record and qualify the user's local runtime report: factory TEE import and ordinary
  Keystore tests pass after an override; RKPD HTTP 400 and keybox-consumer proof remain open.
- [x] Verify the selection property already exists in public/active caimito and local
  product/target-files outputs; prepare the targeted follow-up prompt.
- [x] Record the later targeted-app five-certificate issuer proof and native control,
  plus RKPD's invalid boot_patch_level=20000000 server response.
- [x] Verify forwarded root ADB access and mounted product selection/hostname properties.
- [x] Match active boot, packaged init_boot/vbmeta and the compared bootloader prefix.
- [x] Independently reproduce RKPD HTTP 400 and decode selected fresh CSR fields.
- [x] Trace the existing WITH_AVB gate and libavb's verification-disabled metadata skip.
- [x] Prepare and verify a signed flags-1 vbmeta experiment and save the active-slot backup.
- [x] Test the read-only integrity collector: nine unit tests pass.
- [x] Obtain fresh checker JSON before the metadata test; all three labels absent,
  recognition/licensing UNEVALUATED. DroidGuard restart does not change the result.
- [x] Obtain explicit authorization, write/read-back verify flags-1 vbmeta on slot _a,
  preserve the original backup and complete a successful reboot.
- [x] Verify post-reboot property persistence and corrected CSR boot_patch_level=20261005.
- [x] Confirm RKPD certify default succeeds and its production certificate chain verifies.
- [x] Confirm fresh imported Duck CA issuance, all five signatures and actual boot-state fields.
- [x] Verify ordinary TEE Keystore RSA-2048 generation/sign/verify and temporary alias cleanup.
- [x] Repeat the real checker request after provisioning; all labels still fail.
- [x] Commit/publish the isolated Zumapro AVB metadata fix and update handoff overlays.
- [x] Restore temporary USB stay-awake to 0 and retain recovery/keybox backups.
- [x] Complete three parallel reviews of Settings wording, genuine RKP wiring/status,
  and source-fork/overlay/device dependencies; no missing import-route dependency found.
- [x] Remove the obsolete Qualcomm-only generation description in an isolated Settings
  follow-up; verify XML/resources/caller/whitespace and publish identical objects on main.
- [x] Restore live phone access for read-only checks; confirm Ready/no error, expected
  services/policy, persistent properties and a valid stored five-CA/root signature path.
- [x] Fix permanent renewal pause on documented recoverable import errors, including
  cleanup-failure precedence; complete peer/static checks and publish on main.
- [x] Trace checker icon/request/decode behavior and official optional-label/licensing rules.
- [x] Trace systemReady startup and saved-state restoration; publish the boot recovery
  migration and pre-import Keystore2 readiness deferral with peer/static checks.

The initial nine projects were clean at verification. Current publication contains
21 source commits in eleven forks. The active security, Settings and caimito
build fixes are committed in their local topic tips. Their trees match the public
build-fix checkpoint except for the newly observed unstaged Keystore2 reversal.
The later Settings/renewal/boot corrections remain isolated from active sources.
Publication used isolated worktrees and did not switch or edit active source inputs.
Pre-existing build/soong
changes remain outside the port commits. See [verification.md](porting/audit/verification.md)
and [spoofing-inventory.md](spoofing-inventory.md).

## Remaining acceptance work

- [ ] Verify the corrected Settings description in a rebuilt UI on hardware.
- [ ] Execute the five new import retry/cleanup regressions and live renewal fault injection.
- [ ] Execute the four persisted-state regressions and test cold boot/OTA restoration
  without opening Settings, including missing-key generation after services/network are ready.
- [ ] Reconnect the device for further hardware tests after the authorized disconnect.
- [ ] Reconcile the unexpected active memory/tasks and Keystore2 edits with the published handoff;
  the isolated documentation update preserves them rather than overwriting them.
- [ ] Identify the user-reported Duck failure: last recorded backend state is Ready/no error;
  exact Settings/provisioning symptom is pending. Do not equate Ready with consumer success.
- [ ] Sync Frankel's proprietary vendor/kernel dependencies and complete full device preflight.
- [ ] Validate Frankel compilation and compiled SELinux after integrating the shared build fixes.
- [ ] Validate Frankel firmware import signing, production CA constraints and consumers.
- [ ] Establish actual Play Integrity acceptance. Latest fresh request has no labels;
  do not mark BASIC/DEVICE/STRONG complete from certificate-chain checks.
- [ ] Verify a trusted requester/backend's request binding, recognition/licensing and
  optional-label configuration before interpreting omitted BASIC/STRONG as device failure.
- [ ] Independently review targeted-app use of the new remotely provisioned keybox.
- [ ] Verify an OTA built with the committed AVB source fix; live validation used a signed derivative.
- [ ] Independently review public-chain/probe evidence for the reported factory import success.
- [ ] Validate the produced keybox with Tokay consumers, renewal and secondary users.
- [ ] Resolve direct external-key CSR signing if exact original Duck protocol support is required;
  the imported-CA route is an alternative, not that protocol's implementation.
- [ ] Execute the added Android/bionic regressions and exercise Settings/Binder flows.
- [ ] Address or accept the imported native pathname-pointer limitation.
- [ ] Complete Tokay renewal, secondary-user and broader consumer/regression checks.
- [ ] Verify GMS availability and consumers on the intended installation.

No agent-run build was used, following the applicable ROM skills' static-only workflow.
The user's Tokay build produced the verified OTA and compiled policy; signing-key
identity and OTA signatures were not verified. Android/native tests remain unexecuted. The port is not fully
validated on hardware and does not establish remote integrity acceptance.

The original Duck CSR protocols require Qualcomm firmware. Tokay now selects the
standard import-attestation adapter, and the frontend becomes available when its
hostname and platform services are declared. Its master setting is still opt-in.
The source integration is committed. The user reports factory-backed import and
targeted-app injection success. Remote-provisioned issuance and CA-chain validation
now pass directly; checker acceptance still fails. Direct HWBCC
access remains rejected by shipped firmware. See
[tokay-duck-import.md](porting/audit/tokay-duck-import.md) for implementation and acceptance steps.

Source coverage is bounded to the connected active stack and recorded history queries;
it is not an exhaustive audit of all organization repositories or historical branches.

## hardened_malloc (2026-11-09)

- [x] Trace pinned upstream allocator, matching Android libc/build dependencies,
  4-KiB/VA requirements and both source GKI selections.
- [x] Import the fork with original history/license; wire product flags, libc, MTE
  disable, fatal handling, malloc_info and truthful unsupported heap inspection.
- [x] Preserve Scudo/16-KiB/low-memory/HWASan fallbacks and prior native hooks.
- [x] Adapt both kernels, init mapping limits and selected device/source-GKI configs.
- [x] Add allocator regressions and runtime guards for upstream MTE tests.
- [x] Finish independent source/manifest/setup reviews, 33 source hashes and
  publication checks; publish 14 malloc: source commits across 12 projects.
- [x] Update Android/nested kernel overlays, provenance, agent memory and instructions.
- [ ] After active builds finish, install both required overlays and build the
  coordinated Android/GKI/module set. Agent work used static checks only.
- [ ] Run added libc/libmem tests and applicable MTE tests; verify startup, fallback,
  camera/media/graphics/browser/native bridge, recovery and static processes.
- [ ] Validate module/KMI/FIPS loading and allocator/MTE behavior separately on each device.

The existing RKP, renewal/runtime and Play-verdict acceptance tasks above remain pending.

## Tokay active-source checkpoint (2026-11-09)

- [x] Diagnose why the existing OTA omitted hardened_malloc: published worktrees
  were not installed in the active source checkout.
- [x] Activate the complete Tokay Android port and both GS 6.1 kernel changes,
  install both overlays, preserve old refs and the existing Soong edits.
- [x] Verify 30 allocator file hashes, unique manifest paths, Repo metadata,
  scoped preflight and local source/kernel sync.
- [x] Record the supplied RKP handover with provenance and uncertainty.
- [ ] Build the coordinated Tokay Android/GKI/module set and validate the new OTA
  and runtime allocator. Existing artifacts still contain the earlier source set.
- [ ] Validate allocator regressions, MTE, vendor/module/FIPS behavior on Tokay.
- [ ] Activate and validate the separate Frankel allocator/kernel stack when requested.

The earlier combined install/build checkbox is superseded for Tokay: installation
is complete; compilation and runtime acceptance remain pending. No build or phone
change was performed in this task.

## Required full Tokay integrity acceptance (2026-11-09)

- [x] Establish BASIC, DEVICE and STRONG passing as the explicit completion criteria.
- [x] Trace signing/opaque-key restrictions, cross-algorithm issuer fallback and
  requester/configuration evidence; retain verified facts separately from inference.
- [ ] Obtain the reachable Tokay ADB endpoint; the existing tunnel refuses connection.
- [ ] Verify effective System-namespace PIF/TrickyStore toggles and real caller chain.
- [ ] Establish a working Tensor signing backend that meets the required consumer
  behavior; the current imported-key route is not verified parity.
- [ ] Demonstrate fresh authenticated BASIC, DEVICE and STRONG labels with request
  binding/freshness and requester optional-label configuration validated.

The full integrity objective remains incomplete; no labels were claimed or fabricated.
Details: [tokay-integrity-parity.md](porting/audit/tokay-integrity-parity.md).

## Tokay integrity runtime checkpoint (2026-11-09)

- [x] Restore ADB access and capture fresh checker responses.
- [x] Verify absent owner PIF profile, restore it and observe Java/native integration.
- [x] Verify public Vending caller chain and actual EC issuer fallback for RSA.
- [x] Perform and restore provider comparison without account-data clearing.
- [x] Publish and activate three PIF reload/toggle/restart/generated-ID corrections.
- [x] Preserve other builds, existing source edits and the active allocator port.
- [ ] Compile coordinated Android/GKI/modules and run 13 PIF regressions plus allocator tests.
- [ ] Verify rebuilt-source consumer behavior and allocator runtime on Tokay.
- [ ] Establish a Tensor signing backend that can satisfy the requested consumer trust.
- [ ] Validate requester label configuration, authenticated response binding and actual
  BASIC/DEVICE/STRONG passing. No labels are established by the current responses.

This supersedes the earlier unreachable-tunnel task. The imported-key backend still
contains actual unlocked/orange BootInfo. Source fixes alone do not prove acceptance.

## Tokay confidence validation checkpoint (2026-11-09)

- [x] Verify 133 active Tokay file hashes and committed contents across 16 projects.
- [x] Pass scoped preflight and nine existing evidence-collector tests.
- [x] Confirm the Android regression files belong to their existing test modules.
- [ ] Receive the requested override of the ROM skill's no-build rule, then build
  the coordinated Android/GS 6.1/module set and compile/run the Android regressions.
- [ ] Restore ADB access; both checked local server ports reset the protocol.
- [ ] Establish a working signing path and fresh authenticated BASIC/DEVICE/STRONG
  results after repeated boots without manual Settings intervention.

Details: [validation readiness](porting/audit/tokay-confidence-readiness.md).
No build or new device verdict was produced by these checks.

## Allocator Soong build blockers (2026-11-09)

- [x] Fix inherited allocator headers for product/vendor and APEX consumers.
- [x] Exclude Windows HMallocTest while retaining the supported Linux host test.
- [x] Rerun the reported Soong analysis successfully and verify retained arm64 MTE tests.
- [x] Commit and publish f09ff6a in external/hardened_malloc; update publication mapping.
- [ ] Complete native/Java compilation, coordinated image production and device tests.

The [Soong verification](porting/audit/hardened-malloc-soong-availability.json)
records the narrower validation scope. No passing integrity verdict is implied.
