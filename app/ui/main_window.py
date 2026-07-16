from __future__ import annotations

import logging

from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.accessibility.announcer import Announcer
from app.cleanup.safety import ProtectedPathPolicy
from app.config.settings import AppSettings
from app.localization.translator import Translator
from app.models.domain import FileEntry, ProgramEntry, ScanError, ScanProgress
from app.providers.programs import installed_programs
from app.scanning.paths import system_scan_roots
from app.scanning.scanner import ScanTask


class MainWindow(QMainWindow):
    def __init__(self, settings: AppSettings, translator: Translator) -> None:
        super().__init__()
        self.settings = settings
        self.t = translator
        self.announcer = Announcer()
        self.pool = QThreadPool.globalInstance()
        self.task: ScanTask | None = None
        self.entries: list[FileEntry] = []
        self.errors: list[ScanError] = []
        self.policy = ProtectedPathPolicy()
        self.log = logging.getLogger("deleter")
        self._build_ui()
        self._retranslate()
        self.start_scan()

    def _build_ui(self) -> None:
        self.threshold = QComboBox()
        for label, value in (("500 MB", 500), ("1 GB", 1024), ("2 GB", 2048), ("5 GB", 5120), ("10 GB", 10240), ("20 GB", 20480), ("50 GB", 51200), ("100 GB", 102400)):
            self.threshold.addItem(label, value * 1024 * 1024)
        self.threshold.addItem(self.t.text("custom_size"), None)
        self.threshold.currentIndexChanged.connect(self.choose_custom_size)
        self.scan_button = QPushButton()
        self.scan_button.clicked.connect(self.start_scan)
        self.pause_button = QPushButton()
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.stop_button = QPushButton()
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_scan)
        self.simulation = QCheckBox()
        self.simulation.setChecked(self.settings.simulation_mode)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)
        self.status = QLabel()
        self.status.setAccessibleName("Scan status")
        self.files_table = QTableWidget(0, 12)
        self.files_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.files_table.setSortingEnabled(True)
        self.files_table.setAccessibleName("Files")
        self.programs_table = QTableWidget(0, 9)
        self.programs_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.programs_table.setSortingEnabled(True)
        self.programs_table.setAccessibleName("Programs")
        self.files_table.itemChanged.connect(lambda _: self.update_selection_status())
        self.programs_table.itemChanged.connect(lambda _: self.update_selection_status())
        self.tabs = QTabWidget()
        self.tabs.addTab(self.programs_table, "Programs")
        self.tabs.addTab(self.files_table, "Files")
        self.preview_button = QPushButton()
        self.preview_button.clicked.connect(self.preview_cleanup)
        self.select_all_button = QPushButton()
        self.select_all_button.clicked.connect(self.select_all_visible)
        self.clear_button = QPushButton()
        self.clear_button.clicked.connect(self.clear_selection)
        self.review_button = QPushButton()
        self.review_button.clicked.connect(self.review_selection)
        self.program_action = QPushButton()
        self.program_action.clicked.connect(self.review_program_uninstall)
        self.details_button = QPushButton()
        self.details_button.clicked.connect(self.show_details)
        self.selection_status = QLabel()
        self.selection_status.setAccessibleName("Selection status")
        self.log_list = QListWidget()
        self.log_list.setAccessibleName("Operation log")
        controls = QGridLayout()
        controls.addWidget(QLabel(""), 0, 0)
        controls.addWidget(self.threshold, 0, 1)
        controls.addWidget(self.scan_button, 0, 2)
        controls.addWidget(self.pause_button, 0, 3)
        controls.addWidget(self.stop_button, 0, 4)
        controls.addWidget(self.simulation, 1, 0, 1, 2)
        controls.addWidget(self.progress, 1, 2, 1, 3)
        actions = QHBoxLayout()
        actions.addWidget(self.select_all_button)
        actions.addWidget(self.clear_button)
        actions.addWidget(self.review_button)
        actions.addWidget(self.preview_button)
        actions.addWidget(self.program_action)
        actions.addWidget(self.details_button)
        actions.addStretch()
        body = QVBoxLayout()
        body.addLayout(controls)
        body.addWidget(self.tabs, 1)
        body.addLayout(actions)
        body.addWidget(self.selection_status)
        body.addWidget(self.status)
        body.addWidget(self.log_list, 0)
        container = QWidget()
        container.setLayout(body)
        self.setCentralWidget(container)
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.choose_language)
        self.menuBar().addAction(settings_action)

    def _retranslate(self) -> None:
        self.setWindowTitle(self.t.text("title"))
        self.scan_button.setText(self.t.text("scan"))
        self.pause_button.setText(self.t.text("pause"))
        self.stop_button.setText(self.t.text("stop"))
        self.simulation.setText(self.t.text("simulate"))
        self.preview_button.setText(self.t.text("delete"))
        self.tabs.setTabText(0, self.t.text("programs"))
        self.tabs.setTabText(1, self.t.text("files"))
        self.select_all_button.setText(self.t.text("select_all"))
        self.clear_button.setText(self.t.text("clear"))
        self.review_button.setText(self.t.text("review_selection"))
        self.program_action.setText(self.t.text("deinstall"))
        self.details_button.setText(self.t.text("details"))
        self.files_table.setHorizontalHeaderLabels([self.t.text("name"), self.t.text("path"), "Type", self.t.text("size"), self.t.text("used_space"), self.t.text("modified"), self.t.text("source"), self.t.text("risk"), self.t.text("access"), self.t.text("protection"), self.t.text("reason"), "Selected"])
        self.programs_table.setHorizontalHeaderLabels([self.t.text("name"), self.t.text("publisher"), self.t.text("version"), self.t.text("source"), self.t.text("install_date"), self.t.text("used_space"), self.t.text("install_location"), self.t.text("uninstall_method"), self.t.text("protection")])
        self.status.setText(self.t.text("status_ready"))

    def start_scan(self) -> None:
        if self.task:
            return
        self.entries.clear()
        self.errors.clear()
        self.files_table.setRowCount(0)
        self.programs_table.setRowCount(0)
        self.add_programs(installed_programs())
        self.task = ScanTask(system_scan_roots(), int(self.threshold.currentData()))
        self.task.signals.batch.connect(self.add_batch)
        self.task.signals.progress.connect(self.update_progress)
        self.task.signals.error.connect(self.record_error)
        self.task.signals.finished.connect(self.scan_finished)
        self.scan_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.progress.setVisible(True)
        self.status.setText(self.t.text("status_scanning"))
        self.announcer.say(self.t.text("status_scanning"))
        self.pool.start(self.task)

    def add_programs(self, programs: list[ProgramEntry]) -> None:
        self.programs_table.setSortingEnabled(False)
        for program in programs:
            row = self.programs_table.rowCount()
            self.programs_table.insertRow(row)
            values = [program.name, program.publisher, program.version, program.source, program.install_date, self.format_size(program.used_space_bytes) if program.used_space_bytes else "", program.install_location, program.uninstall_command, self.t.text("protected") if program.protected else self.t.text("review")]
            for column, value in enumerate(values):
                self.programs_table.setItem(row, column, QTableWidgetItem(value))
            item = self.programs_table.item(row, 0)
            if item is None:
                continue
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            if program.protected:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                item.setToolTip(program.protection_reason)
        self.programs_table.setSortingEnabled(True)

    def add_batch(self, batch: list[FileEntry]) -> None:
        self.entries.extend(batch)
        self.files_table.setSortingEnabled(False)
        for entry in batch:
            row = self.files_table.rowCount()
            self.files_table.insertRow(row)
            decision = self.policy.assess(entry.path)
            protection = self.t.text("protected") if decision.protected else self.t.text("review")
            values = [entry.name, str(entry.path), entry.entry_type.value, self.format_size(entry.size_bytes), self.format_size(entry.used_space_bytes or entry.size_bytes), entry.modified_at.strftime("%Y-%m-%d %H:%M"), entry.source, entry.risk, entry.access_status, protection + " — " + decision.reason if decision.protected else protection, entry.cleanup_reason, ""]
            for column, value in enumerate(values):
                self.files_table.setItem(row, column, QTableWidgetItem(value))
            item = self.files_table.item(row, 0)
            if item is None:
                continue
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            if decision.protected:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                item.setToolTip(decision.reason)
        self.files_table.setSortingEnabled(True)

    def update_progress(self, progress: ScanProgress) -> None:
        self.status.setText(self.t.text("live_status", scanned=progress.scanned_items, matched=progress.matched_items, skipped=progress.skipped_items, protected=progress.protected_items, errors=progress.errors, path=progress.current_path))

    def record_error(self, error: ScanError) -> None:
        self.errors.append(error)
        if error.error_code == 5:
            self.log_list.addItem(self.t.text("access_denied", path=error.path))
        else:
            self.log_list.addItem(f"{error.path}: {error.message}")

    def scan_finished(self) -> None:
        stopped = bool(self.task and self.task.stop_requested)
        self.task = None
        self.scan_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.progress.setVisible(False)
        message = self.t.text("status_stopped") if stopped else self.t.text("status_done", count=len(self.entries))
        if self.errors:
            message += " " + self.t.text("errors", count=len(self.errors))
        self.status.setText(message)
        self.announcer.say(message)
        self.update_selection_status()

    def toggle_pause(self) -> None:
        if not self.task:
            return
        if self.task.pause_requested:
            self.task.resume()
            self.pause_button.setText(self.t.text("pause"))
            self.announcer.say(self.t.text("resume"))
        else:
            self.task.pause()
            self.pause_button.setText(self.t.text("resume"))
            self.announcer.say(self.t.text("pause"))

    def stop_scan(self) -> None:
        if self.task:
            self.task.stop()

    def preview_cleanup(self) -> None:
        selected = self.selected_file_entries()
        locked = [entry for entry in selected if self.policy.is_protected(entry.path)]
        size = self.format_size(sum(entry.size_bytes for entry in selected))
        message = f"{self.t.text('selected', count=len(selected), size=size)}\n{self.t.text('locked_count', count=len(locked))}\n{self.t.text('preview')}"
        QMessageBox.information(self, self.t.text("delete"), message)
        self.announcer.say(message.replace("\n", ". "))

    def selected_file_entries(self) -> list[FileEntry]:
        selected_paths: set[str] = set()
        for row in range(self.files_table.rowCount()):
            check_item = self.files_table.item(row, 0)
            path_item = self.files_table.item(row, 1)
            if check_item is not None and path_item is not None and check_item.checkState() == Qt.CheckState.Checked:
                selected_paths.add(path_item.text())
        return [entry for entry in self.entries if str(entry.path) in selected_paths]

    def select_all_visible(self) -> None:
        table = self.programs_table if self.tabs.currentIndex() == 0 else self.files_table
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item is not None and item.flags() & Qt.ItemFlag.ItemIsEnabled:
                item.setCheckState(Qt.CheckState.Checked)
        self.update_selection_status()

    def clear_selection(self) -> None:
        for table in (self.programs_table, self.files_table):
            for row in range(table.rowCount()):
                item = table.item(row, 0)
                if item:
                    item.setCheckState(Qt.CheckState.Unchecked)
        self.update_selection_status()

    def review_selection(self) -> None:
        selected = self.selected_file_entries()
        locked = sum(self.policy.is_protected(entry.path) for entry in selected)
        QMessageBox.information(self, self.t.text("review_selection"), self.t.text("selected", count=len(selected), size=self.format_size(sum(entry.size_bytes for entry in selected))) + "\n" + self.t.text("locked_count", count=locked))

    def review_program_uninstall(self) -> None:
        selected: list[str] = []
        for row in range(self.programs_table.rowCount()):
            item = self.programs_table.item(row, 0)
            if item is not None and item.checkState() == Qt.CheckState.Checked:
                selected.append(item.text())
        QMessageBox.information(self, self.t.text("deinstall"), f"{len(selected)} programs selected.\n{self.t.text('preview')}")

    def show_details(self) -> None:
        selected = self.selected_file_entries()
        if selected:
            entry = selected[0]
            QMessageBox.information(self, self.t.text("details"), f"{entry.name}\n{entry.path}\n{entry.cleanup_reason}\n{entry.protection_reason}")

    def update_selection_status(self) -> None:
        selected = self.selected_file_entries()
        locked = sum(self.policy.is_protected(entry.path) for entry in selected)
        inaccessible = sum(entry.access_status != "accessible" for entry in selected)
        risk = sum(entry.risk.casefold() in {"high", "critical"} for entry in selected)
        self.selection_status.setText(self.t.text("selection_status", count=len(selected), size=self.format_size(sum(entry.size_bytes for entry in selected)), locked=locked, inaccessible=inaccessible, risk=risk))

    def choose_language(self) -> None:
        labels = ["English", "Deutsch", "Türkçe"]
        language, ok = QInputDialog.getItem(self, "Settings", "Language", labels, ["en", "de", "tr"].index(self.t.language), False)
        if ok:
            self.settings.language = dict(zip(labels, ("en", "de", "tr")))[language]
            self.settings.save()
            self._retranslate()

    def choose_custom_size(self, index: int) -> None:
        if self.threshold.itemData(index) is not None:
            return
        value, ok = QInputDialog.getDouble(self, self.t.text("threshold"), "MB", 500, 500, 1024000, 0)
        if ok:
            self.threshold.setItemText(index, f"{value:g} MB")
            self.threshold.setItemData(index, int(value * 1024 * 1024))
        else:
            self.threshold.setCurrentIndex(0)

    @staticmethod
    def format_size(size: int) -> str:
        units = ("B", "KB", "MB", "GB", "TB")
        value = float(size)
        for unit in units:
            if value < 1024 or unit == units[-1]:
                return f"{value:.1f} {unit}"
            value /= 1024
        return "0.0 B"

