# Tokay first-stage boot failure, 2026-11-09

The inspected new images have a proven FIPS/GKI ABI mismatch. The current recovery
installation also has an independently observed module-partition layout problem.
The source fixes are published; no corrected images were built or flashed here.

## Proven FIPS failure

The kernel extracted from `out/target/product/tokay/boot.img` matches the kernel
distribution `Image` byte for byte and uses 4-KiB pages / VA48. Its `module_layout`
CRC is `0x248147a7`. The `fips140.ko` extracted from the packaged
`vendor_kernel_boot.img` expects `0xea759d7f`, matching the user's reported
first-stage init panic. It is the independently downloaded FIPS module from
build 11690398, still selected after the source GKI switch.

Across 340 distribution modules and 18,426 imported GKI-symbol comparisons,
339 modules have no mismatch. FIPS has 68 mismatched imports. This check covers
symbols exported by the selected GKI, not every inter-module dependency or
runtime requirement. A shared Linux version number does not establish this ABI.
The reported crash precedes second-stage Android startup; first-stage init is
itself userspace and may use statically linked libc.

## Source correction

- `common/gki` commit `86f19d582a316c70816d8beb5bcebb3398f20caf` preserves the
  kernel directory resolved by the FIPS build environment instead of overriding
  `common/gki` with the obsolete `common` path.
- `private/devices` commit `4161bff14a5405e22de9921a83f556153d28a867` selects
  the existing source FIPS target from the selected kernel package whenever GKI
  prebuilts are disabled. Prebuilt GKI builds retain the original downloaded FIPS
  path; existing FIPS enablement controls and cryptographic self-tests remain.

Both changes are active on `fix/tokay-fips-kmi-20261109` and published to the
corresponding fruity-lineage `main` branches. The installed nested kernel overlay
already selects those branches. No manifest switch is needed.

Configured Bazel queries verify both source and prebuilt selection, executing zero
build actions. Shell configuration resolution and whitespace checks pass. Native
compilation, a regenerated OTA and boot acceptance remain pending. The build must
refresh the staged `device/google/caimito-kernels/6.1` outputs and regenerate the
coordinated ROM images; rebuilding or flashing only `boot.img` is insufficient.

## Why restoring old boot images is not enough

Recovery on slot B runs the older `g7b58131aec77-ab16736902` GKI and an old ramdisk
module with CRC `0xea759d7f`. The mounted system identifies as new incremental
`1794246017`. The raw installed `system_dlkm_b` contains an exact copy of the new
build's `rfkill.ko`, with CRC `0x248147a7`. Finding bytes in the raw partition does
not prove that a valid mounted filesystem can resolve that file.

More fundamentally, neither currently mapped DLKM partition has a valid ext4
primary superblock at byte 1024. Each contains a superblock matching its expected
volume name, UUID and block count at byte 525312: a 512-KiB displacement.
Both device-mapper tables agree with the current LP metadata, and host `debugfs`
rejects the mapped images. The device fstab requires these as first-stage ext4
mounts. This installation needs a coherent partition/image repair as well as the
FIPS fix. The exact action that caused the displacement is not established.
Do not move partition boundaries or erase metadata based only on this finding.

Pstore was empty by the time recovery was inspected. The reported original panic
is user-provided evidence supported by the artifact mismatch; no fresh normal-boot
failure log after the old-image restoration was available. No reboot, flash, wipe,
settings change, key operation or module insertion was performed in this audit.

The user requested a five-minute build hold, which was observed. Afterward, no
active Tokay build was visible in this workspace and the inspected images were
unchanged. A targeted build override was requested because the loaded ROM skill
says “No builds. Nothing gets built to test.” No approval was received yet.

Machine-readable evidence and source hashes are in
[tokay-boot-kmi.json](tokay-boot-kmi.json). Raw recovery logs and partition reads
remain local investigation material. Successful boot, allocator/MTE runtime
behavior and actual BASIC/DEVICE/STRONG acceptance remain open.
