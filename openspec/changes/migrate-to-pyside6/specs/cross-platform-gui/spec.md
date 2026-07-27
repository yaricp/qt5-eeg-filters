# Spec delta: cross-platform-gui (migrate-to-pyside6)

## ADDED Requirements

### Requirement: Native start on all supported platforms
The application SHALL start natively (no Docker, no X server) on Windows,
macOS (Intel and Apple Silicon) and Linux using PySide6 from a single
Poetry environment defined by one `pyproject.toml`.

#### Scenario: Start on a supported OS
- **WHEN** a user runs the launcher (`start.sh` on Linux/macOS,
  `start.bat` on Windows) on a machine with Python 3.12+
- **THEN** the Poetry environment is created/reused in-project (`.venv`)
- **AND** the main window opens with the plot area, bandwidth list and
  extremum-region controls, identical in behavior on all three OSes

#### Scenario: Single dependency manifest
- **WHEN** a developer inspects the repository
- **THEN** exactly one `pyproject.toml` exists, listing `pyside6`
  (not `pyqt5`) as the GUI dependency
- **AND** no platform-specific pyproject or env-file variants remain

### Requirement: GUI code uses PySide6 exclusively
All GUI modules SHALL import Qt classes from `PySide6` only; `PyQt5`
SHALL NOT appear anywhere in the codebase.

#### Scenario: No PyQt5 references remain
- **WHEN** the source tree is searched for `PyQt5`, `pyqtSignal`,
  `pyqtSlot` or `exec_(`
- **THEN** zero matches are found in `src/`

### Requirement: Docker-free repository launch path
The repository SHALL NOT contain Docker-based launch infrastructure for
the desktop app.

#### Scenario: Docker launch layer removed
- **WHEN** the repository root is inspected after the change
- **THEN** `docker/`, `docker-compose.yml`, `pyproject_macos.toml` and
  `.env`/`.env_linux`/`.env_macos` are absent
- **AND** `README.md` describes the native launch for all three OSes

## REMOVED Requirements

### Requirement: Docker + X11 launch (implicit, never spec'd)
**Reason**: Docker+X11 delivery served only Linux/macOS and cannot work
for the Windows-based user population.
**Migration**: Use the native launcher (`start.sh` / `start.bat`);
CI-built binaries arrive in the follow-up change `package-binaries-ci`.
