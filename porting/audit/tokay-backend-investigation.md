# Tokay signing backend investigation

Updated 2026-11-08 UTC. This is static source and firmware evidence, not successful
device execution or a completed Duck backend.

## Result

The shipped HWBCC service rejects non-secure clients attempting to sign data or obtain
its BCC. This rules out direct HWBCC access from an Android Duck HAL. It does not
establish that every proprietary firmware interface has been exhaustively examined.
Standard imported-key attestation now has a committed Android adapter, described in
[tokay-duck-import.md](tokay-duck-import.md). Tokay selects it and the frontend becomes
available when its hostname and standard services are declared; the master setting is
opt-in. Hardware-key handles remain a separate candidate. Neither route is established
as equivalent to Duck's direct external-key CSR protocol or validated on Tokay hardware.

## Source pins and artifacts

| Project | Inspected revision |
| --- | --- |
| system/security | 123cc4af487922618cd99f28d05736e47eba7b00 |
| system/keymint | cfeefc94bf8c4f19d19dca193d376a1fc05e8e3e |
| trusty/user/app/keymint | 48faccf3fd79ef3bc23171ed9373965e8c302b4c |
| trusty/user/base | 058cbb7314268dd01c13263affc593ed87426b04 |
| vendor/google/tokay | e918e8f50f2e1ae6d882ac972eef42df82e704b0 |
| frameworks/base | b2cb692a58995923598768877c0397cdd980a166 |

The proprietary payloads come from `vendor/google/tokay/radio/tzsw.img`.
[tokay-trusty-selected.json](tokay-trusty-selected.json) records their extraction bounds
and image identity. Rechecked selected-payload SHA-256 values:

- HWBCC: `52ef0192939b2c674205ba1743e430db35417dd7e999854673162fa65c198aca`.
- Apploader: `ef0fc083190f7679a2eb84681edc703461fa01f07bc760033c93445c9fd74a48`.

## Shipped HWBCC access control

Addresses are link-time virtual addresses in the extracted HWBCC ELF. Relevant
sections have matching file offsets in this artifact. These are not runtime addresses
or offsets into the complete firmware image.

The callback table at `0x68160` contains:

| Operation | Callback entry | Implementation |
| --- | --- | --- |
| Initialize session | 0x39b18 | 0x63860 |
| Close session | 0x39c98 | 0x63a30 |
| Sign data | 0x39b00 | 0x39cd0 |
| Get BCC | 0x39b08 | 0x39df4 |
| Get DICE artifacts | 0x39b10 | 0x39f30 |
| Deprivilege non-secure clients | 0x39b20 | 0x63a18 |

Initialization copies the accepted peer UUID to `session + 0x100` at
`0x63890`/`0x63898`. Signing loads it at `0x39ce0` and branches on an all-zero
UUID at `0x39cf4`, before selecting production or test signing. The rejection logs
`NS world attempted to sign key` from `0x28b9` and returns `-43` at `0x39d30`.

The BCC callback likewise loads the peer at `0x39e08`, branches at `0x39e18`,
logs `NS world attempted to get BCC` from `0x1ffd`, and returns `-43`.
Production paths explicitly compare KeyMint's UUID
`5f902ace-5e5c-4cd8-ae54-87b88c22ddaf` and select GSA use case zero. Widevine
gets a different use case. Non-secure DICE-artifact retrieval is a distinct operation;
it does not establish access to the KeyMint BCC or signing identity.

`trusty/user/base/lib/tipc/tipc_srv.c` obtains the peer through `accept()` and passes
it to session initialization. The HWBCC request contains no caller-UUID field.
Changing an Android SELinux rule or request context does not supply KeyMint's trusted
identity. Generic AOSP sample behavior was not substituted for firmware evidence.

Inspection used `llvm-objdump -d --no-show-raw-insn` with bounded address ranges.
Payload-hash and exact callback-table assertions passed. No live HWBCC call was made.

## Shipped app-loader constraints

The apploader's verification call at `0x3d748` has a failure branch at `0x3d750`,
referencing `Signature check failed` at `0x3d784`. Its signing-key lookup at
`0x6fc14` recognizes IDs 0, 1, 10 and 100. The table at `0x73700` requires the
app-loading-unlocked state for IDs 1 and 100. Restricted UUID lists for IDs 10 and
100 exclude KeyMint's UUID.

`SYSTEM_STATE_FLAG_APP_LOADING_UNLOCKED` controls developer app loading. Android
bootloader unlock alone is not evidence that this flag is enabled, a signing key is
usable, or a replacement KeyMint TA can load. No replacement TA was packaged, flashed
or loaded, and no firmware signature or policy check was bypassed.

## Standard KeyMint alternatives

- `system/keymint/ta/src/rkp.rs:261` verifies public-key MACs and returns
  `InvalidMac` on mismatch. `trusty/user/app/keymint/rpc.rs:73` computes the MAC
  with a secure-side ephemeral key. Standard RKP generates non-exportable hardware
  keys; a fabricated external-key MAC is not equivalent.
- `system/keymint/ta/src/keys.rs:326` accepts an optional attestation key for
  import and uses common certificate creation. Attestation records the actual
  imported origin and boot state. This is issuance inside KeyMint, not direct
  external-key CSR certification by the RKP server.
- At the initial system/security revision above, `security_level.rs:817` ignores its
  `_attestation_key` argument and passes `None` to `IKeyMintDevice.importKey` at
  line 870. Unlike generation, it does not select an RKPD key or append its chain.
  This integration gap is now fixed in local commit cc1f9e42200d3e9c7a1aa47e433bd72023162002.
- Hardware-key handles require changes to the current software-keybox consumers;
  standard RKP does not supply Duck's exportable private key.
- `DuckRkpCertificates.java:137` requires certificate-signing usage and sufficient
  CA path length to issue another application leaf. Imported attestation keys add
  an intermediate CA; production parent constraints and full PKIX validation remain
  unverified. VTS `ChainSignaturesAreValid` verifies signatures and issuer names,
  not those path-length constraints.

No production chain or successful Tokay imported-key attestation was obtained. The
Android adapter is a source implementation awaiting runtime acceptance. Exact external-key
CSR signing still requires a supported secure-side extension and an authenticated,
loadable implementation; the import adapter does not bypass those firmware constraints.

## Access and remaining validation

Workspace create/read/delete and GitHub HTTPS now pass. ADB network access is allowed,
but configured and default local endpoints refuse connections. The user connects over
remote SSH; hardware access requires an ADB server reachable from this server, such
as one forwarded from the user's local device host. No device enumeration succeeded.

The firmware evidence above remains unchanged. Four follow-up Android source commits
add the import adapter, Keystore fix, device configuration and scoped property policy.
Five final Java parses, two Rust rustfmt checks, 99 source hashes and static preflight
pass. Compiler/linker checks, compiled SELinux, Android/native regressions, production
CA acceptance and Tokay hardware validation remain pending.
