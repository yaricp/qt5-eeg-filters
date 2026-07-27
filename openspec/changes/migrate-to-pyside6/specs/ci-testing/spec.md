# Spec delta: ci-testing (migrate-to-pyside6)

## ADDED Requirements

### Requirement: Automated test suite exists and passes
The project SHALL have a pytest test suite covering application startup
(pytest-qt, offscreen) and core signal-processing logic, runnable locally
with `poetry run pytest`.

#### Scenario: App startup test
- **WHEN** the test suite runs with `QT_QPA_PLATFORM=offscreen`
- **THEN** a test constructs `MainWindow`, shows the view and asserts the
  main widgets and signal connections exist, without a display server

#### Scenario: Filter logic test
- **WHEN** the filter test runs on a sample recording from `data/`
- **THEN** applying a Chebyshev bandpass filter yields output of the same
  shape with expected numerical characteristics

#### Scenario: Extremum search test
- **WHEN** the extremum-search test runs on a curve with known extremums
- **THEN** the found maximum/minimum positions match the known values

### Requirement: CI runs lint and tests on a three-OS matrix
Every push to `dev` SHALL trigger a CI job matrix on ubuntu, windows and
macos runners that installs the project with Poetry and runs the test
suite; flake8 SHALL run at least on ubuntu.

#### Scenario: Push to dev
- **WHEN** a commit is pushed to `dev`
- **THEN** GitHub Actions runs `poetry install` and `poetry run pytest`
  on ubuntu-latest, windows-latest and macos-latest
- **AND** the workflow fails if any OS job fails

#### Scenario: Test step is mandatory
- **WHEN** the workflow file is inspected
- **THEN** the pytest step is active (not commented out) and required
  for the workflow to succeed
