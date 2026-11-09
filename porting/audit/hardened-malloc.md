# hardened_malloc integration

Target: LineageOS 24 / Android 17. Source integration uses isolated worktrees;
no allocator build or hardware validation has been performed. Published revisions
and source checks are recorded in the companion verification JSON and inventory.

Fourteen malloc-related source commits across twelve projects are published on
main. The [publication mapping](hardened-malloc-publication.json) and
[final verification](hardened-malloc-verification.json) record exact tips, authors,
trees and checks. All 33 modified source files have final SHA-256 hashes in
[hardened-malloc-source-hashes.json](hardened-malloc-source-hashes.json).

The allocator source is pinned to
[GrapheneOS/hardened_malloc bf37d545](https://github.com/GrapheneOS/hardened_malloc/commit/bf37d54560a62b50da72e8fda56abf04f23b5fd2).
Preserve its upstream history, MIT license and CREDITS. Every new port commit,
including supporting kernel/build/documentation commits, starts with `malloc:`.
Inherited commits keep their original metadata.

## Integration requirements

Android consumes the static, prefixed `libhardened_malloc` inside libc. The Android
shared/preload target is disabled, and `CONFIG_SELF_INIT=false` requires bionic
startup wiring. Bionic retains the existing Scudo ABI and dispatch for fallback.
The port uses a product opt-in rather than enabling this allocator for every
LineageOS product.

This source requires 64-bit pointers and 4 KiB pages. Its Android default reserves
approximately 3136 GiB for slab regions alone; the upstream light configuration
reserves more address space and does not solve the 39-bit constraint. The port
preserves the default capacity and hardening settings. Runtime capability checks
must select Scudo before any hardened allocation on unsupported kernels, 16 KiB
boots or constrained address spaces.

The kernel needs `MADV_DONTNEED_LOCKED`, present in the inspected GS 6.1 and 6.6
sources. Init needs `vm.max_map_count=1048576` for guard mappings. MTE support is
optional and must be gated by the product, architecture and hardware capabilities.

Upstream's Android `h_malloc_iterate` aborts because heap iteration is unimplemented.
The libc adapter must return `ENOTSUP` instead, and heap leak inspection must
report unavailable coverage rather than a successful empty result. Android
`malloc_info` uses the upstream extended mallinfo APIs. The private fatal-handler
mallopt operation and disabling heap memory tags also need connected libc hooks.

## Kernel evidence by family

| Family | Exact GKI base | Evidence |
| --- | --- | --- |
| caimito / GS 6.1 | `7b58131aec77682c068b072dd055e130cfc971f7`, tag `android14-6.1-2026-03_r25` | Local source and recorded Tokay output configuration: 4 KiB, VA39, MTE enabled |
| muzel / GS 6.6 | `16f4b570c6c3536fc3e17695b88c7411083c2036`, tag `android15-6.6-2026-04_r33` | Pinned upstream source/configuration only; no Frankel kernel/device validation |

Both kernel builds default to prebuilt GKI. Changing module/device fragments
does not establish that the boot image uses a compatible GKI. Source GKI selection
and rebuilding matching system/vendor modules are required alongside the VA change.
Prebuilt FIPS module compatibility with the new configuration remains unverified.

The Kconfig adaptation selects VA48 and maximum mmap entropy for 4 KiB
builds through the existing architecture defaults. It preserves the 16 KiB VA47
path. Both Android products already expose a 16 KiB developer option; libc must
fall back to Scudo when that path is used.

Frankel's MTE capability is advertised by the pinned adevtool configuration
`690a11d9c97ed7c12b0947179937e3267e8bd200`: Frankel includes Laguna's common
BoardConfig, which includes BoardConfig-armv9.mk with `TARGET_HAS_ARM_MTE=true`.
The port does not import that tree's forced MTE boot policy or global sanitizer
settings. This is source evidence; actual Frankel CPU/boot behavior is unmeasured.

## Installing the complete source set

Use one Android overlay (`tokay.xml`, `frankel.xml` or `pixels.xml`) from
`porting/manifests`. It includes the allocator, libc, build plumbing and heap
inspection caller alongside the existing ports. Kernel overlays are separate
because each kernel is a nested Repo workspace.

Once active builds have finished, initialize the appropriate nested workspace,
install its overlay and sync it **before selecting a lunch target**. For Tokay:

```sh
kernel_workspace="$PWD/out-kernel/google/gs-6.1"
mkdir -p "$kernel_workspace/.repo"
touch "$kernel_workspace/.out-dir"
if [ ! -d "$kernel_workspace/.repo/repo" ]; then
    cp -R "$PWD/.repo/repo" "$kernel_workspace/.repo/repo"
fi
(
    cd "$kernel_workspace"
    repo init -u https://github.com/LineageOS/android_kernel_google_gs-6.1_manifest.git -b lineage-24.0
)
mkdir -p "$kernel_workspace/.repo/local_manifests"
cp porting/manifests/kernels/tokay.xml "$kernel_workspace/.repo/local_manifests/malloc.xml"
(
    cd "$kernel_workspace"
    repo sync
)
```

For Frankel, use `gs-6.6`, its corresponding manifest URL, and
`porting/manifests/kernels/frankel.xml`. Each overlay replaces only GKI and the
device kernel project and retains their original linkfiles. The device's existing
Lineage kernel build hook then sees the overlay during its normal sync and uses
`--nouse_prebuilt_kernel` for the selected family. Do not reuse old distributed
kernel/modules after enabling the new libc; a compatible 4 KiB boot kernel is
required for hardened selection. An incompatible runtime takes the Scudo fallback.
The nested Repo launcher must exist before running `repo init`: otherwise the
launcher can discover the parent Android workspace and reinitialize that instead.

## Runtime selection and diagnostics

`TARGET_USE_HARDENED_MALLOC=true` opts in this device. `TARGET_HAS_ARM_MTE=true`
exposes optional arm64 MTE support. Bionic selects the native allocator once during
shared/static startup after checking 4 KiB pages and probing an 8 TiB `PROT_NONE`
mapping without allocator calls. Insufficient address space or a native process's
`DISABLE_HARDENED_MALLOC` environment opt-out retains Scudo. The opt-out is filtered
during secure execution. Jemalloc low-memory builds and HWASan remain separate.

GWP-ASan remains available on Scudo fallback. Hardened selection occupies the
default dispatch slot and the existing GWP guard declines initialization before
mutating any GWP state. The port does not mix those allocators. Heap leak inspection
queries `M_GET_MALLOC_ITERATE_SUPPORTED` before capturing threads and reports
`ENOTSUP` on hardened_malloc. Allocation profiling/debug wrappers still require
runtime verification with the selected native allocator.

Android C++ operators come from the standard Clang libc++ prebuilts. The pinned
source and existing ARM64 archive confirm that ordinary, aligned and sized delete
overloads reach `free`, which uses the selected allocator. The matching upstream
Android integration also uses standard AOSP C++ projects and excludes desktop
`new.cc`. Its additional desktop sized-deallocation checks are not an Android
dependency. See [the C++ audit](hardened-malloc-cxx-verification.json).

## Source references

- [Bionic integration 9704800](https://github.com/GrapheneOS/platform_bionic/commit/9704800fc75a60be0edcb41cee4f884f6a1aeaf3), Daniel Micay and anupritaisno1; compared Android 17 tip `e93ce48518dc0fba69878cb4ace37a3525862cbe`.
- [Soong MTE variable 17b8985](https://github.com/GrapheneOS/platform_build_soong/commit/17b8985ea3a7a02c12dc57399b7f374a5b9ced60), Dmitry Muhomor.
- [Make MTE variable 3af19bd](https://github.com/GrapheneOS/platform_build/commit/3af19bd7c321a836ffe71020f015363365bd2ca8), Dmitry Muhomor.
- [Guard mapping limit e015be5](https://github.com/GrapheneOS/platform_system_core/commit/e015be54b45c8c13595ba4d402bc88078e19647a), Daniel Micay.
- [VA48 8007d2d](https://github.com/GrapheneOS/kernel_common-6.1/commit/8007d2d1579a3c85446996b654045bea07b8b44e) and [mmap entropy 6d9f73d](https://github.com/GrapheneOS/kernel_common-6.1/commit/6d9f73de39563946bcfc565d8bc15c896daa37b2), flawedworld; adapt rather than applying shared defconfig settings that break the 16 KiB path.

## Validation still required

Source checks do not establish linking, startup reliability, allocator performance
or vendor compatibility. After building the coordinated change set, validate:

- 4 KiB source-GKI configuration, matching module loading and boot/runtime startup.
- Hardened allocation in representative 64-bit processes, Scudo in 32-bit and
  16 KiB processes, and expected `/proc/PID/maps` allocator region names.
- Normal allocation/reallocation/alignment/usable-size behavior and thread/fork flows.
- MTE opt-out and enabled behavior on each target separately.
- `malloc_info`, fatal-handler restoration, explicit unsupported heap inspection,
  malloc debugging and fallback GWP-ASan behavior.
- Camera, graphics, media, browser/WebView, native bridge, recovery and static binaries.

The upstream MTE tests require asymmetric checking. Their runtime guard reports
JUnit assumptions for non-4-KiB boots, native fallback, absent/disabled MTE, or
unreadable/non-asymmetric CPU preferences. Ordinary API/test failures still fail;
the guard never changes system MTE policy.

New Android allocator regression tests remain unexecuted. The applicable ROM skills
require static validation for agent work; no `lunch`, Android or kernel build is run.
