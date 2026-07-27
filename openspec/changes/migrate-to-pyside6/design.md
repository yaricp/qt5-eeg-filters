# Design: migrate-to-pyside6

## Context

All application code lives in `src/` as flat MVC-like modules. Qt is touched
only by an import/API layer: 8 files, 18 `PyQt5` import lines, one `exec_()`
call, no deprecated APIs found (`QRegExp`, `QDesktopWidget` — zero hits).
Science modules are Qt-free. Platform specificity today lives entirely in
delivery: two pyprojects, two Ubuntu-based Dockerfiles, X11 forwarding,
per-OS env files. There are no automated tests yet (CI test step is
commented out).

## Goals / Non-Goals

**Goals:**
- App starts natively on Windows, macOS (arm64), Linux from one
  `pyproject.toml` via Poetry + PySide6.
- First pytest/pytest-qt suite; tests run in CI on a 3-OS matrix.
- Delete the Docker/X11 delivery layer and duplicated configs.

**Non-Goals:**
- No binary packaging / GitHub Releases (next change:
  `package-binaries-ci`).
- No removal of Docker image publication from CI yet (same next change).
- No refactoring of app logic, no new features, no Qt6 visual polish.
- No pip-packaging of this app (explicitly rejected by the owner).

## Decisions

1. **PySide6 over PyQt6.** Both are API-near-identical for this codebase.
   PySide6: LGPL (no GPL obligations), maintained by the Qt Company,
   official wheels for all three OSes incl. Apple Silicon. pyqtgraph
   supports it via its Qt abstraction. Alternative PyQt6 (GPL/commercial)
   offers no technical advantage here.

2. **Import style: `from PySide6.QtWidgets import ...`** — mechanical
   replacement of `PyQt5` → `PySide6`, keeping the existing per-class
   import style of the codebase. Alternative (pyqtgraph's `Qt` shim or
   `qtpy` abstraction layer) adds indirection for no benefit once we
   commit to one binding.

3. **Signal API**: `pyqtSignal`/`pyqtSlot` → `Signal`/`Slot` (PySide
   naming). Grep: 17 usages (incl. `QAction`) in `ui.py` and `views/*`.

4. **Qt6 enum scoping**: Qt6 requires fully-qualified enums
   (e.g., `Qt.AlignmentFlag.AlignCenter`). Fix them as they surface;
   the offscreen GUI tests are the detection net.

5. **TDD order**: write the test skeleton first against PyQt5 (red on
   import of PySide6-based app), then migrate module-by-module until
   green. Tests use `QT_QPA_PLATFORM=offscreen` so they run headless on
   all CI runners without a display server.

6. **Test scope for this change** (deliberately minimal):
   - `test_app_starts`: `MainWindow` constructs, view shows, signals
     connected (pytest-qt `qtbot`).
   - `test_filters`: Chebyshev filter application on `data/data1.txt`
     produces expected shape/values (pure logic, no GUI).
   - `test_extremum_search`: extremum search over a known curve returns
     known points.
   Deeper GUI interaction tests are follow-up work, not this change.

7. **`start.sh` becomes a thin native launcher**: check `.venv` exists
   (else `poetry install`), then `poetry run python src/main.py`. Per-OS
   install scripts collapse into it; Windows users get `start.bat` with
   the same two steps.

8. **CI matrix**: `runs-on: ${{ matrix.os }}` over
   `[ubuntu-latest, windows-latest, macos-latest]`; steps: checkout →
   setup-python 3.12 → install poetry → `poetry install` → flake8
   (ubuntu only) → pytest. The existing Docker build/publish jobs remain
   as-is in this change to keep the diff reviewable.

## Risks / Trade-offs

- [PySide6 subtle API differences beyond imports (e.g., `QAction` moved
  to `QtGui`, default args in signals)] → offscreen GUI test catches
  startup breakage; migrate module-by-module.
- [pyqtgraph version compatibility with PySide6] → pin pyqtgraph
  `^0.13.7` (declared PySide6 support); startup test exercises the plot.
- [Windows CI runner quirks (paths, Qt plugins)] → `--smoke-test`-style
  startup test in offscreen mode; if a runner-specific failure appears,
  document and gate on it rather than skip.
- [Users who relied on Docker launch] → none known (owner confirms the
  Docker path served macOS/Linux only, and users are on Windows);
  README updated with new native instructions.

## Migration Plan

Single PR on `dev`. Rollback = revert the PR (Docker files return with
it). No data or config migration: `settings.py` is untouched.

## Open Questions

- None blocking. Enum-scoping fixes are discovered mechanically during
  migration (decision 4).
