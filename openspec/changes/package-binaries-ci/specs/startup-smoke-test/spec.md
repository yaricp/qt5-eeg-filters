# Spec delta: startup-smoke-test (package-binaries-ci)

## ADDED Requirements

### Requirement: Headless self-check via --smoke-test flag
The application SHALL support a `--smoke-test` command-line flag that runs
a headless self-check: construct the main window offscreen, load a bundled
sample recording, apply one bandpass filter, then exit with code 0 on
success or a non-zero code with a traceback on any failure.

#### Scenario: Successful smoke run
- **WHEN** the application (source or frozen binary) is started with
  `--smoke-test` on a machine without a display server
- **THEN** it prints a PASS message and exits with code 0 without showing
  any window

#### Scenario: Broken bundle is detected
- **WHEN** the frozen binary is missing a required module, Qt plugin or
  the bundled sample data
- **THEN** the smoke run exits with a non-zero code and the failure reason
  appears in output

### Requirement: Sample data bundled with frozen binaries
Frozen binaries SHALL contain a sample recording sufficient for the smoke
test, requiring no external files.

#### Scenario: Smoke test on a clean machine
- **WHEN** the frozen binary runs `--smoke-test` in an empty directory
- **THEN** the check completes using only bundled resources
