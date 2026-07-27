# Changes

Active OpenSpec change folders, one per task: `changes/<task-id>/`.

A change folder contains `proposal.md`, `tasks.md`, optional `design.md`,
and spec deltas under `specs/`. Start a change with `/opsx:propose`,
implement with `/opsx:apply`, then `/opsx:archive` to fold the deltas into
`openspec/specs/` and move the folder to `changes/archive/`.

Changes are committed and pushed so specs can be reviewed on GitHub
alongside the code they describe.
