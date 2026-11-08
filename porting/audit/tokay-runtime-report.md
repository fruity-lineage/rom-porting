# Tokay runtime report and evidence review

Recorded 2026-11-08 UTC from the user's local CLI report. This is user-supplied
hardware evidence, not an independently repeated device test on this SSH server.
Device identifiers, intermediate certificate serials and private key material
are omitted. Frankel has no corresponding hardware result.

## Observations and qualifications

| Stage | Reported observation | Evidence assessment |
| --- | --- | --- |
| ADB | Local USB and rooted adb daemon work | Reported pass on the local host; the SSH server's configured ADB endpoint still refuses connections |
| Build and services | LineageOS 24 build, enforcing SELinux, Keystore2, TEE/StrongBox KeyMint and RKP services present | The selection property is absent on the phone; persistent device configuration fails |
| Duck provisioning | Runtime override enables the backend; provisioning completes and increments keybox revision | Reported pass conditional on the override |
| Import attestation | Software P-256 key imported into TEE as ATTEST_KEY; challenge matches; four-certificate CA chain returned | Reported factory-backed import success; RKPD instead fails with HTTP 400 |
| Ordinary Keystore | EC signing verifies; fresh hardware attestation has a matching challenge and valid four-certificate chain | Reported ordinary Keystore pass; does not establish use of Duck's imported keybox |
| Cleanup and policy | Import alias removed, no relevant AVCs, existing keybox backed up, temporary probe removed | Reported happy-path cleanup; cancellation, failure cleanup, actual secondary-user behavior and restoration of overrides need further evidence |

The imported certificate reportedly has subject `CN=DuckRkp Imported Key`,
CA:TRUE and Certificate Sign usage. Its attestation records TEE security level,
IMPORTED origin, ATTEST_KEY purpose and an exact challenge match. Reported
attestation/keymaster version fields are 500; this record does not infer an
interface version from those numeric fields alone.

The reported chain ends at the pinned Google root with SHA-256
`CEDB1CB6DC896AE5EC797348BCE9286753C2B38EE71CE0FBE34A9A1248800DFC`.
Keystore logs reportedly show RKPD `ERROR_UNKNOWN` with HTTP 400, followed by
factory attestation fallback. This supports the alternative import route on the
tested firmware. It does not prove remote-provisioned issuer acceptance or the
original external-key CSR transport. Public certificates, probe source and full
validation outputs have not been supplied for independent verification.

## Missing device property

The report says `ro.lineage.duckrkp.trusty_import` is absent in the flashed build
and was overridden in runtime property memory for later tests. Persistent
configuration therefore remains unresolved on that installation.

The requested source setting already exists in the active and published
`device/google/caimito/device-tokay.mk`, using PRODUCT_PRODUCT_PROPERTIES. The
actual inheritance chain is:

`caimito/lineage_tokay.mk -> caimito/aosp_tokay.mk -> caimito/device-tokay.mk`.

`device/google/tokay` is the extraction wrapper; adding a duplicate setting to an
unused wrapper file does not resolve the discrepancy. Public caimito main and the
active makefile are byte-identical.

This server's generated product build.prop and the packaged target-files
`PRODUCT/etc/build.prop` both contain the selection property. Both SHA-256 hashes
are `f8229a2e54274f52f60832cef304ee6551b4ad20298b8a5e2c1ef9963f87b859`.
The previously verified OTA SHA-256 is
`55f7a4cec8e04562628351d9c685159a864b4d77470aad320a521129d1c86852`.

The flashed OTA hash, active slot, mounted product property file and runtime
override mechanism must be compared. A stale/different product image, property
loading problem or different build inputs remain hypotheses, not diagnosed causes.
The reported display ID differs from local source overrides; identity overrides
make that insufficient by itself to identify the flashed source revision.

## Why Stage 5 does not yet prove Duck use

The probe ran through app_process. AndroidKeyStoreSpi resolves Process.myUid()
to packages and only hooks requests selected by TrickyStoreService.needHack().
That method returns false for null packages or untargeted packages. The report
does not identify the probe UID, package mapping or target policy.

CertificateHacker and CertificateGenerator construct the app chain by prepending
the new app leaf to the active keybox's certificates. A four-certificate imported
keybox therefore normally produces a five-certificate app chain whose cert[1]
is the imported Duck certificate. The reported four-certificate ordinary chain
can instead be the factory path. Challenge matching and valid signatures alone
do not identify which issuer signed the new leaf.

A targeted package must retrieve a fresh chain containing the exact active Duck
certificate as issuer. Compare public DER/SPKI hashes on-device, verify the new
leaf signature with the imported keybox public key, then validate the complete
chain including CA path lengths. Preserve an untargeted control and test the
application's real package/UID path. Read-only source restrictions alone do not
prove secondary-user behavior.

## Remaining checks

1. Reconcile the phone's missing property with its exact OTA and product image;
   verify persistence across a user-controlled reboot without the runtime override.
2. Demonstrate Duck keybox use through a targeted app with the issuer binding above.
3. Diagnose RKPD's HTTP 400 and test a successfully remote-provisioned issuer.
4. Exercise cancellation, failure cleanup, renewal, real secondary-user restrictions
   and state restoration. Record precise results rather than marking unrun cases pass.
5. Test intended consumers separately from cryptographic issuance.

Use [the follow-up CLI prompt](tokay-runtime-followup-prompt.md). Preserve sources,
manifests, keyboxes and full certificate validation while collecting evidence.
