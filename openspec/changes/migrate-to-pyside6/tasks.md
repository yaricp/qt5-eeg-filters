# Tasks: migrate-to-pyside6

## 1. Test infrastructure first (TDD)

- [ ] 1.1 Add dev deps `pytest`, `pytest-qt` to pyproject.toml; create
      `tests/` with `conftest.py` setting `QT_QPA_PLATFORM=offscreen`
- [ ] 1.2 Write `tests/test_filters.py` (Chebyshev filter on `data/data1.txt`:
      shape + numerical sanity) — must pass on current PyQt5 code
- [ ] 1.3 Write `tests/test_extremum_search.py` (known curve → known
      extremums) — must pass on current PyQt5 code
- [ ] 1.4 Write `tests/test_app_starts.py` with pytest-qt (`MainWindow`
      constructs, view shows, key widgets exist) — passes on PyQt5,
      guards the migration
- [ ] 1.5 Write `tests/test_interactions.py` (level 1, API-driven):
      `setRegion()` → line-edits + model sync; line-edit input → region
      moves; bandwidth checkbox click toggles curve; select-all;
      curve `sigClicked` — all pass on PyQt5
- [ ] 1.6 Write `tests/test_points_drag.py` (level 3): custom item from
      `points.py` — `mouseDragEvent(fake_event)` updates position —
      passes on PyQt5

## 2. PySide6 migration

- [ ] 2.1 Switch `pyproject.toml`: `pyqt5` → `pyside6`; `poetry lock`,
      `poetry install`; delete `pyproject_macos.toml`
- [ ] 2.2 Migrate imports `PyQt5` → `PySide6` in all 8 files;
      `pyqtSignal`/`pyqtSlot` → `Signal`/`Slot`; `exec_()` → `exec()`;
      move `QAction` imports to `QtGui`
- [ ] 2.3 Fix Qt6 enum scoping and any API breaks until
      `tests/test_app_starts.py` passes offscreen
- [ ] 2.4 Manual GUI check on macOS (developer machine): open file from
      `data/`, apply filter, drag regions, save results
- [ ] 2.5 Verify zero `PyQt5|pyqtSignal|pyqtSlot|exec_(` matches in `src/`

## 3. Synthetic mouse-drag tests (level 2, on migrated stack)

- [ ] 3.1 Add ~20-line drag helper (data→pixel via
      `viewbox.mapViewToScene()`, QMouseEvent press/move/release to
      plot viewport), fixed window size in fixture
- [ ] 3.2 Write 2–3 integration tests: synthetic drag of max/min region
      boundary and body → `getRegion()`, line-edits and model update

## 4. Delivery cleanup

- [ ] 4.1 Rewrite `start.sh` as native launcher (ensure `.venv` via
      poetry, run `src/main.py`); add `start.bat` for Windows
- [ ] 4.2 Delete `docker/`, `docker-compose.yml`, `.env`, `.env_linux`,
      `.env_macos`; remove/simplify `scripts/linux`, `scripts/macos`,
      `scripts/test_start_with_docker.sh`
- [ ] 4.3 Update `README.md`: native install/run for Windows, macOS,
      Linux; drop Docker instructions

## 5. CI matrix

- [ ] 5.1 Rework `dev-actions.yml` test job: matrix
      ubuntu/windows/macos-latest, setup-python 3.12, poetry install,
      flake8 (ubuntu only), `poetry run pytest` (leave Docker publish
      jobs untouched — removed in next change)
- [ ] 5.2 Push to `dev`, verify all three matrix jobs green; fix
      runner-specific issues if any

## 6. Wrap up

- [ ] 6.1 Update `openspec/project.md` conventions (PySide6, pytest
      active in CI) and `openspec/config.yaml` context
- [ ] 6.2 Verification: full test suite green locally + CI; manual GUI
      smoke on macOS; ready for review
