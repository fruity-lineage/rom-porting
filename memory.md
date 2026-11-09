# Workspace memory

Updated 2026-11-09 UTC after the parallel review, live Tokay checks and publication
of Settings, renewal and boot-resume fixes. No passing Play Integrity labels have been established.

## Setup

- Workspace: /serverhive4/fruitzail/evox; Android Repo workspace, not a root Git checkout.
- Manifest: LineageOS lineage-24.0, Android android-17.0.0_r1.
- Device: Pixel 9, tokay, platform zumapro.
- Network source downloads succeeded.
- Workspace create/read/delete and GitHub HTTPS passed after access was restored.
- The user connects over remote SSH. At the last live check, forwarded ADB at
  127.0.0.1:50096 enumerated Tokay and provided root access. Forwarding
  is for ADB only, not USB fastboot recovery. Keep serials and credentials out of notes.
- User Git identity: fuzailmansuri <mfm9875@gmail.com>.
- Publication authorized under fruity-lineage, limited to ported work. Eleven source forks
  now have verified main tips and default branch main. Original authors and user coauthor
  credit are retained; publication messages include references and omit Gerrit Change-Id.
  Source trees are identical to the local topic commits. The mapping is in
  porting/audit/publication-commits.json. Handoff repository: fruity-lineage/rom-porting.
- The complete initial handoff is published on main at d6a940198b57eedadb5333ad2a7a940626d14c1e.
  All 57 tracked files and the tree match the local commit; all ten source fork tips
  were rechecked at that point. See porting/audit/handoff-publication-verification.json.
  Subsequent documentation commits record publication status without altering source forks.
- fruity-lineage/.github/main contains a device-neutral organization profile linking
  the handoff and disclosing AI assistance, as required by the ROM development skill.
- Read taste.md, tasks.md, spoofing-inventory.md and the final verification report before continuing.

## Tokay sources

All five projects were synced from matching lineage-24.0 branches through
.repo/local_manifests/tokay.xml.

| Local path | Upstream | Role |
| --- | --- | --- |
| device/google/tokay | LineageOS/android_device_google_tokay | Wrapper/extraction entry point |
| device/google/caimito | LineageOS/android_device_google_caimito | Pixel 9 family tree; tokay/ holds this device's extraction lists |
| device/google/zumapro | LineageOS/android_device_google_zumapro | Shared platform |
| device/google/caimito-kernels | LineageOS/android_device_google_caimito-kernels | Kernel modules/output destination |
| vendor/google/tokay | TheMuppets/proprietary_vendor_google_tokay | Proprietary blobs/firmware |

Vendor is shallow. All 15 LFS files were downloaded and initially passed git lfs fsck.
No device/vendor firmware edits were made during this verification.

## Kernel

- Nested Repo workspace: out-kernel/google/gs-6.1; all 18 projects initially synced.
- Manifest: LineageOS/android_kernel_google_gs-6.1_manifest, lineage-24.0.
- Common kernel: common/gki, android14-6.1-2026-03_r25, Linux 6.1.162.
- Device config: private/devices/google/caimito; modules: private/google-modules.
- The .out-dir marker excludes the nested workspace from Android source scans.
- caimito/device-tokay.mk selects caimito and google/gs-6.1.
- vendor/lineage/build/envsetup.sh initializes and builds the nested workspace, copying
  output into device/google/caimito-kernels/6.1.
- Do not invoke lunch to inspect configuration: it can trigger kernel work.
- No Android/kernel build was run during this verification. Existing output directories
  are not evidence of a successful validation of these commits.

## Port and verification checkpoint

The active Evolution X cnb manifest uses the same Android 17 tag and LineageOS 24 base.
Its vendor_evolution and device_evolution_sepolicy map to vendor/lineage and
device/lineage/sepolicy. Complete source snapshots are in /tmp/evo-spoofing-upstream;
additional compared text blobs are in /tmp/native-extra-sources. These temporary paths
are investigation caches; durable pins and evidence are in porting/audit.

