# User preferences and requirements

Recorded from this workspace conversation on 2026-11-08.

- Search and read the upstream sources before acting. Tokay's shared Pixel setup needs tracing.
- Port the full connected feature stack, including framework, vendor, UI, SELinux, apps,
  settings, HALs, and Trusty dependencies where they actually participate.
- The target is LineageOS for Tokay; Evolution X supplies the spoofing and Duck RKP references.
- Make clean commits for the code changes.
- Keep agent memory in this workspace, including this exact `taste.md` filename.
- Verify changes and update the Markdown handoff afterward; record validation limits honestly.
- Complete the Tokay backend as far as evidence and access permit; UI wiring alone is insufficient.
- Publish only ported work under fruity-lineage, using main as each default branch.
- Preserve original upstream authors, credit fuzailmansuri as coauthor on adapted ports,
  and include source commit references. Keep the agent handoff in its own repository.
- Use device-neutral GitHub descriptions and the shared rom-porting handoff.
- Carry the shared stack to Pixel 10 frankel too, with its own source and hardware evidence.
- Preserve active build inputs and isolate other device changes in worktrees.
- Enabled device RKP should restore, provision and renew automatically at boot without
  opening Settings. Generate the Duck key locally; do not download a premade keybox.
- Port GrapheneOS hardened_malloc as a connected allocator, libc, build and kernel change.
- Every new commit for the hardened_malloc port must start its subject with `malloc:`,
  including dependency wiring, kernel patches and handoff documentation. Keep inherited
  upstream history and authorship intact.

Add preferences when the user states them. Keep task-specific discoveries in `memory.md`
and `spoofing-inventory.md`.

- A published feature port must be distinguished from one installed in the active
  build tree. After preserving any running build, finish the active source integration
  and report separately whether the ROM was rebuilt and validated on hardware.
