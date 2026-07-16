from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class CleanupRule:
    rule_id: str
    name: str
    description: str
    source: str
    risk: str
    allowed_patterns: tuple[str, ...]
    excluded_patterns: tuple[str, ...]


class CleanupRuleProvider:
    def __init__(self) -> None:
        local_app_data = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
        temp = Path(os.environ.get("TEMP", str(local_app_data / "Temp")))
        self.rules = (
            CleanupRule("user-temp", "User temporary files", "Temporary files created for the current user.", "Windows TEMP", "review", (str(temp),), (),),
            CleanupRule("browser-cache", "Known browser caches", "Cache data from supported browser cache locations.", "Known cache path", "review", (str(local_app_data / "Microsoft" / "Edge" / "User Data"), str(local_app_data / "Google" / "Chrome" / "User Data")), ("\\Default\\Cookies", "\\Default\\Login Data")),
        )

    def rule_for(self, path: Path) -> CleanupRule | None:
        normalized = str(path.resolve()).casefold()
        for rule in self.rules:
            if any(normalized.startswith(pattern.casefold()) for pattern in rule.allowed_patterns) and not any(pattern.casefold() in normalized for pattern in rule.excluded_patterns):
                return rule
        return None