The initial twelve-commit checkpoint covers nine projects on port/evolution-spoofing:
bionic, external/bouncycastle, vendor/lineage, system/core, device/lineage/sepolicy,
frameworks/base, packages/apps/Settings, system/security and device/google/caimito.
All nine were clean at that checkpoint. The user's build fixes were subsequently
amended into three local topic tips; those active checkouts remain untouched.
The same source trees are published through separate follow-up commits and isolated
worktrees. Pre-existing build/soong changes remain outside the port. There are now 21 source commits
across eleven published forks; original checkpoint hashes remain recorded below.

The port includes PIF, TrickyStore, game/device identity, package visibility, Aurora
installer reporting, per-app Settings-value overrides, their Settings UI, native hooks,
property staging and Duck framework/AIDL. The broader Sandbox feature set is excluded
because it is not a dependency of the selected Settings-value overrides.

Verified: 94 committed source hashes; 41 Java/16 Kotlin parses; 353 resource references;
244 unique names; eight destinations; 276 preserved plus 15 implemented AMS signatures;
frozen Duck AIDL/hash; six private syscall replacements; zero-error/warning scoped
preflight; eight extractor tests; five selected firmware payload hashes.
The follow-up verifies 99 combined committed source hashes (88 baseline files unchanged),
five final Java parses, two Rust rustfmt checks and zero-error/warning Tokay preflight.

Review closed missing EC provider registration, direct Duck gate bypass, destructive
malformed-config updates, unbounded network reads, unchecked refresh writes and stale
background downloads. Added Android/bionic tests remain unexecuted. The subsequent
user build provides Tokay compilation and compiled-policy evidence, recorded below;
hardware behavior was pending at that checkpoint; later direct results are below.

[verification.md](porting/audit/verification.md) records exact checks and limitations.
[spoofing-inventory.md](spoofing-inventory.md) contains source pins and all commit hashes.
Published revisions differ from local hashes because commit metadata was cleaned. Local
topic branches and backup/pre-fruity-publication-20261108 remain available. The overlay
at porting/manifests/tokay.xml selects the shared/device main forks, three unchanged Tokay dependencies
and the handoff repository, linking the root notes and porting tools into the workspace.

## Frankel and active build checkpoint

- User added Pixel 10 frankel as a target and requested device-neutral GitHub descriptions.
- Wrapper: device/google/frankel. Actual family tree: device/google/muzel; shared platform: laguna.
- All three source trees were synced from lineage-24.0; their pins are in frankel-import-verification.json.
- Laguna selects Rust Trusty KeyMint, ships API 36, and already sets TEE RKP-only.
- The isolated Frankel product port selects the same standard import-attestation adapter
  and supplies the missing RKP hostname default. It is published in android_device_google_muzel/main
  at 2b195b35d051eb63c9dcc6b02ff66a9e5c1a6a61, with source/property checks passing.
  The current main tip is 9c4bad6692c8275790bff334263914ddbd2a59e5 after moving
  device properties to PRODUCT_PRODUCT_PROPERTIES, matching the generic-system layout.
- caimito/main is now 2f7cc304134f77b3858da6e9d2390a5b22fbc467 with the same
  product-partition correction captured independently of the active build checkout.
- The active muzel checkout remains at its upstream pin; the change is in /tmp/frankel-duck-port.
  Use the public main tip as the durable copy. The user's Tokay build produced an OTA;
  the agent preserved active sources and manifests during publication and verification.
- Frankel vendor and muzel-kernel dependencies exist upstream but were not synced here.
  Complete device preflight, compilation, hardware import and production CA acceptance are pending.
- New overlays select either family or both via porting/manifests. Install one overlay
  after active builds finish; do not install overlapping overlays together.
