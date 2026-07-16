from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.cleanup.operations import CleanupService
from app.exports import ExportService
from app.models.domain import EntryType, FileEntry, ProgramEntry
from app.uninstallers import UninstallService


def test_cleanup_preflight_rejects_changed_file(tmp_path: Path) -> None:
    target = tmp_path / "file.tmp"
    target.write_bytes(b"before")
    stat = target.stat()
    entry = FileEntry(target.name, target, stat.st_size, datetime.fromtimestamp(stat.st_mtime), EntryType.FILE)
    target.write_bytes(b"after")
    result = CleanupService().preflight(entry)
    assert result.skipped
    assert "changed" in result.message


def test_exports_write_unicode_json_and_csv(tmp_path: Path) -> None:
    target = tmp_path / "çalışma.tmp"
    target.write_bytes(b"data")
    stat = target.stat()
    entry = FileEntry(target.name, target, stat.st_size, datetime.fromtimestamp(stat.st_mtime), EntryType.FILE)
    json_path = tmp_path / "results.json"
    csv_path = tmp_path / "results.csv"
    ExportService.write_json(json_path, [entry])
    ExportService.write_csv(csv_path, [entry])
    assert "çalışma.tmp" in json_path.read_text(encoding="utf-8")
    assert "çalışma.tmp" in csv_path.read_text(encoding="utf-8-sig")


def test_uninstall_planner_rejects_shell_syntax() -> None:
    program = ProgramEntry("Example", "1", "Publisher", "", "setup.exe & cmd.exe", "Registry")
    plan = UninstallService().plan(program)
    assert not plan.supported

