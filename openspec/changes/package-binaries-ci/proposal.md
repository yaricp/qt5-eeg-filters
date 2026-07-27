# Proposal: package-binaries-ci

## Why

After `migrate-to-pyside6` the app runs natively everywhere, but users —
mainly neurophysiologists on Windows without Python or Docker — still have
no way to install it. CI-built standalone binaries downloadable from GitHub
Releases turn installation into "download → double-click", and the now
purposeless Docker image publication can be removed.

**Depends on:** `migrate-to-pyside6` (must be implemented first).

## What Changes

- Add a `--smoke-test` CLI flag to the app: starts offscreen, loads a
  bundled sample recording, applies one filter, exits 0 on success.
- PyInstaller packaging: committed spec file producing a one-file `.exe`
  (Windows), a `.app` bundle zip (macOS), a one-file binary (Linux).
- New release workflow (tag `v*`): 3-OS matrix builds binaries, runs each
  frozen binary with `--smoke-test`, attaches artifacts to a GitHub
  Release.
- **BREAKING** (infra only): remove Docker image build/publish to GHCR
  from `dev-actions.yml` and `main-actions.yml`.
- README: download/run instructions per OS, incl. SmartScreen (Windows)
  and Gatekeeper (macOS) notes for unsigned binaries — signing is
  deliberately skipped (cost; accepted by owner).

## Capabilities

### New Capabilities

- `startup-smoke-test`: the application supports a `--smoke-test` flag
  that exercises startup, sample-data load and filtering headlessly and
  reports success via exit code.
- `release-binaries`: tagged releases carry CI-built, smoke-tested
  standalone binaries for Windows, macOS and Linux on GitHub Releases.

### Modified Capabilities

<!-- none: ci-testing (from migrate-to-pyside6) covers lint+tests and is
     unchanged; Docker publication was never spec'd -->

## Impact

- Code: `src/main.py` (flag handling only); no logic changes.
- New files: PyInstaller spec, `release-actions.yml` workflow, `start.bat`
  already exists from previous change.
- Removed: Docker build/publish jobs in both workflows; GHCR references.
- Dependencies: `pyinstaller` as dev dependency.
- Final gate: owner verifies the Windows `.exe` manually in a Windows VM
  before publishing the first release.
