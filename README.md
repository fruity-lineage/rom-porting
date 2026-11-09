# ROM porting handoff

Agent instructions, source provenance, manifests and validation records for the
LineageOS 24 / Android 17 spoofing and Duck integration. The source changes are in
the forks listed in [spoofing-inventory.md](spoofing-inventory.md), all using main.

Read [AGENTS.md](AGENTS.md), [taste.md](taste.md), [memory.md](memory.md),
[tasks.md](tasks.md) and the inventory before continuing. Preserve original authors
and source references. Keep incomplete work and validation limits visible.

The shared stack is committed. Device configuration is available for Pixel 9
(tokay/caimito/zumapro) and Pixel 10 (frankel/muzel/laguna). Tokay remote provisioning,
imported-key attestation and the returned production CA path are now verified on hardware.
Actual Play Integrity labels still fail; Frankel hardware remains unverified.
The subsequent [parallel review](porting/audit/rkp-integration-review.md) fixes an
obsolete Qualcomm-only Settings description and a recoverable-error renewal pause.
The boot follow-up also resumes known temporary legacy pauses and defers import
until eager Keystore2 is ready; normal enabled startup already restores without Settings.
Live checks again confirm Ready and a valid stored certificate path. The new fixes
need rebuilt-device tests. Checker label omission also requires requester/licensing validation.
The original direct external-key CSR protocol remains unresolved on these targets.
Tokay's user build produced a verified OTA after the recorded
[build fixes](porting/audit/tokay-build-followups.md), now published as follow-up
commits. Frankel compilation remains pending.

## Workspace setup

Start from the LineageOS lineage-24.0 manifest. Use **one** overlay from
[porting/manifests](porting/manifests): pixels.xml includes both families; the
individual overlays include the shared forks and one family's dependencies.
Replace overlapping device-discovery manifests rather than installing duplicates.

For a fresh workspace:

```sh
repo init -u https://github.com/LineageOS/android.git -b lineage-24.0 --git-lfs
mkdir -p .repo/local_manifests
curl -fL https://raw.githubusercontent.com/fruity-lineage/rom-porting/main/porting/manifests/pixels.xml \
  -o .repo/local_manifests/ported-pixels.xml
repo sync
```

The overlay checks this repository out as agent-memory and links its instructions,
memory files and porting directory into the Android root. Edit those files through
either path and commit them in agent-memory. This checkout alone contains no ROM
sources or private keyboxes. Source commit mapping and identical-tree publication
checks are in [publication-commits.json](porting/audit/publication-commits.json).

Do not sync or change source revisions during an active build. Tokay's build fixes
and Frankel's configuration were published from isolated worktrees, preserving
active source checkouts. Frankel's proprietary vendor and kernel dependencies
were not synced or built during this work.

## Acceptance work

Read the [Tokay adapter audit](porting/audit/tokay-duck-import.md) and
[Frankel source audit](porting/audit/frankel-import.md). Tokay's compiled outputs are
recorded separately from the initial static checks. Complete the recorded device checks
before claiming successful signing or consumer acceptance.

The [Tokay runtime verification prompt](porting/audit/tokay-runtime-verification-prompt.md)
can be passed to an AI CLI with access to the workspace and device.

The user's [runtime report](porting/audit/tokay-runtime-report.md) records the earlier
factory-backed import and targeted-app issuer proof. The
[direct ADB investigation](porting/audit/tokay-live-integrity-investigation.md) now
confirms property persistence and resolves RKPD's invalid boot patch date: original
vbmeta flags 3 skipped chained boot metadata; a signed flags-1 derivative restores
boot_patch_level=20261005. RKPD and fresh Duck provisioning succeed; the production
chain and ordinary TEE sign/verify pass. The shared Zumapro source fix is published
on main and included in the Tokay/combined overlays. Active build inputs were preserved.

A fresh checker request after provisioning still returns no BASIC/DEVICE/STRONG
labels. Hardware remains unlocked/orange. The
[verification JSON](porting/audit/tokay-avb-fix-verification.json) separates these
outcomes and records the remaining checks. Keep the vbmeta and on-phone keybox backups;
the ADB bridge does not provide fastboot recovery. Temporary stay-awake was restored.
The [read-only collector](porting/tools/check-play-integrity.py) retains selected
configuration/verdict fields without copying private keys or raw request material.

## Allocator port

The [hardened_malloc audit](porting/audit/hardened-malloc.md) covers the separate
allocator, bionic, build and kernel integration. Malloc-related port commits use
`malloc:` subjects. The Android overlays include its userspace dependencies;
install the matching overlay in `porting/manifests/kernels` into the nested kernel
workspace before selecting a lunch target. Both parts are required. Unsupported
page sizes/address spaces retain Scudo. Compilation, boot and allocator runtime
validation remain pending on both families.
