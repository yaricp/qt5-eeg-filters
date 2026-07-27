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

## 3. Delivery cleanup

- [ ] 3.1 Rewrite `start.sh` as native launcher (ensure `.venv` via
      poetry, run `src/main.py`); add `start.bat` for Windows
- [ ] 3.2 Delete `docker/`, `docker-compose.yml`, `.env`, `.env_linux`,
      `.env_macos`; remove/simplify `scripts/linux`, `scripts/macos`,
      `scripts/test_start_with_docker.sh`
- [ ] 3.3 Update `README.md`: native install/run for Windows, macOS,
      Linux; drop Docker instructions

## 4. CI matrix

- [ ] 4.1 Rework `dev-actions.yml` test job: matrix
      ubuntu/windows/macos-latest, setup-python 3.12, poetry install,
      flake8 (ubuntu only), `poetry run pytest` (leave Docker publish
      jobs untouched — removed in next change)
- [ ] 4.2 Push to `dev`, verify all three matrix jobs green; fix
      runner-specific issues if any

## 5. Wrap up

- [ ] 5.1 Update `openspec/project.md` conventions (PySide6, pytest
      active in CI) and `openspec/config.yaml` context
- [ ] 5.2 Verification: full test suite green locally + CI; manual GUI
      smoke on macOS; ready for review