- The handoff's actual Git checkout is agent-memory. Root notes and porting are linked into it.
- Ten remote forks and their source credits/trees are verified through the API. The
  HTTPS Git endpoint subsequently returned HTTP 403 despite verified push permissions;
  the two product-property commits were uploaded through Git data APIs with identical
  commit IDs. Do not expose credentials in troubleshooting or handoff notes.

## Tokay firmware constraint

The three Xiaomi HAL references use libkeymasterdeviceutils.so, Qualcomm commands
0x311e/0x3122 and a vendor object ABI. Tokay uses Rust Trusty KeyMint,
com.android.trusty.keymint and tee_device at /dev/trusty-ipc-dev0. AOSP KeyMint's secure
RKP path validates MACed CSR keys; raw external keys are not an equivalent request.

The initial tree lacked Duck AIDL/callers; the framework/AIDL port now supplies them.
Evolution X's available Trusty sources did not provide an equivalent external-key
extension. The Qualcomm HAL and its VINTF/policy were not installed on Tokay.

tzsw.img and five selected ELF payloads were re-extracted/hash-verified. Service-name
hints identify leads, not capabilities. No supported direct external-key CSR signing
entry point is verified. The alternative import adapter retains a capability gate.

Targeted disassembly now confirms the shipped HWBCC sign and BCC callbacks reject
the non-secure peer UUID before signing. KeyMint's UUID selects a separate GSA use case.
The app loader verifies signatures and signing-key policy; Android bootloader unlock
does not establish that a modified trusted app can load.

Standard imported-key attestation is now implemented as an alternative source adapter:
Duck generates an EC P-256 key, imports it as ATTEST_KEY through Keystore2's TEE security
level, and validates its certificate chain before producing the existing XML keybox.
Keystore import now honors user/RKPD attestation-key selection, keyblob upgrades and
chain processing. Tokay selects it with ro.lineage.duckrkp.trusty_import=true and an
optional production remote_provisioning.hostname default; this hostname was absent.
Availability requires a hostname plus Keystore2, TEE KeyMint and RKP declarations.
The Duck master setting remains opt-in. No new HAL daemon or Trusty command is needed
for this route; existing init, VINTF and service policy are traced in
[tokay-duck-import.md](porting/audit/tokay-duck-import.md).

Tokay firmware import and the returned production CA path are now directly verified
after correcting AVB boot metadata. General consumer compatibility remains unverified.
This route adds an imported CA certificate with actual imported origin and
boot state; it is not equivalent to Duck's direct external-key CSR protocol. Existing
RKPD hybrid/factory fallback behavior is retained. Full certificate validation rejects
unusable chains. [tokay-backend-investigation.md](porting/audit/tokay-backend-investigation.md)
records the unchanged firmware constraint. Later user reports record factory-backed
TEE import and targeted-app keybox use after a runtime override. The initial RKPD
failure is resolved by the later AVB experiment;
the actual checker/consumer acceptance remains unresolved.

## User build output verification (2026-11-08)

- Tokay's Android 17 OTA was generated by the user's build; no agent-run build was used.
- Package: `out/target/product/tokay/lineage-24.0-20261108-UNOFFICIAL-tokay.zip` (1,705,536,749 bytes).
- SHA-256: `55f7a4cec8e04562628351d9c685159a864b4d77470aad320a521129d1c86852`.
- ZIP CRC verification passes; embedded metadata declares tokay, SDK 37 and the 2026-11-01 patch level.
- Installed Settings contains the compiled focus-ring helper. Keystore2, runtime libc,
  product properties and compiled vendor policy are present and hash-recorded.
- Signing-key identity and the OTA signature were not verified. A complete source
  manifest was not captured before the user's build.
- Resolved build issues:
  1. `device/google/caimito`: Moved RKP and Duck properties to `PRODUCT_PRODUCT_PROPERTIES` to satisfy generic system artifact path requirements.
  2. `system/security`: Fixed the callback return type to `Result<KeyCreationResult, Error>` and removed premature anyhow context from import.
  3. `packages/apps/Settings`: Restored `src/com/android/settings/widget/InsetFocusRing.kt` for Compose UI focus rings.
