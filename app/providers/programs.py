from __future__ import annotations

import json
import subprocess
import sys
import winreg

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from app.models.domain import ProgramEntry

UNINSTALL_ROOTS = (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER)
UNINSTALL_PATHS = (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")


class ProgramDiscoverySignals(QObject):
    finished = Signal(list)


class ProgramDiscoveryTask(QRunnable):
    def __init__(self) -> None:
        super().__init__()
        self.signals = ProgramDiscoverySignals()

    @Slot()
    def run(self) -> None:
        self.signals.finished.emit(installed_programs())


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
    for entry in microsoft_store_programs():
        programs[(entry.name.casefold(), entry.version, entry.source)] = entry
    for entry in winget_programs():
        programs[(entry.name.casefold(), entry.version, entry.source)] = entry
    return sorted(programs.values(), key=lambda item: item.name.casefold())


def microsoft_store_programs() -> list[ProgramEntry]:
    if sys.platform != "win32":
        return []
    command = "Get-AppxPackage -AllUsers | Select-Object Name,Version,Publisher,InstallLocation,PackageFullName | ConvertTo-Json -Compress"
    try:
        completed = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90, check=False)
        if completed.returncode != 0 or not completed.stdout.strip():
            return []
        values = json.loads(completed.stdout)
        records = values if isinstance(values, list) else [values]
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        return []
    programs: list[ProgramEntry] = []
    for record in records:
        if not isinstance(record, dict) or not record.get("Name"):
            continue
        package_id = str(record.get("PackageFullName", ""))
        protected = not bool(package_id)
        programs.append(ProgramEntry(str(record.get("Name", "")), str(record.get("Version", "")), str(record.get("Publisher", "")), str(record.get("InstallLocation", "")), "", "Microsoft Store", provider_id="appx", package_id=package_id, protected=protected, protection_reason="Package identity could not be verified" if protected else ""))
    return programs


def winget_programs() -> list[ProgramEntry]:
    if sys.platform != "win32":
        return []
    try:
        completed = subprocess.run(
            ["winget.exe", "list", "--accept-source-agreements", "--disable-interactivity", "--output", "json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if completed.returncode != 0 or not completed.stdout.strip():
        return []
    try:
        values = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return []
    records = values.get("Sources", []) if isinstance(values, dict) else values
    if not isinstance(records, list):
        return []
    programs: list[ProgramEntry] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        name = str(record.get("Name") or record.get("name") or "").strip()
        if not name:
            continue
        package_id = str(record.get("Id") or record.get("id") or "").strip()
        version = str(record.get("Version") or record.get("version") or "").strip()
        if not package_id:
            continue
        programs.append(ProgramEntry(name, version, str(record.get("Publisher") or "").strip(), "", "", "WinGet", provider_id="winget", package_id=package_id))
    return programs

