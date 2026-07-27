# Tasks: package-binaries-ci

## 1. Smoke-test flag (TDD)

- [ ] 1.1 Write `tests/test_smoke_flag.py`: running main with
      `--smoke-test` returns exit code 0 (subprocess, offscreen)
- [ ] 1.2 Implement `--smoke-test` in `src/main.py`: offscreen platform,
      construct MainWindow, load sample recording, apply first bandwidth
      filter, PASS + exit 0 / traceback + exit 1
- [ ] 1.3 Pick and commit the bundled sample (small file from `data/`),
      resolve its path so it works both from source and frozen bundle

## 2. PyInstaller packaging

- [ ] 2.1 Add `pyinstaller` dev dependency; write committed `.spec` file
      (per-OS branches: onefile exe / windowed .app / onefile linux;
      `datas` includes the sample)
- [ ] 2.2 Local build on macOS dev machine; run frozen app with and
      without `--smoke-test`; fix hidden imports until green

## 3. Release workflow

- [ ] 3.1 Create `release-actions.yml`: trigger on tag `v*`, 3-OS matrix:
      poetry install → pyinstaller → run artifact `--smoke-test` →
      upload via softprops/action-gh-release
- [ ] 3.2 Push a test tag (e.g. `v0.3.0-rc1`) on dev; verify three
      artifacts appear on the draft release and all smoke runs pass

## 4. Remove Docker publication

- [ ] 4.1 Strip Docker build/publish jobs and GHCR login from
      `dev-actions.yml` (keep lint+tests matrix) and `main-actions.yml`
- [ ] 4.2 Remove remaining Docker references from repo docs/scripts if
      any survived migrate-to-pyside6

## 5. Docs and final gate

- [ ] 5.1 README: per-OS download/run instructions, SmartScreen and
      Gatekeeper notes, release checklist (incl. owner's Windows VM
      check)
- [ ] 5.2 Owner verifies `.exe` interactively in Windows VM; publish
      first real release `v0.3.0`
- [ ] 5.3 Update `openspec/project.md` / `config.yaml` (distribution via
      Releases, no Docker)