- The property correction was already public. The other two fixes are now separate
  fast-forward commits: system/security a39ce2250d6ad58dcefa377bdd9e8465fd83e9c8
  and Settings 233ff319af4e0eb8369b4f1a5f976b3205a591e9. The helper exactly matches
  Joey's upstream file and retains his authorship plus user coauthor credit.
- Current active tips: security 27c3ec5862429ce676e1a396a747caf7c4567da1,
  Settings 53030932d1aa4b763b77c5085b2430709048dbe0,
  caimito bf2174958d133abfd1f233dd559e019939d8f707. Their trees equal the corresponding
  public build-fix checkpoint. The later Settings wording fix is isolated from active sources.
- All 101 build-followup snapshot files match that checkpoint's published trees. See
  [tokay-build-followups.md](porting/audit/tokay-build-followups.md) and its verification JSON.

## Known acceptance limits

- Direct ADB and the authorized reboot confirm persistent Duck selection and the
  production hostname; the original missing-property discrepancy is closed.
- Fresh remote provisioning and hardware import now pass. The current five-CA
  imported chain verifies to Google's current root, with IMPORTED/ATTEST_KEY and
  the actual unlocked/orange boot state. This verifies this chain, not all consumers.
- A sequential fresh Play Integrity Checker 2.2 request after provisioning finishes
  still shows BASIC/DEVICE/STRONG Fail. deviceRecognitionVerdict is omitted;
  recognition/licensing are UNEVALUATED. Checker token authenticity was not verified.
- The user's earlier targeted-app issuer proof and secondary-user checks remain
  reported evidence. A targeted chain using the new remotely provisioned keybox,
  renewal and independent secondary-user checks have not been repeated here.
- Frankel has source configuration only; its vendor/kernel dependencies, compilation
  and hardware acceptance remain pending. Do not transfer Tokay hardware conclusions.
- Android/bionic regressions remain unexecuted. Tokay's earlier user build provides
  compilation/linking and compiled-policy evidence; no rebuilt OTA with the AVB fix exists.
- Arbitrary unmapped pathname pointers can still crash the imported native app hooks;
  the committed guard fixes low pointers and non-app inspection only.
- Imports/reset span individual Binder/settings writes and can partially apply on failure.
- Background refresh still has a narrow final cross-process settings race.
- GMS 26.11.36, Play Store 53.9.23-34 and GSF 17 are installed. DroidGuard logs show
  configuration/keybox load; this does not prove its returned certificate chain.
- Coverage is bounded to recorded connected sources/history, not every org repo/branch.

## Direct RKP investigation and source fix

- See [tokay-live-integrity-investigation.md](porting/audit/tokay-live-integrity-investigation.md)
  and [verification JSON](porting/audit/tokay-avb-fix-verification.json).
- Original vbmeta flags 3 skipped chained AVB metadata. With the required zero GKI v4
  header word, fresh CSR boot_patch_level was 20000000 and RKPD rejected it with HTTP 400.
- The user explicitly authorized the signed flags-1 metadata write/reboot. The phone
  booted successfully; read-back matches the candidate; boot_patch_level is now 20261005.
  vbmeta size/hash properties return. Bootloader remains unlocked/orange; verity disabled.
- certify default now succeeds with four certificates and a verified Google root.
  Fresh Duck provisioning succeeds, ready/not busy/no error, revision 1 since reboot.
  Its imported five-CA chain and root self-signature verify; earliest expiry is Nov 20.
- Ordinary TEE RSA-2048 generation and SHA-256 sign/verify pass. The unique temporary
  probe alias was deleted and confirmed absent. No private keybox material was exported.
- Clean source fix: device/google/zumapro 13f60c3e3a84ace1a311082f134d4a0ab3ae0abd, published in
  fruity-lineage/android_device_google_zumapro/main. Use --set_hashtree_disabled_flag
  instead of --flags 3 when WITH_AVB is not true; normal AVB stays selectable.
  Make cases unset/false/true, scoped Tokay preflight and commit whitespace pass.
