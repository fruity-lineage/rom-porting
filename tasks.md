# Task state

Updated 2026-11-08 UTC after successful AVB/RKPD validation; Play Integrity still fails.

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
- [x] Match all 101 current source snapshot files to public trees and preserve active checkouts.
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

The initial nine projects were clean at verification. Current publication contains
eighteen source commits in eleven forks. The active security, Settings and caimito
build fixes are committed in their local topic tips. Their trees match public main;
publication used isolated worktrees and did not switch or edit active source inputs.
Pre-existing build/soong
changes remain outside the port commits. See [verification.md](porting/audit/verification.md)
and [spoofing-inventory.md](spoofing-inventory.md).

## Remaining acceptance work

- [ ] Sync Frankel's proprietary vendor/kernel dependencies and complete full device preflight.
- [ ] Validate Frankel compilation and compiled SELinux after integrating the shared build fixes.
- [ ] Validate Frankel firmware import signing, production CA constraints and consumers.
- [ ] Establish actual Play Integrity acceptance. Latest fresh request has no labels;
  do not mark BASIC/DEVICE/STRONG complete from certificate-chain checks.
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
