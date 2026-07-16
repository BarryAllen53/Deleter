from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.config.settings import AppSettings
from app.localization.translator import Translator
from app.ui.main_window import MainWindow
from app.version import __version__
from app.windows.elevation import is_process_elevated, relaunch_elevated


def main() -> int:
    if not is_process_elevated():
        return relaunch_elevated()
    stdout_reconfigure = getattr(sys.stdout, "reconfigure", None)
    stderr_reconfigure = getattr(sys.stderr, "reconfigure", None)
    if callable(stdout_reconfigure):
        stdout_reconfigure(encoding="utf-8", errors="replace")
    if callable(stderr_reconfigure):
        stderr_reconfigure(encoding="utf-8", errors="replace")
    application = QApplication(sys.argv)
    application.setApplicationName("Deleter")
    application.setOrganizationName("Deleter")
    application.setApplicationVersion(__version__)
    settings = AppSettings(Path.home() / ".deleter" / "settings.json")
    log_path = Path.home() / ".deleter" / "deleter.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(handlers=[RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")], level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    translator = Translator(settings)
    window = MainWindow(settings, translator)
    window.show()
    return application.exec()