- The fix was committed in /tmp/tokay-avb-port; active sources/manifests remain untouched.
  Tokay/combined handoff overlays now select this eleventh fork. Frankel's Laguna tree
  was not changed. No ROM/kernel build or vendor/Trusty firmware modification was performed;
  the authorized experiment did change vbmeta boot metadata.
- Keep server backups in out/porting-tests/tokay-avb-metadata and the on-phone original
  vbmeta backup under /data/local/tmp. The full installed partition hash is
  777f68b817b2f4d77fa0a37c99bc2ced3d209fc2044af4caa40be5a03b822616.
  Keep the pre-renewal keybox backup on the phone only. The ADB tunnel has no fastboot
  recovery capability. No relock, wipe or slot change occurred.
- Temporary USB stay-awake was restored to its original global setting 0. The checker
  JSON dialog was closed and the temporary UI dump removed. Partition/keybox backups remain.
- Actual Play Integrity labels still fail. DEVICE on Android 13+ requires a locked,
  manufacturer-certified boot state; STRONG also imposes update requirements.
  Successful certificate issuance alone does not establish those verdicts.

## Duck failure report follow-up

The user reports Duck RKP is not working. A fresh read-only check still returns
available/enabled/active=true, busy=false, has_keybox=true, stage=ready and an empty
error. Automatic provisioning is not paused or waiting for network; expiry is
2026-11-20 09:46:07 UTC. The sampled 3000 recent log lines contain no known Duck
error codes or relevant AVC denials. This does not reproduce a provisioning fault
or establish consumer acceptance. The exact Settings/action symptom is pending.
See [status follow-up](porting/audit/tokay-duck-status-followup.json). No setting,
keybox, package or partition was changed by this check.

## Parallel integration review and follow-up fixes

- Three subagents reviewed the Settings description, genuine RKP status/source wiring,
  and published handoff/device dependencies. No missing dependency was found in this
  bounded review of the standard Trusty import route. It does not prove consumer acceptance.
- The forwarded ADB server initially listed no device. After access was restored,
  a fresh 2026-11-08 23:53:32 UTC check confirmed root, persistent selection/hostname,
  Ready/no error, all expected services and no sampled relevant denials or HTTP 400.
  Actual boot remains unlocked/orange and SELinux Enforcing. At 23:59:39 UTC the
  stored five-CA path and root self-signature verified again; no private material
  was exported. No fresh provisioning, renewal, secondary-user or integrity request ran.
- Settings' generation summary incorrectly required compatible Qualcomm firmware.
  The backend availability gate already supports the selected Trusty import adapter.
  Published follow-up 0a2e3c2c7dd19611e2e0a131c7530573ed59fc1c removes that sentence
  without changing provisioning logic. XML, resource names/caller and whitespace checks pass.
- The fix is isolated in /tmp/rom-settings-rkp-wording and published as a fast-forward
  on fruity-lineage/android_packages_apps_Settings/main with identical Git objects.
  Active Settings and the earlier build-fix worktree remain unchanged. The new UI has
  not been rebuilt or exercised on hardware.
- Published framework follow-up 60153c127470c3855d4e979a4b60190f6b13bdf5 retries
  documented temporary RKP pool/connectivity/busy failures through the existing
  backoff/network scheduler. Previously they permanently paused renewal. Failed
  alias cleanup still pauses; permanent, update-required and ambiguous errors keep
  their existing behavior. Peer review, Java syntax/API and whitespace checks pass;
  five added Android regressions and live fault injection remain unexecuted.
- The checker source maps omitted labels to crosses. Official Android 13+ rules also
  condition optional BASIC/STRONG labels on requester licensing and configuration.
  The recorded UNEVALUATED response establishes no returned labels, not independently
  evaluated BASIC failure. Verified requester/backend binding and licensing remain open.
