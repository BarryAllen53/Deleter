from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProtectionDecision:
    protected: bool
    reason: str


class ProtectedPathPolicy:
    def __init__(self) -> None:
        windows = Path(os.environ.get("WINDIR", r"C:\Windows"))
        self._protected = tuple(path.resolve() for path in (windows, windows / "Boot", windows / "WinSxS", windows / "System32", windows / "servicing", Path(os.environ.get("ProgramFiles", r"C:\Program Files")), Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"))))
        self._scan_blocked_segments = frozenset({"$recycle.bin", "system volume information", "config.msi", "windowsapps", "inetcache", "content.ie5", "webcache", "recovery", "system32\\config", "programdata\\microsoft\\windows defender"})

    def is_protected(self, path: Path) -> bool:
        return self.assess(path).protected

    def should_skip_scan(self, path: Path) -> bool:
        normalized = str(path).replace("/", "\\").casefold().rstrip("\\")
        parts = [part.casefold() for part in Path(normalized).parts]
        if any(part in self._scan_blocked_segments for part in parts):
            return True
        return "\\system32\\config" in normalized or "\\programdata\\microsoft\\windows defender" in normalized

    def assess(self, path: Path) -> ProtectionDecision:
        try:
            candidate = path.resolve()
            if any(candidate == protected or protected in candidate.parents for protected in self._protected):
                return ProtectionDecision(True, "Known critical Windows or installed-program path")
            if self.should_skip_scan(path):
                return ProtectionDecision(True, "Windows protects this cache, recovery, recycle-bin, or security directory")
            if path.is_symlink():
                return ProtectionDecision(True, "Symbolic links and reparse points are locked")
            if candidate.anchor and candidate == Path(candidate.anchor):
                return ProtectionDecision(True, "Drive roots are never deletable")
            return ProtectionDecision(False, "User selection requires explicit review")
        except OSError:
            return ProtectionDecision(True, "Path identity or security metadata could not be verified")

