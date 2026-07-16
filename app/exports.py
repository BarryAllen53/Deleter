from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from app.models.domain import FileEntry


class ExportService:
    @staticmethod
    def write_json(path: Path, entries: list[FileEntry]) -> None:
        path.write_text(json.dumps([{**asdict(entry), "path": str(entry.path), "modified_at": entry.modified_at.isoformat(), "entry_type": entry.entry_type.value} for entry in entries], ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def write_csv(path: Path, entries: list[FileEntry]) -> None:
        fields = ("name", "path", "size_bytes", "modified_at", "access_status", "risk", "protected", "protection_reason", "source", "cleanup_reason")
        with path.open("w", encoding="utf-8-sig", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=fields)
            writer.writeheader()
            for entry in entries:
                row = asdict(entry)
                row["path"] = str(entry.path)
                row["modified_at"] = entry.modified_at.isoformat()
                row["entry_type"] = entry.entry_type.value
                writer.writerow({field: row.get(field, "") for field in fields})

