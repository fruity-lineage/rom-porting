# Frankel import-attestation source integration

Updated 2026-11-08 UTC. This is source evidence and isolated device configuration;
it is not a hardware signing or full device validation result.

## Sources and device path

| Project | Inspected revision | Role |
| --- | --- | --- |
| device/google/frankel | f3bcc57634a8d7e4831ea9fb74f1874fc7c4d5ef | Wrapper; points to muzel |
| device/google/muzel | 60f3d1ade4062cec3609023357eba8fcccc9e74a | Pixel 10 family; device-frankel.mk and lineage_frankel.mk |
| device/google/laguna | 7ef3601320418d70f25509f4f1dd4895b6937fd2 | Shared platform, Trusty selection and policy |

lineage_frankel.mk inherits vendor/lineage and the device product. aosp_frankel.mk
identifies Pixel 10 and includes Laguna plus the Frankel product. The product uses
muzel kernels, GS 6.6 and shipping API 36. No kernel work was invoked.

Laguna selects TRUSTY_KEYMINT_IMPL=rust, inherits trusty-base.mk, and labels the
Trusty IPC node and HAL executable. The shared Trusty package supplies the standard
KeyMint/default and RKP/default init/VINTF integration already used by the adapter.
Laguna's vendor.prop already sets remote_provisioning.tee.rkp_only=1, while no RKP
hostname was found in the inspected device/shared configuration.

## Change and publication

The isolated configuration selects ro.lineage.duckrkp.trusty_import=true and adds
the optional production remote_provisioning.hostname default. It consumes the shared
Keystore import fix and framework adapter through existing standard interfaces and
policy. The master setting remains opt-in. No Qualcomm transport or Tokay firmware
addresses were reused, and no Frankel trusted-app modification was made.

Commit: [2b195b35d051eb63c9dcc6b02ff66a9e5c1a6a61](https://github.com/fruity-lineage/android_device_google_muzel/commit/2b195b35d051eb63c9dcc6b02ff66a9e5c1a6a61).
The fork's default branch is main. Its current tip is
[9c4bad6692c8275790bff334263914ddbd2a59e5](https://github.com/fruity-lineage/android_device_google_muzel/commit/9c4bad6692c8275790bff334263914ddbd2a59e5),
which places these properties in PRODUCT_PRODUCT_PROPERTIES. The active muzel checkout stays
at its inspected upstream revision; the port branch is in /tmp/frankel-duck-port.
GitHub main is the durable copy. No active Tokay checkout was changed for this port.

Checks passed: product inheritance, the Rust Trusty selection and standard VINTF
instances, RKP-only setting, transport labels, unique selection/hostname declarations,
whitespace, commit identity and unchanged active checkout. The changed file matches
its committed hash. [frankel-import-verification.json](frankel-import-verification.json)
records the evidence and limits.

## Pending

The source interface contract supports this integration route; shipped Frankel
firmware import behavior and production CA constraints have not been exercised.
The imported CA adds an intermediate and must satisfy full chain validation. The
Tokay HWBCC disassembly is not evidence about Frankel's firmware.

TheMuppets/proprietary_vendor_google_frankel and LineageOS/android_device_google_muzel-kernels
exist on lineage-24.0. They were not synced into this workspace. Full device preflight,
compiler/linker and compiled policy checks, Keystore regressions, hardware signing,
ordinary key operations, renewal and keybox consumers remain pending.
