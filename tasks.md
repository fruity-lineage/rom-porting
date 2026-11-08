# Task state

Updated 2026-11-08 UTC after direct ADB configuration, image and RKP checks.

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

The initial nine projects were clean at verification. Current publication contains
seventeen source commits in ten forks. The active security, Settings and caimito
build fixes are committed in their local topic tips. Their trees match public main;
publication used isolated worktrees and did not switch or edit active source inputs.
Pre-existing build/soong
changes remain outside the port commits. See [verification.md](porting/audit/verification.md)
and [spoofing-inventory.md](spoofing-inventory.md).

## Remaining acceptance work

- [ ] Sync Frankel's proprietary vendor/kernel dependencies and complete full device preflight.
- [ ] Validate Frankel compilation and compiled SELinux after integrating the shared build fixes.
- [ ] Validate Frankel firmware import signing, production CA constraints and consumers.
- [ ] Check selection-property persistence after an authorized reboot; mounted product
  now matches the build and contains the setting, so no duplicate source edit is needed.
- [ ] Independently review the reported targeted-app public chain/probe and test actual consumers.
- [ ] Obtain fresh JSON/licensing/labels from the identified Play Integrity API Checker
  2.2; phone unlock and the checker request are pending.
- [ ] Trace the invalid boot patch value, resolve RKPD HTTP 400 and validate a remote-provisioned chain.
- [ ] If approved, test the prepared metadata-verification candidate with local USB
  recovery available. Do not flash/reboot from diagnostic-access authorization alone.
  Verify CSR/RKPD, ordinary Keystore and real verdicts afterward; restore on failure.
- [ ] Independently review public-chain/probe evidence for the reported factory import success.
- [ ] Validate the produced keybox with Tokay consumers, renewal and secondary users.
- [ ] Resolve direct external-key CSR signing if exact original Duck protocol support is required;
  the imported-CA route is an alternative, not that protocol's implementation.
- [ ] Execute the added Android/bionic regressions and exercise Settings/Binder flows.
- [ ] Address or accept the imported native pathname-pointer limitation.
- [ ] Verify Tokay hardware behavior, ordinary keystore operations and secondary users.
- [ ] Verify GMS availability and consumers on the intended installation.

No agent-run build was used, following the applicable ROM skills' static-only workflow.
The user's Tokay build produced the verified OTA and compiled policy; signing-key
identity and OTA signatures were not verified. Android/native tests remain unexecuted. The port is not fully
validated on hardware and does not establish remote integrity acceptance.

The original Duck CSR protocols require Qualcomm firmware. Tokay now selects the
standard import-attestation adapter, and the frontend becomes available when its
hostname and platform services are declared. Its master setting is still opt-in.
The source integration is committed. The user reports factory-backed import and
targeted-app injection success; remote-provisioned issuance and checker acceptance
are unverified. Direct HWBCC
access remains rejected by shipped firmware. See
[tokay-duck-import.md](porting/audit/tokay-duck-import.md) for implementation and acceptance steps.

Source coverage is bounded to the connected active stack and recorded history queries;
it is not an exhaustive audit of all organization repositories or historical branches.
