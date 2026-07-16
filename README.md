# Deleter

[Deutsche Dokumentation](README.de.md) · [Türkçe documentation](README.tr.md)

Deleter is a Windows desktop application for accessible storage analysis and safety-first cleanup review. It helps users find large files and installed programs while keeping Windows-critical paths technically protected.

## Status

Version 0.1.0 is an early public build focused on safe scanning, protected-item handling, accessibility, and simulation. It is not a destructive cleaner: deletion and uninstall execution remain disabled until their provider and preflight safeguards are complete.

## Features

- Programs and Files tabs with incremental background scanning.
- Multi-selection with protected and inaccessible states.
- Size threshold filtering from 500 MB.
- Pause, resume, and cancellation.
- English, German, and Turkish UI text.
- Qt keyboard accessibility and Accessible Output 2 announcements.
- Windows ACL-aware error handling and UAC elevation support.
- Simulation previews before any future destructive operation.

## Safety model

Large files are never treated as automatically unnecessary. Windows, boot, driver, recovery, security, package, installed-program, reparse-point, and ACL-uncertain locations remain protected or inaccessible. The application does not take ownership, rewrite ACLs, disable security software, or bypass Windows protection mechanisms.

## Accessibility

Controls use native Qt roles, names, keyboard focus, check states, and status labels. Important scan and warning events are announced through Accessible Output 2 when available. Test reports should document NVDA, JAWS, and Narrator results for the target release.

## Languages and requirements

The supported UI languages are English, Deutsch, and Türkçe. Windows 10 or Windows 11 and Python 3.14.5 are required for source execution. A future portable release will not require Python.

## Installation and start

For normal users, download a release asset when one is available. From source, run `run.bat`; it creates `.venv`, installs controlled dependencies, and starts `python -m app`. Developers can install `requirements-dev.txt` and run the same module directly. Release builds are portable; they are Authenticode-signed only when the maintainer configures the encrypted `WINDOWS_PFX_BASE64` and `WINDOWS_PFX_PASSWORD` GitHub Secrets.

## Usage

The application starts a system scan automatically. Files are filtered by the selected minimum size and appear incrementally. Programs are read from supported Windows uninstall registration sources. Select entries with the keyboard or mouse, review the selection, and use the simulation preview. Protected checkboxes cannot be enabled.

## Permissions and privacy

The app can request administrator elevation for the system-wide scan, but an elevated token does not override explicit ACL denies, in-use files, or Windows security boundaries. Local file metadata, paths, and program information remain on the device and are not transmitted.

## Documentation and project structure

The application is organized under `app/accessibility`, `app/cleanup`, `app/config`, `app/localization`, `app/models`, `app/providers`, `app/scanning`, `app/ui`, and `app/windows`. Tests are under `tests`.

## Known limitations and roadmap

Destructive cleanup, verified cleanup rules, full uninstall providers, exports, and a portable signed build are not enabled in 0.1.0. See [ROADMAP.md](ROADMAP.md) and [CHANGELOG.md](CHANGELOG.md).

## Reporting, contributions, and releases

Use the issue templates for bugs, accessibility, performance, translations, program detection, filesystem analysis, and build problems. Report security issues through GitHub Security Advisories as described in [SECURITY.md](SECURITY.md). See [CONTRIBUTING.md](CONTRIBUTING.md) for development, testing, formatting, review, and release expectations.

## License

Deleter is released under the [MIT License](LICENSE).

