from __future__ import annotations

from pathlib import Path

from app.cleanup.safety import ProtectedPathPolicy
from app.localization.translator import TEXTS, Translator
from app.models.domain import FileEntry


def test_size_is_stored_as_bytes() -> None:
    entry = FileEntry("large.bin", Path("large.bin"), 1024 * 1024 * 500, __import__("datetime").datetime.now())
    assert entry.size_bytes == 524288000


def test_protected_path_policy_rejects_windows_directory() -> None:
    policy = ProtectedPathPolicy()
    windows = Path(__import__("os").environ.get("WINDIR", r"C:\Windows"))
    assert policy.is_protected(windows / "System32" / "kernel32.dll")


def test_protected_path_policy_skips_denied_internet_cache() -> None:
    policy = ProtectedPathPolicy()
    path = Path(r"C:\Users\Example\AppData\Local\Microsoft\Windows\INetCache\Content.IE5")
    assert policy.should_skip_scan(path)


def test_translations_have_same_keys() -> None:
    assert set(TEXTS["en"]) == set(TEXTS["de"]) == set(TEXTS["tr"])


def test_translator_falls_back_to_english(tmp_path: Path) -> None:
    from app.config.settings import AppSettings

    settings = AppSettings(tmp_path / "settings.json")
    settings.language = "unsupported"
    assert Translator(settings).text("scan") == TEXTS["en"]["scan"]
