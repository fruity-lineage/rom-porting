# Tokay KeyMint import-attestation adapter

Updated 2026-11-08 UTC. The source adapter is committed and statically checked.
At this initial source checkpoint hardware signing was unverified. The later
[live investigation](tokay-live-integrity-investigation.md) verifies Tokay import and
its production CA path after the AVB correction. Play Integrity labels still fail.

## Implementation

The framework creates an EC P-256 software key and imports its PKCS#8 encoding as
ATTEST_KEY through Keystore2's TEE security level, with a random challenge, serial,
distinct subject and bounded validity. Keystore now selects the caller's RKPD
attestation key for import, handles issuer-key upgrades, and appends its chain using
the same processing as generation. Explicit user attestation keys are also honored.

The adapter checks TEE metadata and response bounds, binds the chain to the generated
public key, verifies issuer signatures, pinned roots, CA usage, path lengths and PKIX,
then emits Duck's existing XML keybox format. The temporary Keystore alias is deleted
before and after import. The encoded import buffer is cleared. A cleanup failure
retains the primary failure; failed cleanup cannot turn provisioning into success.

Tokay selects the adapter with ro.lineage.duckrkp.trusty_import=true and supplies an
optional production remote_provisioning.hostname default. This hostname was absent
from the device/shared configuration; Keystore and RKPD use it to enable provisioning.
Availability also requires declared Keystore2, TEE KeyMint and RKP services. The
user's Duck master setting remains opt-in, with existing permission and scheduling gates.

The final device properties use PRODUCT_PRODUCT_PROPERTIES. The initial system
placement was corrected in [2f7cc304](https://github.com/fruity-lineage/android_device_google_caimito/commit/2f7cc304134f77b3858da6e9d2390a5b22fbc467),
matching the Pixel generic-system/product split. The active build edit was preserved;
publication was prepared in an isolated worktree.

## Service, init, VINTF and policy

| Layer | Existing source and integration |
| --- | --- |
| Product selection | zumapro/common.mk selects TRUSTY_KEYMINT_IMPL=rust and inherits trusty-base.mk |
| HAL packaging | system/core/trusty/keymint/trusty-keymint.mk selects android.hardware.security.keymint-service.rust.trusty |
| HAL init | android.hardware.security.keymint-service.rust.trusty.rc starts vendor.keymint.rust-trusty on /dev/trusty-ipc-dev0 |
| HAL VINTF | Its XML declares IKeyMintDevice/default V5 and IRemotelyProvisionedComponent/default V3 |
| HAL transport | keymint_hal_main.rs uses com.android.trusty.keymint and registers the standard Binder services |
| Keystore init | system/security/keystore2/keystore2.rc starts the early_hal service |
| Keystore VINTF | android.system.keystore2-service.xml declares IKeystoreService/default V6 and is required by keystore2_defaults |
| RKPD packaging | build/make/target/product/base_system.mk includes com.android.rkpd |
| Binder policy | system_server can find/use Keystore; Keystore is a Binder service and a KeyMint client, with RKPD access |
| Device policy | zumapro labels the Trusty node and HAL executable; platform hal_keymint policy grants transport access |
| New property | Lineage private policy labels the selection flag as an exact bool and allows system_server reads |

This route uses those services and interfaces. It introduces no new Trusty command,
custom HAL instance, init daemon, VINTF instance or direct Android HWBCC access.
The existing platform remote_prov_prop label and access rules cover the hostname.

## Local commits

| Project | Commit |
| --- | --- |
| system/security | cc1f9e42200d3e9c7a1aa47e433bd72023162002 |
| device/lineage/sepolicy | c9299e36c9738e4048bec188054ea0434e7b1798 |
| frameworks/base | 535d28c54c950b131550796c9829a4e572446df1 |
| device/google/caimito | 51ba2449f5180c93f6d2a7b4e6030a93034ed7f4 |

These are the local topic commits before publication metadata cleanup. The inventory
and publication mapping record their corresponding public revisions when available.

## Validation

- Five final Java sources parse without syntax errors.
- Both modified Rust files pass rustfmt --check with the project's Android configuration.
- Java/AIDL/provider/test helper dependencies and source inclusion were inspected.
- Tokay static preflight passes: zero errors/warnings, 76 normal and two recovery manifests.
- Eleven changed files match committed contents; all 99 combined source hashes pass.
  Eighty-eight baseline files remain unchanged. All nine port projects are clean.
- Commit whitespace, author/coauthor attribution and user sign-off were checked.

[tokay-duck-import-verification.json](tokay-duck-import-verification.json) contains
source pins and results. These checks do not establish compilation or test execution.

Added Android regressions remain unexecuted: explicit import issuer selection and
imported origin; imported ATTEST_KEY issuance and chain return; backend selection;
bounded TEE metadata; CA path-length, key mismatch, root and duplicate-chain rejection.

## Acceptance limits and continuation

The imported key adds a CA below the RKPD issuer. If a production issuer has pathLen=0,
that issuer cannot certify the additional CA; full validation must reject it. A successful
HAL import or VTS-style signature check alone is insufficient. The imported certificate
retains actual imported origin and boot state. This is a distinct issuance route from
Duck's direct external-key CSR protocol, with unverified consumer compatibility.
Standard Keystore hybrid/factory fallback policy is retained. No remote integrity result
is established. Shipped HWBCC still rejects non-secure signing, as recorded in the
[firmware investigation](tokay-backend-investigation.md).

A lost Binder reply or service termination may leave a temporary alias until a later
attempt deletes it. A stuck Binder request cannot be forcibly cancelled by the framework;
the existing single worker, timeout state and generation check prevent a stale save.

Hardware access was unavailable at the initial source checkpoint. It is now verified
through the forwarded ADB server; the [live investigation](tokay-live-integrity-investigation.md)
confirms imported CA issuance and production-chain validation after correcting AVB
metadata. Play Integrity labels still fail. To establish the same kind of ADB transport:

```sh
adb devices -l
ssh -o ExitOnForwardFailure=yes -R 127.0.0.1:50096:127.0.0.1:5037 USER@SERVER
```

On an installation containing these commits, verify the selection property, hostname
and standard services, run the added Keystore regressions, and use Settings' Device
RKP · Duck screen from the owner's profile. Inspect a returned production chain for
CA constraints and full validity before testing keybox consumers, renewal, cancellation
and ordinary Keystore operations. Do not export private keybox material into audit notes.
