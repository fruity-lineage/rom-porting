# Tokay integrity runtime and source checkpoint

2026-11-09. BASIC, DEVICE and STRONG passing remains unachieved.

The restored ADB tunnel reached Tokay build 1794188022 on slot B. The bootloader
remains unlocked/orange. The initial owner PIF configuration was absent and native
staging properties were blank. The existing Settings picker fetched and saved its
recommended Pixel 6a Canary profile, then restarted GMS. Profile loading and
certificate-generation/update hooks were observed. The installed allocator image
is still the earlier VA39 kernel; hardened_malloc source activation is separate.

Three fresh checker requests (initial state, restored profile, and a reversible
provider-enabled comparison) each omitted deviceRecognitionVerdict and returned
UNEVALUATED app recognition/licensing. Their decoded timestamps differ. The
provider block armed in the comparison; its setting was restored afterward. No
account/application data was cleared. Third-party decoded responses do not
independently verify Google token authenticity or requester label configuration.

The public Keystore2 certificate metadata for Vending's integrity request alias
contains six certificates. The EC leaf claims locked/verified and is signed by
Duck's imported EC signer. That Google-signed intermediate records unlocked/orange,
zero boot key and imported origin. All chain signatures, including the root
self-signature, verify. Reading stored caller metadata establishes the available
chain, not a capture of what Google's server received or its exact rejection logic.

A disposable RSA key confirms EC-issuer fallback works: its RSA public leaf has an
ECDSA signature, the same six-certificate path verifies, and the probe alias was
deleted. The missing-RSA parsing warning therefore is not an algorithm-support
blocker on this installed path. The normal integrity alias sampled here was EC.

The post-profile Vending leaf still contained real Tokay/Pixel 9 device IDs while
PIF was configured for bluejay/Pixel 6a. Generated leaves populate those requested
IDs from preloaded Build attestation constants; the existing verified-issuer guard
then skips re-signing them on retrieval. The new source correction applies the
existing PIF identity mapping before signing in eligible DG/Vending processes,
without adding unrequested identity tags or changing the retrieval guard.

Published and activated source corrections:

- frameworks/base: 9413fe868c27b3410c054f9a4666eb5d521501fa resets omitted/cleared/
  malformed flags, honors the owner System PIF enable switch, stages native identity
  and coalesces GMS restarts after config/enable changes.
- frameworks/base: 4c9ed082169abc5dab5391eca7b3b3ffe3defae7 applies requested PIF
  identity fields before generated certificate signing.
- packages/apps/Settings: 31eae4cc1336dd3960acb9c14543df001dc1acf3 delegates
  PIF restarts to the framework observer and retains the optional data-wipe prompt.

All three commits preserve porter identity and original contributor credit. Static
Java/Kotlin syntax, whitespace, file hashes and scoped Tokay preflight pass. Thirteen
Android regressions were added and remain unexecuted. No production Android/kernel
build or flash was performed. Sources were integrated after checking that no evox
build was running; the separate aospa build and pre-existing Soong edits were preserved.

The signing backend remains unresolved. Inspected Trusty/shared KeyMint sources do
not provide a supported Android route to an exportable Google-certified signer
without a real BootInfo intermediate. ATTEST_KEY purpose prevents arbitrary signing;
CSR keys require hardware MAC authentication; BootInfo configuration is one-shot;
factory provisioning consumes supplied certificates and is trusted-policy gated.
These bounded source findings do not prove that no firmware vulnerability can exist.
A rebuild of these integration fixes cannot itself remove the signed boot-state
record or guarantee all requested labels.

See tokay-integrity-live-20261109.json, tokay-pif-reload-verification.json,
tokay-pif-identity-verification.json and tokay-pif-source-activation.json for scoped
facts and validation. No private keybox/key, nonce, signed token or account identity
is included in this handoff.
