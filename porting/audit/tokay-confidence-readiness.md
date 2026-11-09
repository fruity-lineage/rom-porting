# Tokay validation readiness — 2026-11-09

Source integration is verified. Compilation, boot reliability and STRONG acceptance
remain unverified for the updated source set.

## Checks completed

- 133 Tokay source files match both their recorded SHA-256 values and the active
  Git commits across 16 projects, including the two nested GS 6.1 projects.
  The expected Frankel-only device file was excluded: that port remains inactive
  and does not participate in Tokay.
- The input snapshots are verification-rkp-review-source-hashes.json,
  hardened-malloc-activation.json, tokay-pif-reload-verification.json and
  tokay-pif-identity-verification.json, with newer records overriding earlier ones.
- Scoped Tokay preflight reports zero errors and zero warnings.
- All nine existing check-play-integrity.py collector/parser tests pass.
  These are host utility tests, not Android or Play Integrity acceptance tests.
- The added Java regressions are included by the existing FrameworksCoreTests,
  FrameworksServicesTests and RemoteProvisioningServiceTests source globs.
- Both tested ADB endpoints, localhost ports 50096 and 5037, reset the ADB protocol
  connection. TCP connectivity alone did not establish device access.
- No build controller was found when checked. No Android/kernel build, source
  revision switch, application-data clearing or phone change occurred.

Commands executed:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 porting/tools/preflight-tokay.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s porting/tools -p test_check_play_integrity.py -v
```

The current OTA still declares incremental 1794188022. Its generated product
properties identify the November 9 build; the saved build manifest predates build
fixes already included in the output. It is not a complete record of final build
inputs. The local vbmeta output still has flags 3; the active source selects only
the hashtree-disabled flag. Earlier build evidence and the recorded activation
baselines were used to avoid treating already-built fixes as new.

## Required validation

1. Preserve the previous OTA and kernel distribution, pin Android and nested
   kernel inputs, and build the coordinated Tokay Android/GKI/module set.
   The existing kernel hook supports SKIP_KERNEL_SYNC=true to retain reviewed
   revisions. Kernel selection itself must still build the source GKI.
2. Compile and run the PIF, identity and RKP regressions in FrameworksCoreTests,
   FrameworksServicesTests and RemoteProvisioningServiceTests. Run the applicable
   bionic-unit-tests, memunreachable_test and allocator MTE tests; record skips
   and unsupported configurations separately from passing tests.
3. On the resulting image, verify actual allocator selection, module/FIPS loading,
   ordinary Keystore operations, boot restoration, late network availability and
   recoverable renewal errors. Recheck normal device functions affected by libc.
4. Obtain fresh, authenticated BASIC/DEVICE/STRONG results after repeated cold and
   warm boots without manual Settings intervention. Verify requester recognition,
   licensing, optional-label configuration, request binding and freshness. Test
   verdict overrides and third-party UI screenshots do not establish this result.

The current imported signing certificate retains actual unlocked/orange BootInfo.
No verified Tensor signing alternative has been established, and the precise
Google rejection reason remains unisolated. A successful build or local test suite
alone cannot establish STRONG acceptance.

The ROM device-development skill explicitly forbids builds for validation. An
override and restored ADB access were requested; neither had been received at this
checkpoint. No build or new device verdict is claimed.
