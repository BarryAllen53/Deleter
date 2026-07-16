# Changelog

## [0.2.2] - 2026-07-16

### Fixed

- Added an explicit pytest configuration so the GitHub Windows runner does not mis-detect the TOML project configuration.

## [0.2.0] - 2026-07-16

### Added

- Windows storage scanning with incremental results, pause, resume, and cancellation.
- Programs and Files navigation with multi-selection and protected-item states.
- English, German, and Turkish user-facing text.
- Accessible Output 2 announcements and keyboard-oriented Qt controls.
- Verified cleanup rules, final identity preflight, Recycle Bin execution, and simulation mode.
- Windows-aware protected path and access-denied handling.
- JSON and CSV export.
- Controlled planning and isolated execution for registered Windows and Microsoft Store/AppX uninstall commands.

### Known limitations

- Permanent deletion is intentionally unavailable; cleanup always targets the Recycle Bin.
- Authenticode signing requires the encrypted certificate secrets documented in the release workflow.
- Windows ACL-denied, in-use, and security-managed paths remain visible as inaccessible or protected.

