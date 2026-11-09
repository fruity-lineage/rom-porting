# Tokay full Play Integrity acceptance target

Updated 2026-11-09 after the user explicitly required Snapdragon-like BASIC,
DEVICE and STRONG acceptance. This requirement is not complete. Duck Ready,
remote-provisioning HTTP 200, and a valid Google certificate chain are intermediate
results, not substitutes for fresh server verdicts.

## Current signing gap

Active frameworks/base is 4755e2231cf2ccc5617b310a1fb28583e6cb2f89. Its Trusty
adapter generates an exportable software EC key, imports it as ATTEST_KEY, and
includes the imported hardware-attested certificate in its XML chain
(DuckRkpTrusty.java:58-61,79-95,152-164; DuckRkpCertificates.java:93-103).
Previously measured attestation preserves the real unlocked/orange RootOfTrust.
Removing that certificate disconnects the software signer's public key from its
Google issuer; changing the signed record invalidates the signature.

A standard opaque RKPD key is not a replacement exportable signing key. At
system/keymint cfeefc94bf8c4f19d19dca193d376a1fc05e8e3e, rkp.rs:46-52,158-200
returns an ATTEST_KEY encrypted keyblob and MACed public key. operation/begin.rs:
412-417 rejects SIGN when the key lacks that purpose. The preliminary ATTEST_KEY
entry in the allowed-purpose table is not a signing escape: EC dispatch at
279-289 rejects it. Ordinary hardware attestation still adds actual BootInfo
(cert.rs:344-350,1317-1330). AndroidKeyStoreKey.java:95-103 returns no encoding.

The standard CSR path verifies public-key MACs using secure-side key material
(rkp.rs:235-270). Current Trusty source at
48faccf3fd79ef3bc23171ed9373965e8c302b4c computes the production HMAC with its
secure ephemeral key (rpc.rs:34-74). Android-generated keys and fabricated MACs
are not an equivalent API request. The inspected shipped HWBCC rejects non-secure
signing/BCC access, and app-loader policy does not establish that a modified
KeyMint TA is loadable. See tokay-backend-investigation.md. All five selected
firmware payload hashes were rechecked in this investigation and still match.
No exhaustive claim about all proprietary firmware interfaces is made.

## RSA warning is not a proved failure

KeyBoxManager.java:114 implements getKeyboxForLeaf(), including cross-algorithm
issuer fallback. CertificateGenerator.java:151 and CertificateHacker.java:123
both use it and select the signature algorithm from the issuer. An EC signing
key can therefore certify an RSA subject key. TrickyStoreService.java:400-401
warns about missing algorithm blocks during XML parsing. That warning does not
prove an RSA request failed. Actual installed-device behavior still needs capture.

## The server verdict cause remains unisolated

The recorded payload omits deviceRecognitionVerdict and reports app recognition
and licensing as UNEVALUATED. The checker displays missing labels as crosses.
This does not establish the exact proprietary server rejection reason. Google's
[verdict documentation](https://developer.android.com/google/play/integrity/verdicts)
allows UNEVALUATED for an untrustworthy device, unrecognized requester version,
or no signed-in Play account. Licensing may itself be a consequence of device
failure; it is not independently established as the root cause here. On Android
13+, BASIC/STRONG are optional and require a licensed requester to be returned;
DEVICE can still be returned without those optional labels. BASIC's criteria do
not inherently require locked boot. No OEM-keybox result is guaranteed.

## Concrete next device checks

- Read spoof_pif_enabled and spoof_trickystore_enabled from Settings.System for
  user 0, not Settings.Secure. AxSpoofManager.java:474,483,528,634,686 reads the
  System namespace with enabled defaults. Read spoof_activated from Secure.
- Verify the effective PIF profile and TrickyStore mode without exporting private
  keybox material. PIF defaults to spoofProvider=false. Enabling provider spoofing
  causes AndroidKeyStoreSpi.java:190 to reject DroidGuard chain retrieval; this
  fallback is not evidence of DEVICE/STRONG.
- Use a Play-recognized/licensed requester with optional BASIC/STRONG configured,
  no test verdict overrides, and fresh authenticated response decoding. Validate
  package binding, nonce/request hash and timestamp. Reviewed checker backend
  91178657c076bb6f0aee23c43e014b619a6dcdcc returns Google's decoded payload but
  does not itself compare request binding or freshness; deployed configuration
  remains unverified.
- Capture the public certificate chain actually returned to the integrity caller
  and the RSA/EC alias path, not only Duck's saved imported chain. Hold requester
  and profile constant when comparing signing routes.
- Record actual BASIC, DEVICE and STRONG labels separately from recognition,
  licensing, RKPD provisioning and certificate validation.

The configured ADB tunnel 127.0.0.1:50096 refused connections on 2026-11-09.
A current reachable endpoint was requested. No live verdict request, settings
change, keybox import, flash or relock was performed in this investigation. The
inspected code supplies no verified Tensor equivalent of the direct external-key
signing backend. Full verdict acceptance and that backend remain pending.
