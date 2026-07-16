from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path


class EntryType(str, Enum):
    FILE = "file"


@dataclass(frozen=True, slots=True)
class FileEntry:
    name: str
    path: Path
    size_bytes: int
    modified_at: datetime
    entry_type: EntryType = EntryType.FILE
    access_status: str = "accessible"
    risk: str = "review"
    protected: bool = False
    protection_reason: str = ""
    used_space_bytes: int = 0
    source: str = "System scan"
    cleanup_reason: str = "Size threshold requires review"
    modified_ns: int = 0


@dataclass(frozen=True, slots=True)
class ScanProgress:
    scanned_items: int
    matched_items: int
    current_path: Path
    skipped_items: int = 0
    protected_items: int = 0
    errors: int = 0


@dataclass(frozen=True, slots=True)
class ProgramEntry:
    name: str
    version: str
    publisher: str
    install_location: str
    uninstall_command: str
    source: str
    install_date: str = ""
    used_space_bytes: int = 0
    protected: bool = False
    protection_reason: str = ""
    provider_id: str = "registry"
    package_id: str = ""


@dataclass(frozen=True, slots=True)
class ScanError:
    path: Path
    message: str
    error_code: int | None = None

