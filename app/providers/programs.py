from __future__ import annotations

import sys
import winreg

from app.models.domain import ProgramEntry

UNINSTALL_ROOTS = (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER)
UNINSTALL_PATHS = (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")


def installed_programs() -> list[ProgramEntry]:
    if sys.platform != "win32":
        return []
    programs: dict[tuple[str, str, str], ProgramEntry] = {}
    for hive in UNINSTALL_ROOTS:
        for key_path in UNINSTALL_PATHS:
            try:
                with winreg.OpenKey(hive, key_path) as root:
                    for index in range(winreg.QueryInfoKey(root)[0]):
                        try:
                            with winreg.OpenKey(root, winreg.EnumKey(root, index)) as key:
                                name = str(winreg.QueryValueEx(key, "DisplayName")[0]).strip()
                                if not name:
                                    continue
                                values = {winreg.EnumValue(key, item)[0]: winreg.EnumValue(key, item)[1] for item in range(winreg.QueryInfoKey(key)[1])}
                                entry = ProgramEntry(name, str(values.get("DisplayVersion", "")), str(values.get("Publisher", "")), str(values.get("InstallLocation", "")), str(values.get("UninstallString", "")), "Windows Registry")
                                programs[(entry.name.casefold(), entry.version, entry.source)] = entry
                        except (OSError, ValueError):
                            continue
            except OSError:
                continue
    return sorted(programs.values(), key=lambda item: item.name.casefold())

