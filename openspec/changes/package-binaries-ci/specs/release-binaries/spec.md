# Spec delta: release-binaries (package-binaries-ci)

## ADDED Requirements

### Requirement: Tagged release produces binaries for three OSes
Pushing a tag matching `v*` SHALL trigger a CI workflow that builds
standalone artifacts with PyInstaller on windows, macos and ubuntu
runners: a one-file `.exe`, a zipped `.app` bundle, and a one-file Linux
binary, and attaches all three to the corresponding GitHub Release.

#### Scenario: Release from tag
- **WHEN** the owner pushes tag `v0.3.0`
- **THEN** GitHub Actions builds the three artifacts and attaches them to
  release `v0.3.0`

#### Scenario: End-user installation
- **WHEN** a Windows user downloads the `.exe` from the release page and
  runs it (accepting the SmartScreen prompt described in README)
- **THEN** the application starts without Python, Docker or any
  preinstalled dependency

### Requirement: Binaries are smoke-tested before publication
Each built artifact SHALL be executed with `--smoke-test` on its build
runner; the release job SHALL fail if any smoke run fails.

#### Scenario: Packaging defect blocks release
- **WHEN** a frozen binary fails its `--smoke-test` run in CI
- **THEN** the workflow fails and no release artifacts are published

### Requirement: README documents unsigned-binary installation
`README.md` SHALL document per-OS download/run steps, including the
SmartScreen (Windows) and Gatekeeper (macOS) prompts for unsigned
binaries, and the owner's pre-release Windows VM check.

#### Scenario: User consults README
- **WHEN** a user opens README installation section
- **THEN** they find download links wording, the "More info → Run anyway"
  SmartScreen path and the macOS right-click-Open instruction

## REMOVED Requirements

### Requirement: Docker image publication to GHCR (implicit, never spec'd)
**Reason**: Docker distribution is obsolete once native binaries exist;
users have no Docker.
**Migration**: Distribution via GitHub Releases binaries;
`dev-actions.yml` keeps only lint+tests; existing GHCR packages remain
but receive no updates.
