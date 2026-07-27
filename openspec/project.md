# Project Context — qt5-eeg-filters

## Purpose

Desktop PyQt5 GUI for filtering EEG / evoked-potential (EP) signals.
Loads EEG recordings (ASCII export from NeuroExplorer 4.4), plots curves
with pyqtgraph, applies Chebyshev bandpass filters over a configurable list
of bandwidths, searches signal extremums inside movable plot regions, and
exports results. Domain: neurophysiology research tooling.

## Tech Stack

- Python 3.12, Poetry (in-project `.venv`)
- PyQt5 + pyqtgraph (GUI and plotting)
- scipy / numpy / pandas (signal processing), pyedflib, matplotlib, loguru
- Author's own pip packages: `eeg-filters` (Chebyshev filters, import/export)
  and `ep-bandpass-filter-selector` (optimal passband search).
  Git-ignored local dev copies live in `src/eeg_filters/` and
  `src/ep_bandpass_filter_selector/`.

## Code Layout

All application code is in `src/` (flat modules, MVC-like):

- `main.py` — MainWindow: wires everything, connects Qt signals to handlers
- `models.py` — `Config`, `ModelData`
- `views/` + `ui.py` — main plot window, selector windows
- `controllers.py` — `Controller`, `PassbandSelector`
- `handlers.py` — all UI event handlers
- `settings.py` — bandwidth list, Chebyshev order/ripple, search ranges

## Conventions

- Spec-driven development: every non-trivial change starts as an OpenSpec
  change in `openspec/changes/<task-id>/` (proposal → tasks → apply →
  archive). Specs are committed and reviewed on GitHub together with code.
- TDD: tests are written before implementation. Test runner: pytest
  (CI step currently commented out in `.github/workflows/dev-actions.yml` —
  enable it once the first tests land).
- Lint: flake8 (enforced in CI), ruff available as dev dependency.
- Branches: work on `dev`, merge to `master`. Push to `dev` triggers CI:
  lint → Docker image build → push to GitHub Container Registry.
- Always use the project-local `.venv` (Poetry), never global installs.
- Run locally: `./start.sh` (env from `.env`/`.env_linux`/`.env_macos`);
  Docker: `docker-compose.yml` with X11 forwarding.
