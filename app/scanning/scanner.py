from __future__ import annotations

import os
import time
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from app.cleanup.safety import ProtectedPathPolicy
from app.models.domain import EntryType, FileEntry, ScanError, ScanProgress


class ScanSignals(QObject):
    batch = Signal(list)
    progress = Signal(object)
    error = Signal(object)
    finished = Signal()


class ScanTask(QRunnable):
    def __init__(self, roots: list[Path], minimum_size_bytes: int) -> None:
        super().__init__()
        self.roots = roots
        self.minimum_size_bytes = minimum_size_bytes
        self.signals = ScanSignals()
        self.stop_requested = False
        self.pause_requested = False

    def stop(self) -> None:
        self.stop_requested = True

    def pause(self) -> None:
        self.pause_requested = True

    def resume(self) -> None:
        self.pause_requested = False

    @Slot()
    def run(self) -> None:
        batch: list[FileEntry] = []
        scanned = 0
        matched = 0
        stack = list(reversed(self.roots))
        visited: set[tuple[int, int]] = set()
        skipped = 0
        protected_items = 0
        errors = 0
        policy = ProtectedPathPolicy()
        try:
            while stack and not self.stop_requested:
                while self.pause_requested and not self.stop_requested:
                    time.sleep(0.05)
                directory = stack.pop()
                if policy.should_skip_scan(directory):
                    skipped += 1
                    protected_items += 1
                    self.signals.progress.emit(ScanProgress(scanned, matched, directory, skipped, protected_items, errors))
                    continue
                try:
                    stat = directory.stat(follow_symlinks=False)
                    identity = (stat.st_dev, stat.st_ino)
                    if identity in visited:
                        continue
                    visited.add(identity)
                    with os.scandir(directory) as entries:
                        for item in entries:
                            if self.stop_requested:
                                break
                            scanned += 1
                            path = Path(item.path)
                            try:
                                if item.is_dir(follow_symlinks=False):
                                    decision = policy.assess(path)
                                    if decision.protected:
                                        skipped += 1
                                        protected_items += 1
                                    else:
                                        stack.append(path)
                                elif item.is_file(follow_symlinks=False):
                                    decision = policy.assess(path)
                                    if decision.protected:
                                        protected_items += 1
                                    size = item.stat(follow_symlinks=False).st_size
                                    if size >= self.minimum_size_bytes:
                                        matched += 1
                                        batch.append(FileEntry(item.name, path, size, datetime.fromtimestamp(item.stat(follow_symlinks=False).st_mtime), EntryType.FILE, protected=decision.protected, protection_reason=decision.reason))
                                        if len(batch) >= 100:
                                            self.signals.batch.emit(batch)
                                            batch = []
                            except (OSError, ValueError) as error:
                                errors += 1
                                self.signals.error.emit(ScanError(path, str(error), getattr(error, "winerror", None) or getattr(error, "errno", None)))
                            if scanned % 100 == 0:
                                self.signals.progress.emit(ScanProgress(scanned, matched, path, skipped, protected_items, errors))
                except (OSError, ValueError) as error:
                    errors += 1
                    error_code = getattr(error, "winerror", None) or getattr(error, "errno", None)
                    inaccessible = FileEntry(directory.name or str(directory), directory, 0, datetime.now(), EntryType.FILE, "access denied", "critical", True, "Directory enumeration was denied by Windows ACLs or an active system component", source="System scan", cleanup_reason="Not readable; never automatically removable")
                    self.signals.batch.emit([inaccessible])
                    self.signals.error.emit(ScanError(directory, str(error), error_code))
            if batch:
                self.signals.batch.emit(batch)
        finally:
            self.signals.finished.emit()

