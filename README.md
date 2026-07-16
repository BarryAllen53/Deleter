Exit code: 0
Wall time: 0.4 seconds
Output:
# Deleter

[Deutsche Dokumentation](README.de.md) · [Türkçe documentation](README.tr.md)

Deleter is a Windows desktop application for accessible storage analysis and safety-first cleanup review. It helps users find large files and installed programs while keeping Windows-critical paths technically protected.

## Status

Version 0.2.0 is the first functional public release. It includes protected system-wide scanning, verified Recycle Bin cleanup, supported uninstall execution, exports, accessibility, and simulation mode.

## Features

- Programs and Files tabs with incremental background scanning.
- Multi-selection with protected and inaccessible states.
- Size threshold filtering from 500 MB.
- Pause, resume, and cancellation.
- English, German, and Turkish UI text.
- Qt keyboard accessibility and Accessible Output 2 announcements.
- Windows ACL-aware error handling and UAC elevation support.
- Verified cleanup moves eligible files to the Windows Recycle Bin after confirmation; simulation mode remains available for review.
- Registry and Microsoft Store/AppX uninstall providers, with validated command planning and isolated execution.
- JSON and CSV exports for scan results.

## Safety model

Large files are never treated as automatically unnecessary. Windows, boot, driver, recovery, security, package, installed-program, reparse-point, and ACL-uncertain locations remain protected or inaccessible. The application does not take ownership, rewrite ACLs, disable security software, or bypass Windows protection mechanisms.

## Accessibility

Controls use native Qt roles, names, keyboard focus, check states, and status labels. Important scan and warning events are announced through Accessible Output 2 when available. Test reports should document NVDA, JAWS, and Narrator results for the target release.

## Languages and requirements

The supported UI languages are English, Deutsch, and Türkçe. Windows 10 or Windows 11 and Python 3.14.5 are required for source execution. Portable release artifacts do not require Python.

## Installation and start

For normal users, download the portable ZIP from the Releases page. From source, run `run.bat`; it creates `.venv`, installs controlled dependencies, and starts `python -m app`. Developers can install `requirements-dev.txt` and run the same module directly. Authenticode signing is enabled by the release workflow when the maintainer configures the encrypted `WINDOWS_PFX_BASE64` and `WINDOWS_PFX_PASSWORD` GitHub Secrets.

## Usage

The application starts a system scan automatically. Files are filtered by the selected minimum size and appear incrementally. Programs are read from supported Windows uninstall registration sources. Select entries with the keyboard or mouse, review the selection, and use the simulation preview. Protected checkboxes cannot be enabled.

## Permissions and privacy

The app can request administrator elevation for the system-wide scan, but an elevated token does not override explicit ACL denies, in-use files, or Windows security boundaries. Local file metadata, paths, and program information remain on the device and are not transmitted.

## Documentation and project structure

The application is organized under `app/accessibility`, `app/cleanup`, `app/config`, `app/localization`, `app/models`, `app/providers`, `app/scanning`, `app/ui`, and `app/windows`. Tests are under `tests`.

## Known limitations and roadmap

Permanent deletion is intentionally unavailable: cleanup is restricted to verified, confirmed moves to the Recycle Bin. Provider availability depends on Windows registration and installed Store packages. See [ROADMAP.md](ROADMAP.md) and [CHANGELOG.md](CHANGELOG.md).

## Reporting, contributions, and releases

Use the issue templates for bugs, accessibility, performance, translations, program detection, filesystem analysis, and build problems. Report security issues through GitHub Security Advisories as described in [SECURITY.md](SECURITY.md). See [CONTRIBUTING.md](CONTRIBUTING.md) for development, testing, formatting, review, and release expectations.

## License

Deleter is released under the [MIT License](LICENSE).