- Published boot follow-up 4755e2231cf2ccc5617b310a1fb28583e6cb2f89 resumes only
  legacy temporary Trusty pauses, respects backend selection, and defers import before
  key/alias work if eager Keystore2 is not registered. Existing systemReady startup,
  saved-key restoration and networking already run without Settings. Four added
  persisted-state regressions and the updated hardware boot path remain unexecuted.
  Local key generation, valid-key reuse and automatic renewal remain conditional on
  the user's enabled/master settings; permanent/ambiguous/cleanup failures stay paused.
- The eleven source-fork tips and overlay/dependency mappings were reviewed against
  the inventory. Frankel still lacks synced proprietary vendor, muzel-kernels and GS 6.6
  dependencies here; full preflight, compilation and hardware validation remain pending.
- See [RKP review](porting/audit/rkp-integration-review.md) for the final source snapshot,
  publication verification and remaining checks. Actual BASIC/DEVICE/STRONG remains unresolved.
- Local memory.md and tasks.md reverted to older content during the review. Those
  unexpected unstaged edits were preserved. This update was prepared in the isolated
  /tmp/rom-memory-rkp-review worktree; the active handoff checkout was not overwritten.
- Active system/security also has an unstaged reversal of the published callback-type
  build fix. Its diff was preserved in /tmp; published main remains correct. Reconcile
  the concurrent edits before rebuilding. Active source inputs were not overwritten.
- The user authorized disconnecting the phone after the live checks finished. Further
  device testing requires reconnecting it; this review made no phone changes.

## Scoped validation commands

For the device checks, use the saved
[Tokay runtime verification prompt](porting/audit/tokay-runtime-verification-prompt.md).
It covers ADB access, provisioning, chain validation, actual signing and regressions;
preparing the prompt does not establish a hardware result.

Run from the Android root:

- PYTHONDONTWRITEBYTECODE=1 python3 porting/tools/preflight-tokay.py
- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s porting/tools -p test_extract_trusty_apps.py -v

The first wraps the skill checker to use caimito/tokay extraction lists and separates
normal/recovery manifests. Its underlying product scan is static and includes family
makefiles, not a fully evaluated Tokay build graph. See verification.md before interpreting it.

## hardened_malloc source checkpoint (2026-11-09)

- Fourteen malloc-related commits in twelve projects are published on main, with
  preserved upstream authors and porter credit. Every subject starts `malloc:`.
- Exact allocator upstream pin: GrapheneOS/hardened_malloc bf37d54560a62b50da72e8fda56abf04f23b5fd2.
  Latest allocator tip: 8fd6c6016ef53cc97ee5bc6f521cf70859342e37.
  Bionic tip: 4bf97cec2ff7787b54e23ca557411efb445e320d.
- Product opt-in targets Tokay/Frankel. Shared/static libc selects hardened_malloc
  only for compatible 64-bit/4-KiB/address-space configurations; Scudo fallback
  and secure-filtered DISABLE_HARDENED_MALLOC opt-out are retained.
- Source GKI uses 4-KiB VA48/max mmap entropy, preserving the 16-KiB VA47 path.
  Kernel overlays replace GKI and device configurations in separate Repo workspaces.
  Initialize nested .repo/repo before repo init to avoid the parent Android workspace.
- GWP-ASan remains on Scudo fallback; hardened heaps report ENOTSUP for allocation
  enumeration. Android C++ delete overloads reach free; upstream desktop new.cc
  is excluded by Android design. MTE tests skip unsupported configurations or CPUs without asymmetric policy.
- GitHub objects, 33 final changed-file hashes, manifests and source/static checks
  pass. No allocator Android/kernel build, boot or device test ran. Matching modules,
  vendor runtime, FIPS loading and MTE behavior remain acceptance work per device.
- Source and handoff work use isolated /tmp worktrees; active build inputs and
  pre-existing edits were preserved. Read the allocator audit and publication mapping.
