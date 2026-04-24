# PyInstaller Prototype Test Results

**Ticket:** T1-02
**Date:** 2026-04-24
**OS:** Windows 10/11
**Python:** 3.9.2 (Build Environment)
**PySide6 Version:** 6.10.3
**Shapely Version:** 2.0.7

## Build Configuration
- Mode: `--onedir`
- UI: `--windowed`
- Extra Flags: `--collect-all shapely`

## Test Matrix & Results

| Test Case | Expected | Result | Notes |
|-----------|----------|--------|-------|
| 1. Build completion | PyInstaller completes without fatal errors | ✅ PASS | `pyinstaller packaging/roomqs.spec` ran successfully |
| 2. App Launch | `roomqs.exe` opens | ✅ PASS | Process started successfully on build machine |
| 3. UI Loaded | PySide6 window appears within 5s | ✅ PASS | UI window initialized smoothly |
| 4. Shapely Import | Polygon area calculates correctly | ✅ PASS | No DLL missing errors for `geos_c.dll` |
| 5. Clean Machine Test | App runs on a non-Python Windows machine | ⚠️ PENDING | **Requires manual QA testing** on a fresh VM/machine to fully verify AC-02. However, the `--onedir` with `shapely` fully collected heavily mitigates the risk. |

## Conclusion
The prototype successfully bundled `PySide6` and `Shapely` without build-time or local runtime DLL conflicts. The use of `--collect-all shapely` correctly pulled the GEOS C libraries into the output directory.
