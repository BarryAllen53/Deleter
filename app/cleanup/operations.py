from __future__ import annotations

import ctypes
import os
from dataclasses import dataclass
from pathlib import Path

from app.cleanup.rules import CleanupRuleProvider
from app.cleanup.safety import ProtectedPathPolicy
from app.models.domain import FileEntry


@dataclass(frozen=True, slots=True)
class OperationResult:
    path: Path
    success: bool
    message: str
    skipped: bool = False


class CleanupService:
    def __init__(self, policy: ProtectedPathPolicy | None = None, rules: CleanupRuleProvider | None = None) -> None:
        self.policy = policy or ProtectedPathPolicy()
        self.rules = rules or CleanupRuleProvider()

    def preflight(self, entry: FileEntry) -> OperationResult:
        decision = self.policy.assess(entry.path)
        if decision.protected or entry.protected:
            return OperationResult(entry.path, False, decision.reason, True)
        if entry.access_status != "accessible":
            return OperationResult(entry.path, False, "The item is not accessible", True)
        try:
            current = entry.path.stat()
        except OSError as error:
            return OperationResult(entry.path, False, str(error), True)
        expected_mtime_ns = entry.modified_ns or int(entry.modified_at.timestamp() * 1_000_000_000)
        if current.st_size != entry.size_bytes or abs(int(current.st_mtime_ns) - expected_mtime_ns) > 1_000_000:
            return OperationResult(entry.path, False, "The item changed since the scan", True)
        if self.rules.rule_for(entry.path) is None:
            return OperationResult(entry.path, False, "No verified cleanup rule matches this path", True)
        return OperationResult(entry.path, True, "Ready")

    def move_to_recycle_bin(self, entry: FileEntry) -> OperationResult:
        check = self.preflight(entry)
        if not check.success:
            return check
        if os.name != "nt":
            return OperationResult(entry.path, False, "Recycle Bin operations require Windows")
        flags = 0x0040 | 0x0010 | 0x0400 | 0x0004
        class SHFILEOPSTRUCTW(ctypes.Structure):
            _fields_ = [("hwnd", ctypes.c_void_p), ("wFunc", ctypes.c_uint), ("pFrom", ctypes.c_wchar_p), ("pTo", ctypes.c_wchar_p), ("fFlags", ctypes.c_ushort), ("fAnyOperationsAborted", ctypes.c_int), ("hNameMappings", ctypes.c_void_p), ("lpszProgressTitle", ctypes.c_wchar_p)]
        operation = SHFILEOPSTRUCTW(None, 3, str(entry.path) + "\0", None, flags, 0, None, None)
        code = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(operation))
        return OperationResult(entry.path, code == 0 and not operation.fAnyOperationsAborted, "Moved to Recycle Bin" if code == 0 else f"Windows cleanup error {code}")

