# Security Policy

## Supported versions

| Version | Security fixes |
| --- | --- |
| `0.2.x` | Supported |
| Older releases | Not supported; update to the latest release before reporting a previously fixed issue |

The current release is listed on the [GitHub Releases page](https://github.com/BarryAllen53/Deleter/releases).

## Reporting a vulnerability

Do not report security vulnerabilities in public issues, pull requests, discussions, or comments. Use the repository's private [GitHub Security Advisory form](https://github.com/BarryAllen53/Deleter/security/advisories/new).

If the advisory form is unavailable, do not publish the vulnerability. Contact the repository maintainers through an authenticated GitHub channel and request a private reporting route.

Please include:

- Affected Deleter version and whether it was installed from source or a portable release
- Windows edition, version, and architecture
- Whether the process was elevated and which user context was active
- Clear reproduction steps or a minimal proof of concept
- Expected and observed behavior
- Security impact, affected boundaries, and any required privileges
- Relevant sanitized logs, stack traces, or screenshots
- Whether the issue is reproducible on the latest release

Remove usernames, private paths, personal files, access tokens, passwords, certificate material, registry exports, and other sensitive data before submitting evidence. Do not attach a malicious payload unless the maintainers specifically request it through the private advisory.

## Response and disclosure

The maintainers aim to acknowledge a report within seven calendar days. They will validate the report, keep the reporter informed when practical, coordinate a fix and disclosure date, and credit the reporter according to their preference.

Do not publicly disclose the vulnerability, exploit details, or identifying proof before coordinated disclosure. A report may be closed when it is not reproducible, is already fixed, is outside the application's security boundary, or does not create a security impact.

## Security boundaries

Deleter is a Windows desktop application. It does not upload file lists, paths, program lists, telemetry, or usage data. Administrator elevation does not bypass explicit ACL denies, in-use files, Windows security boundaries, or the application's protected-path policy.

The application must never permanently delete protected Windows-critical elements. Cleanup is restricted to verified, confirmed moves to the Windows Recycle Bin, and uninstall commands are validated before isolated execution.

## Out of scope

The following are not security vulnerabilities in Deleter unless they demonstrate an additional security impact:

- Access denied on files protected by Windows, ACLs, security software, or another process
- Unsupported uninstallers or missing optional Windows providers
- Findings that require an already-compromised administrator or SYSTEM account
- Vulnerabilities in Windows, Python, Qt, PySide6, Accessible Output 2, or other third-party components without a Deleter-specific impact
- Denial of service caused only by scanning a deliberately hostile or unbounded filesystem

Third-party vulnerabilities should be reported to their respective maintainers as well as privately to Deleter when the application meaningfully amplifies the impact.

## Safe-harbor request

Good-faith security research that follows this policy, avoids privacy violations and service disruption, and stops testing after confirming the issue is authorized. The maintainers will not pursue legal action for such research based solely on conduct within this policy's scope.

