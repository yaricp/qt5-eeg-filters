# Design: package-binaries-ci

## Context

Prerequisite `migrate-to-pyside6` delivers: PySide6-only code, single
pyproject.toml, pytest suite green on a 3-OS CI matrix, Docker launch
layer already deleted. This change adds the distribution layer for users
who have neither Python nor Docker (mainly Windows laptops, no shared
server), and strips the obsolete GHCR image publication from CI.

## Goals / Non-Goals

**Goals:**
- One-command CI path from git tag to GitHub Release with three
  smoke-tested binaries.
- Packaging failures (missing Qt plugins, hidden imports, data files)
  caught in CI, not by users.

**Non-Goals:**
- No code signing (SmartScreen/Gatekeeper warnings documented instead).
- No auto-update mechanism, no installers (MSI/DMG) — plain
  exe/app-zip/binary is enough for this audience.
- No pip package, no Docker distribution.

## Decisions

1. **PyInstaller over Briefcase/Nuitka/cx_Freeze.** Most mature, ships
   PySide6 + pyqtgraph hooks, huge community for troubleshooting.
   Briefcase targets store-style packaging (heavier); Nuitka compiles
   (slow builds, harder debugging) — no benefit for an internal science
   tool.

2. **Artifact formats:** Windows — one-file `.exe` (simplest download;
   slower start accepted); macOS — `--windowed` `.app` bundle zipped
   (one-file breaks Gatekeeper translocation more often); Linux —
   one-file binary. One committed `.spec` file with per-OS branches.

3. **`--smoke-test` flag in `main.py`:** when present, force
   `QT_QPA_PLATFORM=offscreen`, construct `MainWindow`, load the bundled
   sample recording, apply the first bandwidth filter, print PASS and
   `sys.exit(0)`; any exception → traceback and exit 1. A small sample
   from `data/` is bundled via the spec's `datas` so the frozen binary is
   self-sufficient. TDD: unit test asserts the flag path returns 0
   before packaging work starts.

4. **Release workflow (`release-actions.yml`), trigger `push: tags: v*`:**
   matrix over the three `-latest` runners: poetry install → pyinstaller
   → run the frozen artifact with `--smoke-test` → upload to release via
   `softprops/action-gh-release`. Version comes from the tag; job fails
   if any binary fails its smoke run.

5. **Docker publication removal:** delete build/publish jobs and GHCR
   login from `dev-actions.yml` and `main-actions.yml`; `dev-actions.yml`
   keeps lint+tests only. Old GHCR packages left as-is (history).

6. **Windows verification:** CI smoke-run covers unpack/imports/Qt
   plugins; the owner additionally checks the `.exe` interactively in a
   Windows VM before the first public release (documented as release
   checklist item in README).

## Risks / Trade-offs

- [One-file exe slow first start (unpack to temp)] → acceptable for this
  tool; can switch to one-dir zip later without spec redesign.
- [GitHub runner smoke-run lacks real GPU/display] → offscreen platform
  is exactly what the flag forces; interactive rendering verified once
  per release in the VM.
- [SmartScreen scares users] → README screenshot-level instructions
  ("More info → Run anyway"); revisit paid signing only if adoption
  grows.
- [PyInstaller misses a dynamic import (scipy/pyedflib)] → smoke test
  loads real data through the full import chain; add
  `--hidden-import` entries as CI reveals them.

## Migration Plan

Single PR on `dev` after `migrate-to-pyside6` merges. First release:
tag `v0.3.0` → verify three artifacts on the draft release → owner VM
check → publish. Rollback: delete tag/release; dev CI unaffected.

## Open Questions

- None blocking.
