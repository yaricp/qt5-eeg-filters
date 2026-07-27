# Proposal: migrate-to-pyside6

## Why

The app's users are mainly on Windows, but the current delivery (Ubuntu Docker
image + X11 forwarding) does not work there at all, and PyQt5 has no official
Apple Silicon wheels — which forced a parallel macOS pyproject/Dockerfile
stack. Migrating to PySide6 gives official wheels for Windows, macOS
(arm64 + x86_64) and Linux, so the app runs natively everywhere from a single
dependency manifest, and the Docker/X11 workaround can be removed.

## What Changes

- Replace PyQt5 with PySide6 in all 8 GUI modules in `src/`
  (imports, `exec_()` → `exec()`, enum/API adjustments required by Qt6).
- Single `pyproject.toml`: delete `pyproject_macos.toml`; PySide6 replaces
  `pyqt5` as the GUI dependency.
- **BREAKING** (infra only, not behavior): remove Docker-based launch —
  `docker/DockerfileUbuntu`, `docker/DockerfileMacOs`, `docker-compose.yml`,
  `.env`/`.env_linux`/`.env_macos`; `start.sh` becomes a native
  venv launcher (Poetry). App behavior for the user is unchanged.
- First automated test suite: pytest + pytest-qt (offscreen), covering app
  startup wiring and core filter/extremum logic.
- CI (`dev-actions.yml`): run lint + tests on a 3-OS matrix
  (ubuntu / windows / macos) on every push to `dev`. Docker image
  build/publish steps stay untouched in this change (removed in the
  follow-up `package-binaries-ci` change).

## Capabilities

### New Capabilities

- `cross-platform-gui`: the GUI application starts and runs natively on
  Windows, macOS (incl. Apple Silicon) and Linux from one Poetry environment
  with PySide6; no Docker or X server required.
- `ci-testing`: every push to `dev` runs flake8 and the pytest suite
  (GUI tests offscreen) on ubuntu, windows and macos runners.

### Modified Capabilities

<!-- none: openspec/specs/ is empty; this change introduces the first specs -->

## Impact

- Code: `src/main.py`, `src/ui.py`, `src/points.py`, `src/handlers.py`,
  `src/qt5_waiting_spinner.py`, `src/views/*` (3 files) — import/API layer
  only; science modules (`eeg_filters`, `ep_bandpass_filter_selector`,
  `controllers.py`, `models.py`) untouched.
- Dependencies: `pyqt5` → `pyside6`; add dev deps `pytest`, `pytest-qt`.
  pyqtgraph works with PySide6 natively.
- Removed files: `pyproject_macos.toml`, `docker/*`, `docker-compose.yml`,
  `.env*` variants; `scripts/{linux,macos}/install.sh` simplified or removed.
- CI: `dev-actions.yml` test job reworked to 3-OS matrix.
- Local pip packages `eeg-filters` / `ep-bandpass-filter-selector` on PyPI
  are Qt-free — no coordination needed.
