# main.py
# Telegram-style GUI for Facebook Automation
# Built using PyQt6

import sys
import threading
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QStackedWidget, QCheckBox,
    QSpinBox, QPlainTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt

# Custom handler to show logs in GUI console
class LogHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

# Main GUI class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Facebook Bulk Creator")
        self.setGeometry(100, 100, 1100, 580)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Main layout
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.addItems([
            "Home", "Tracker", "Retry Config",
            "Email Stats", "Logs", "Themes", "About Me"
        ])
        self.sidebar.setFixedWidth(180)
        self.sidebar.currentRowChanged.connect(self.switch_panel)
        main_layout.addWidget(self.sidebar)

        # Main content panels
        self.panels = QStackedWidget()
        main_layout.addWidget(self.panels)

        # Add pages
        self.panels.addWidget(self.home_panel())
        self.panels.addWidget(self.tracker_panel())
        self.panels.addWidget(self.retry_panel())
        self.panels.addWidget(self.email_panel())
        self.panels.addWidget(self.logs_panel())
        self.panels.addWidget(self.themes_panel())
        self.panels.addWidget(self.about_panel())

        # Init logging console
        self.logger_box = QPlainTextEdit()
        self.logger_box.setReadOnly(True)
        log_handler = LogHandler(self.logger_box)
        log_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%H:%M:%S"))
        logging.getLogger().addHandler(log_handler)
        logging.getLogger().setLevel(logging.INFO)

    def switch_panel(self, index):
        self.panels.setCurrentIndex(index)

    def home_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🧠 Facebook Automation"))
        start_btn = QPushButton("▶️ Start Account Creation")
        start_btn.clicked.connect(self.start_automation)
        layout.addWidget(start_btn)
        panel.setLayout(layout)
        return panel

    def tracker_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("✅ Created accounts will be shown here."))
        layout.addWidget(QLabel("❌ Failed attempts and retry stats."))
        panel.setLayout(layout)
        return panel

    def retry_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("🔁 Max Retry Attempts:"))
        self.attempts_spin = QSpinBox()
        self.attempts_spin.setValue(3)
        layout.addWidget(self.attempts_spin)

        layout.addWidget(QLabel("⏱️ Delay Between Retries (seconds):"))
        self.delay_spin = QSpinBox()
        self.delay_spin.setValue(30)
        layout.addWidget(self.delay_spin)

        layout.addWidget(QLabel("🗂️ Max Parallel Tabs:"))
        self.tabs_slider = QSpinBox()
        self.tabs_slider.setValue(3)
        self.tabs_slider.setRange(1, 5)
        layout.addWidget(self.tabs_slider)

        self.fallback_checkbox = QCheckBox("🧪 Enable Fallback Retry")
        self.fallback_checkbox.setChecked(True)
        layout.addWidget(self.fallback_checkbox)

        self.headless_checkbox = QCheckBox("🎭 Run in Headless Mode")
        self.headless_checkbox.setChecked(True)
        layout.addWidget(self.headless_checkbox)

        panel.setLayout(layout)
        return panel

    def email_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📧 Gmail Usage Stats will be shown here."))
        refresh_btn = QPushButton("🔄 Refresh Stats")
        refresh_btn.clicked.connect(self.show_email_stats)
        layout.addWidget(refresh_btn)
        panel.setLayout(layout)
        return panel

    def logs_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📜 Live Logs Console"))
        layout.addWidget(self.logger_box)

        export_btn = QPushButton("💾 Export Logs to JSON")
        export_btn.clicked.connect(self.export_logs)
        layout.addWidget(export_btn)
        panel.setLayout(layout)
        return panel

    def themes_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        self.theme_toggle = QCheckBox("🌓 Toggle Dark Mode")
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_toggle)
        panel.setLayout(layout)
        return panel

    def about_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        dev_label = QLabel('Developed by <a href="https://t.me/uKnowMehedi">@uKnowMehedi</a>')
        dev_label.setOpenExternalLinks(True)
        layout.addWidget(dev_label)
        layout.addWidget(QLabel("🐰 Automation for Smart Fighters"))
        panel.setLayout(layout)
        return panel

    def toggle_theme(self, state):
        if state == Qt.CheckState.Checked.value:
            self.setStyleSheet("background-color: #1e1e1e; color: white;")
        else:
            self.setStyleSheet("background-color: #f0f0f0; color: black;")

    def start_automation(self):
        # Collect GUI config
        from controllers.automation import start_account_creation
        headless = self.headless_checkbox.isChecked()
        max_tabs = self.tabs_slider.value()
        max_attempts = self.attempts_spin.value()
        delay = self.delay_spin.value()
        fallback = self.fallback_checkbox.isChecked()

        # Launch automation in background
        threading.Thread(
            target=start_account_creation,
            kwargs={
                "headless": headless,
                "max_tabs": max_tabs,
                "max_attempts": max_attempts,
                "delay": delay,
                "fallback_enabled": fallback
            },
            daemon=True
        ).start()

    def export_logs(self):
        from controllers.export_logs import export_results
        # Dummy data — Replace with live session logs
        success = ["user123"]
        failed = ["Tab 1"]
        emails = ["demo@gmail.com"]
        paths = export_results(success, failed, emails)

        msg = QMessageBox()
        msg.setWindowTitle("Export Done")
        msg.setText(f"📦 Logs exported to:\n{paths[0]}\n{paths[1]}")
        msg.exec()

    def show_email_stats(self):
        from utils.real_email_loader import get_email_usage_stats
        get_email_usage_stats()

# Launch the App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())