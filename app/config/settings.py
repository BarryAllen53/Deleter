from __future__ import annotations

import json
import locale
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class AppSettings:
    storage_path: Path
    language: str = ""
    minimum_size_bytes: int = 500 * 1024 * 1024
    simulation_mode: bool = True

    def __post_init__(self) -> None:
        self.load()

    def load(self) -> None:
        if self.storage_path.exists():
            try:
                values = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.language = str(values.get("language", ""))
                self.minimum_size_bytes = int(values.get("minimum_size_bytes", self.minimum_size_bytes))
                self.simulation_mode = bool(values.get("simulation_mode", True))
            except (OSError, ValueError, TypeError):
                return
        if self.language not in {"en", "de", "tr"}:
            system_language = (locale.getlocale()[0] or "en").lower()
            self.language = "de" if system_language.startswith("de") else "tr" if system_language.startswith("tr") else "en"

    def save(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.write_text(json.dumps({**asdict(self), "storage_path": str(self.storage_path)}, ensure_ascii=False, indent=2), encoding="utf-8")

