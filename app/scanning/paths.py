from __future__ import annotations

import ctypes
import os
from pathlib import Path


def system_scan_roots() -> list[Path]:
    candidates: list[Path] = []
    if os.name == "nt":
        mask = ctypes.windll.kernel32.GetLogicalDrives()
        for index in range(26):
            if mask & (1 << index):
                candidates.append(Path(f"{chr(65 + index)}:\\"))
    candidates.extend((Path.home(), Path(os.environ.get("TEMP", str(Path.home() / "AppData" / "Local" / "Temp"))), Path(os.environ.get("WINDIR", r"C:\Windows")) / "Temp"))
    user_profile = Path(os.environ.get("USERPROFILE", str(Path.home())))
    candidates.extend(user_profile / name for name in ("AppData", "Desktop", "Documents", "Downloads"))
    local_app_data = Path(os.environ.get("LOCALAPPDATA", str(user_profile / "AppData" / "Local")))
    roaming = Path(os.environ.get("APPDATA", str(user_profile / "AppData" / "Roaming")))
    candidates.extend((local_app_data, local_app_data / "Packages", roaming))
    roots: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        try:
            normalized = str(candidate.resolve()).casefold()
        except OSError:
            continue
        if normalized not in seen and candidate.exists():
            seen.add(normalized)
            roots.append(candidate)
    return roots

