# Task state

Updated 2026-11-08 UTC after verifying source forks and publishing the shared handoff.

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

The initial nine projects were clean at verification. Current publication contains
fifteen source commits in ten forks. The active caimito product-property edit is
preserved; both device corrections were committed in isolated worktrees.
Pre-existing build/soong
changes remain outside the port commits. See [verification.md](porting/audit/verification.md)
and [spoofing-inventory.md](spoofing-inventory.md).

## Remaining acceptance work

- [ ] Collect the result of the user's currently running Tokay build; no compiler result is recorded.
- [ ] Sync Frankel's proprietary vendor/kernel dependencies and complete full device preflight.
- [ ] Validate Frankel firmware import signing, production CA constraints and consumers.
- [ ] Connect Tokay through an ADB server reachable from this remote SSH server.
- [ ] Verify imported ATTEST_KEY acceptance, RKPD chain constraints and ordinary Keystore behavior.
- [ ] Validate the produced keybox with Tokay consumers, renewal and secondary users.
- [ ] Resolve direct external-key CSR signing if exact original Duck protocol support is required;
  the imported-CA route is an alternative, not that protocol's implementation.
- [ ] Complete Android compiler/linker/API checks and compiled SELinux validation.
- [ ] Execute the added Android/bionic regressions and exercise Settings/Binder flows.
- [ ] Address or accept the imported native pathname-pointer limitation.
- [ ] Verify Tokay hardware behavior, ordinary keystore operations and secondary users.
- [ ] Verify GMS availability and consumers on the intended installation.

No build was run during this verification, following the applicable ROM skills'
static-only workflow. Android/native tests remain unexecuted. The port is not fully
validated on hardware and does not establish remote integrity acceptance.

The original Duck CSR protocols require Qualcomm firmware. Tokay now selects the
standard import-attestation adapter, and the frontend becomes available when its
hostname and platform services are declared. Its master setting is still opt-in.
The source integration is committed; successful signing and production CA acceptance
are unverified. Direct HWBCC access remains rejected by shipped firmware. See
[tokay-duck-import.md](porting/audit/tokay-duck-import.md) for implementation and acceptance steps.

Source coverage is bounded to the connected active stack and recorded history queries;
it is not an exhaustive audit of all organization repositories or historical branches.
