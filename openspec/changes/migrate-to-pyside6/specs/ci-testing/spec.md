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

### Requirement: GUI interaction wiring is covered by tests
The test suite SHALL cover the interaction wiring between pyqtgraph items,
Qt widgets and the model: search-region changes, bandwidth checkboxes,
curve clicks and the custom draggable point item.

#### Scenario: Region change propagates to edits and model
- **WHEN** a test moves a search region via `setRegion()` (which emits the
  same signal as a finished mouse drag)
- **THEN** the corresponding start/end line-edits and the model's search
  range reflect the new boundaries, and extremums are recomputed

#### Scenario: Line-edit change propagates to region
- **WHEN** a test enters a new boundary value into a start/end line-edit
- **THEN** the corresponding region on the plot moves to match

#### Scenario: Bandwidth checkbox toggles curve visibility
- **WHEN** a test clicks a bandwidth checkbox (real `qtbot.mouseClick`)
- **THEN** the corresponding curve's visibility changes accordingly

#### Scenario: Custom draggable item reacts to drag events
- **WHEN** a test invokes `mouseDragEvent` on the custom item from
  `points.py` with a fabricated event
- **THEN** the item's position updates as the handler prescribes

### Requirement: Synthetic mouse-drag integration tests on migrated stack
After the PySide6 migration is green, the suite SHALL include 2–3
integration tests that drag plot regions with synthetic QMouseEvents
(data-to-pixel mapping through the viewbox) to validate the full
mouse-to-model chain offscreen.

#### Scenario: Synthetic drag moves a region
- **WHEN** a synthetic press-move-release sequence is sent to the plot
  viewport across a region boundary at a fixed window size
- **THEN** `getRegion()` returns moved boundaries and the line-edits/model
  update as in a human drag

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
