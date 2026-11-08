# Tokay runtime verification prompt

Copy the following prompt into the AI CLI on the SSH server. The phone must be
reachable through ADB; the prompt includes diagnosing a missing connection.
This is a verification plan, not a record of completed hardware tests.

```text
Verify the Duck RKP integration on my Tokay using actual device tests.

Workspace: /serverhive4/fruitzail/evox
Published handoff: https://github.com/fruity-lineage/rom-porting

Read AGENTS.md, taste.md, memory.md, tasks.md, spoofing-inventory.md,
porting/audit/tokay-duck-import.md and
porting/audit/tokay-build-followups.md. Verify their claims against current sources.

The ROM has built successfully. Hardware signing remains unverified.
Tokay uses the standard Trusty KeyMint import-attestation adapter;
the original Qualcomm external-key CSR protocol is unresolved.

1. Establish ADB access. Try the existing ADB server and the previously
   configured endpoint 127.0.0.1:50096. Select Tokay explicitly if multiple
   devices appear. If unreachable, give me the exact SSH tunnel command
   to run on the computer with the phone attached.

2. Confirm the phone is running the intended ported build. Inspect:
   - ro.lineage.duckrkp.trusty_import (expected true)
   - remote_provisioning.hostname
   - Keystore2, Trusty KeyMint, RKP and RKPD service availability
   - SELinux enforcement and relevant denials.
   Do not treat the spoofed fingerprint alone as build identity evidence.

3. Trace the actual Duck entry points in Settings and framework source.
   Test provisioning from the owner's profile through supported entry
   points. Record availability, enablement, progress, completion and
   exact failure codes. Capture relevant DuckRkp, Keystore2 and RKPD logs.
   An ordinary RKP "certify" command succeeding does not prove Duck works.

4. Verify the real import path:
   software P-256 key -> TEE import as ATTEST_KEY -> selected attestation
   issuer -> returned certificate chain -> Duck validation -> stored keybox.
   Check public-key binding, challenge, security level, imported origin,
   issuer signatures, trusted root, validity, BasicConstraints, key usage
   and every CA path-length constraint. Identify whether the issuer came
   from RKPD or factory fallback.

5. Demonstrate actual use of the resulting keybox: issue a fresh test
   attestation and independently verify its certificate signatures,
   challenge and chain. Separately test ordinary Android Keystore
   generation/signing to detect regressions. Check failure handling,
   temporary alias cleanup and cancellation. Test secondary-user
   restrictions and renewal where practical; mark untested cases honestly.
   You may build/install a small disposable test probe if needed.
   Do not rebuild the ROM or kernel.

6. Preserve existing keyboxes and restore any toggles changed for testing.
   Never print or upload private keys or complete keybox XML.
   Keep active source revisions and manifests unchanged.
   Record results and sanitized evidence in the persistent Markdown notes.

Report PASS, FAIL or BLOCKED for each stage, with observed evidence.
If anything fails, identify the first failing layer and propose a concrete
fix based on the error and target implementation. Do not weaken certificate
validation to obtain a pass. Distinguish successful provisioning/signing
from acceptance by apps or remote integrity services.
```
