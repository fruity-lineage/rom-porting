# Workspace instructions

Read `taste.md`, `memory.md`, `tasks.md`, and `spoofing-inventory.md` before continuing work.
Treat these as persistent handoff notes; verify relevant facts against the current sources.
Read any more specific `AGENTS.md` before working in a subdirectory.

This is an Android Repo workspace, not a single Git repository. Run Git commands in the
affected project. Preserve existing changes, use topic branches, and make clean commits
for the authorized feature ports. Record the project, commit, and validation in the inventory.

For Tokay, start with `device/google/caimito`; `device/google/tokay` is a wrapper.
Trace shared `zumapro` configuration and the separate GS 6.1 kernel workspace as needed.
The kernel workspace has its own instructions and Repo metadata.
For Frankel, start with device/google/muzel; device/google/frankel is a wrapper.
Trace shared laguna configuration and its separate GS 6.6 kernel dependencies.
Keep device evidence separate; one device's firmware findings do not prove another's behavior.

Search and read before adapting code. Follow the whole feature from its UI and configuration
through framework callers, interfaces, native services, vendor integration, and SELinux.
Check the target platform's implementation before reusing transport or trusted-app code.

Keep durable preferences in `taste.md`, verified setup and findings in `memory.md`, current
progress in `tasks.md`, and source provenance and port validation in `spoofing-inventory.md`.
Update these after meaningful changes. Distinguish completed work from pending work and
verified behavior from assumptions. Keep credentials and transient command dumps out of memory.

Selecting an Android lunch target can invoke the kernel build. Use explicit, scoped
validation commands when checking a port; do not invoke lunch merely to inspect configuration.

The handoff is published in fruity-lineage/rom-porting on main. In a synced
Android workspace, agent-memory is its Git checkout and root notes/porting can be
links into it. If opened alone, this repository is documentation and tools, not the
Android source workspace. Run source Git commands in the actual Android projects.
Read porting/audit/publication-commits.json and porting/manifests/tokay.xml for the
published revisions. Preserve upstream authors and fuzailmansuri's coauthor credit.
Only ported work is authorized for publication; unrelated pre-existing edits are excluded.
Preserve a running build's inputs. Use isolated worktrees for additional device work,
and do not switch the active workspace's manifests or source revisions during a build.
