# ROM porting handoff

Agent instructions, source provenance, manifests and validation records for the
LineageOS 24 / Android 17 spoofing and Duck integration. The source changes are in
the forks listed in [spoofing-inventory.md](spoofing-inventory.md), all using main.

Read [AGENTS.md](AGENTS.md), [taste.md](taste.md), [memory.md](memory.md),
[tasks.md](tasks.md) and the inventory before continuing. Preserve original authors
and source references. Keep incomplete work and validation limits visible.

The shared stack is committed. Device configuration is available for Pixel 9
(tokay/caimito/zumapro) and Pixel 10 (frankel/muzel/laguna). Imported-key signing,
production CA constraints and consumer acceptance remain unverified on hardware.
The original direct external-key CSR protocol remains unresolved on these targets.
Tokay's user build produced a verified OTA after the recorded
[build fixes](porting/audit/tokay-build-followups.md), now published as follow-up
commits. Frankel compilation remains pending.

## Workspace setup

Start from the LineageOS lineage-24.0 manifest. Use **one** overlay from
[porting/manifests](porting/manifests): pixels.xml includes both families; the
individual overlays include the shared forks and one family's dependencies.
Replace overlapping device-discovery manifests rather than installing duplicates.

For a fresh workspace:

```sh
repo init -u https://github.com/LineageOS/android.git -b lineage-24.0 --git-lfs
mkdir -p .repo/local_manifests
curl -fL https://raw.githubusercontent.com/fruity-lineage/rom-porting/main/porting/manifests/pixels.xml \
  -o .repo/local_manifests/ported-pixels.xml
repo sync
```

The overlay checks this repository out as agent-memory and links its instructions,
memory files and porting directory into the Android root. Edit those files through
either path and commit them in agent-memory. This checkout alone contains no ROM
sources or private keyboxes. Source commit mapping and identical-tree publication
checks are in [publication-commits.json](porting/audit/publication-commits.json).

Do not sync or change source revisions during an active build. Tokay's build fixes
and Frankel's configuration were published from isolated worktrees, preserving
active source checkouts. Frankel's proprietary vendor and kernel dependencies
were not synced or built during this work.

## Acceptance work

Read the [Tokay adapter audit](porting/audit/tokay-duck-import.md) and
[Frankel source audit](porting/audit/frankel-import.md). Tokay's compiled outputs are
recorded separately from the initial static checks. Complete the recorded device checks
before claiming successful signing or consumer acceptance.

The [Tokay runtime verification prompt](porting/audit/tokay-runtime-verification-prompt.md)
can be passed to an AI CLI with access to the workspace and device.

The user's [runtime report](porting/audit/tokay-runtime-report.md) records factory-backed
import success after an override. Use the [follow-up prompt](porting/audit/tokay-runtime-followup-prompt.md)
to resolve the missing installed property, prove targeted-app keybox use and diagnose RKPD HTTP 400.
The later report supplies targeted-app issuer binding; remaining work is persistent
configuration, the invalid RKP boot patch date and the actual checker's failed verdicts.
