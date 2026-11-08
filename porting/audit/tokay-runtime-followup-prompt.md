# Tokay runtime follow-up prompt

Run this on the local host that can reach Tokay. The SSH server currently cannot
reach that host's ADB daemon.

```text
Continue the Tokay Duck verification. Read AGENTS.md and the persistent notes,
then porting/audit/tokay-runtime-report.md and the initial verification prompt.

The earlier report established factory-backed TEE import attestation after a
runtime property override. RKPD failed with HTTP 400. Ordinary app_process
Keystore tests did not establish that an app used the imported Duck keybox.
The later installed-app probe reports the expected five-certificate chain
and exact Duck issuer binding. Focus now on the actual checker showing crosses,
configuration persistence and the invalid boot patch date.

First identify the failing app/screen and every failed label. If it is Play
Integrity, capture the sanitized actual verdict/error and distinguish an API
request failure from a valid integrity rejection. If it is a certificate
checker, capture its failed validation/revocation fields. Do not infer remote
acceptance from the local injected-chain probe or identify a cause from icons alone.

1. Diagnose the missing persistent selection property before changing source.
   Record the exact flashed OTA SHA-256, active boot slot, mounted product path,
   /product/etc/build.prop SHA-256 and its selection-property line. Identify
   how the earlier runtime override was applied and its original value.
   Compare with this server's verified evidence:
   OTA SHA-256:
   55f7a4cec8e04562628351d9c685159a864b4d77470aad320a521129d1c86852
   Product/etc/build.prop SHA-256:
   f8229a2e54274f52f60832cef304ee6551b4ad20298b8a5e2c1ef9963f87b859
   Actual device configuration:
   device/google/caimito/device-tokay.mk already contains
   PRODUCT_PRODUCT_PROPERTIES += ro.lineage.duckrkp.trusty_import=true.
   It is inherited by caimito/lineage_tokay.mk through aosp_tokay.mk.
   Do not add a duplicate to an unused device/google/tokay wrapper file.
   If the OTA matches but mounted contents differ, investigate the active
   image/slot and flashing procedure. If contents contain the property but
   getprop is empty, investigate init loading and overrides. Report evidence
   before proposing a persistent fix. Do not flash or reboot without my instruction.

2. Prove actual Duck use with a disposable installed app in a real package
   and app UID. Record its effective TrickyStore target policy and enablement.
   Preserve the previous policy and restore it after the test.
   Generate a fresh key/challenge through the normal Android Keystore API.
   Extract only public certificate metadata from the active Duck keybox
   on-device; never print or export its XML or private key.
   Require returned cert[1] to match the active imported Duck certificate
   by DER hash, verify cert[0]'s signature using that issuer's public key,
   verify the challenge and complete chain, including all CA path lengths.
   With the reported four-certificate keybox, expect the normal hooked app
   chain to have five certificates; explain any difference from actual code.
   Repeat with an untargeted control and compare issuer hashes. A valid
   factory chain or a root app_process probe alone is insufficient.

3. Reproduce and locate RKPD HTTP 400. Collect the failing operation,
   service/instance, timing and sanitized server error reason. Do not dump
   device CSRs, credentials, private keys or device identifiers into notes.
   Use the standard remote_provisioning diagnostics to distinguish an RKP
   service failure from import/signing failure. Preserve factory fallback
   and certificate validation. Do not call factory fallback an RKPD pass.
   The supplied signCertificates error already identifies
   boot_patch_level=20000000 as an invalid date. Trace the actual boot-info
   source in the shipped firmware/boot flow. Current caimito source sets
   BOOT_SECURITY_PATCH=2026-10-05 and adds an AVB boot security-patch property.
   Compare the installed boot image and metadata rather than assuming the
   bootloader/header hypothesis is proven. Do not fabricate a date or edit
   a CSR to hide the failure.

4. Exercise cancellation, failure cleanup, temporary alias cleanup,
   actual secondary-user restrictions and renewal where practical.
   Restore test policies/toggles and remove disposable probes. Explain
   any runtime property override that remains and how persistence should
   be checked after a user-authorized reboot.

You may build/install a small disposable test APK. Do not rebuild the ROM
or kernel, switch source revisions, change manifests or weaken validation.
Update the Markdown handoff with sanitized evidence. Mark each check
PASS, FAIL, BLOCKED or NOT RUN. Distinguish factory import success, actual
Duck keybox use, successful RKPD issuance and remote consumer acceptance.
```
