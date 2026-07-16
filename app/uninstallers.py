from __future__ import annotations

import os
import re
import shlex
import subprocess
from dataclasses import dataclass

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from app.models.domain import ProgramEntry


@dataclass(frozen=True, slots=True)
class UninstallPlan:
    program: ProgramEntry
    arguments: tuple[str, ...]
    supported: bool
    reason: str


class UninstallService:
    def plan(self, program: ProgramEntry) -> UninstallPlan:
        if program.protected:
            return UninstallPlan(program, (), False, program.protection_reason)
        if program.provider_id == "appx":
            if not re.fullmatch(r"[A-Za-z0-9._-]+", program.package_id):
                return UninstallPlan(program, (), False, "The Microsoft Store package identity is invalid")
            return UninstallPlan(program, ("powershell.exe", "-NoProfile", "-NonInteractive", "-Command", f"Remove-AppxPackage -Package '{program.package_id}'"), True, "Microsoft Store package removal")
        if not program.uninstall_command.strip():
            return UninstallPlan(program, (), False, "No registered uninstall method")
        try:
            arguments = tuple(shlex.split(program.uninstall_command, posix=False))
        except ValueError as error:
            return UninstallPlan(program, (), False, str(error))
        if not arguments or any(";" in argument or "|" in argument or "&" in argument for argument in arguments):
            return UninstallPlan(program, (), False, "The registered command contains unsafe shell syntax")
        executable = os.path.basename(arguments[0]).casefold()
        if executable not in {"msiexec.exe", "msiexec", "uninstall.exe", "unins000.exe", "setup.exe"} and not arguments[0].lower().endswith(".exe"):
            return UninstallPlan(program, (), False, "The registered executable is not a Windows executable")
        return UninstallPlan(program, arguments, True, "Registered uninstall command")

    def execute(self, plan: UninstallPlan) -> int:
        if not plan.supported:
            raise ValueError(plan.reason)
        completed = subprocess.run(list(plan.arguments), shell=False, check=False, timeout=900)
        return completed.returncode


class UninstallSignals(QObject):
    finished = Signal(list)


class UninstallTask(QRunnable):
    def __init__(self, plans: list[UninstallPlan]) -> None:
        super().__init__()
        self.plans = plans
        self.signals = UninstallSignals()

    @Slot()
    def run(self) -> None:
        service = UninstallService()
        results: list[tuple[UninstallPlan, int | str]] = []
        for plan in self.plans:
            try:
                results.append((plan, service.execute(plan)))
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                results.append((plan, str(error)))
        self.signals.finished.emit(results)

