# Account Creator GUI Application
# Developed using PyQt6
# GUI controls Playwright-based Facebook automation with Gmail OTP

import logging

# Custom logging handler to show logs inside the GUI log box (QPlainTextEdit)
class LogHandler(logging.Handler):
    def __init__(self, output_widget):
        super().__init__()
        self.output_widget = output_widget

    def emit(self, record):
        msg = self.format(record)
        self.output_widget.appendPlainText(msg)

# Standard PyQt6 imports
import sys
from PyQt6.QtWidgets import (
    QPlainTextEdit, QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget,
    QStackedWidget, QCheckBox, QSpinBox, QComboBox
)
from PyQt6.QtCore import Qt

# Main GUI window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Account Creator")
        self.setGeometry(100, 100, 1158, 540)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Main horizontal layout that holds sidebar and main content
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Setup log redirection from console to GUI Logs panel
        self.logger_handler = LogHandler(self.log_output)
        self.logger_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S'))
        logging.getLogger().addHandler(self.logger_handler)
        logging.getLogger().setLevel(logging.INFO)

        # Sidebar for navigation
        self.sidebar = QListWidget()
        self.sidebar.addItems([
            "Home", "Tracker", "Retry Config",
            "Email Preview", "Logs", "Themes", "Developer"
        ])
        self.sidebar.setFixedWidth(200)
        self.sidebar.currentRowChanged.connect(self.display_panel)
        main_layout.addWidget(self.sidebar)

        # Main area: changes based on selected sidebar panel
        self.panels = QStackedWidget()
        main_layout.addWidget(self.panels)

        # Attach all panels (loaded as separate widget builders)
        self.panels.addWidget(self.home_panel())
        self.panels.addWidget(self.tracker_panel())
        self.panels.addWidget(self.retry_panel())
        self.panels.addWidget(self.email_panel())
        self.panels.addWidget(self.logs_panel())
        self.panels.addWidget(self.themes_panel())
        self.panels.addWidget(self.developer_panel())


# Home panel with the main Start button
    def home_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        label = QLabel("🚀 Start New Account Creation")
        start_button = QPushButton("Start Account Creation (Headless Tabs)")
        start_button.clicked.connect(self.start_account_creation)  # Triggers automation
        layout.addWidget(label)
        layout.addWidget(start_button)
        panel.setLayout(layout)
        return panel

    # Tracker panel: displays static tracker status messages
    def tracker_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("✅ Account Created Successfully"))
        layout.addWidget(QLabel("❌ OTP Verification Failed – Retrying..."))
        panel.setLayout(layout)
        return panel

    # Retry configuration panel
    def retry_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Max Attempts:"))
        self.attempts_spin = QSpinBox()
        self.attempts_spin.setValue(3)
        layout.addWidget(self.attempts_spin)

        layout.addWidget(QLabel("Delay (sec):"))
        self.delay_spin = QSpinBox()
        self.delay_spin.setValue(30)
        layout.addWidget(self.delay_spin)

        self.fallback_checkbox = QCheckBox("Enable Fallback")
        layout.addWidget(self.fallback_checkbox)
        panel.setLayout(layout)
        return panel

    # Email preview panel — shows current Gmail account being used
    def email_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📧 Current Email: demo@example.com"))
        layout.addWidget(QLabel("🟡 App Password: ✅ Enabled"))
        layout.addWidget(QLabel("🔄 Status: Not Used"))
        panel.setLayout(layout)
        return panel

    # Logs panel — real-time logs + Export button
    def logs_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📜 Real-time logs will appear here..."))

        # QPlainTextEdit for live logging
        self.log_output = QPlainTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # Export logs to JSON
        export_button = QPushButton("Export Logs to JSON")
        export_button.clicked.connect(self.export_logs)
        layout.addWidget(export_button)

        panel.setLayout(layout)
        return panel


# Themes panel — Toggle Light/Dark mode
    def themes_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        self.theme_toggle = QCheckBox("Toggle Dark Mode")
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_toggle)
        panel.setLayout(layout)
        return panel

    # Developer panel — Shows Telegram contact and quote
    def developer_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        link = QLabel('<a href="https://t.me/uKnowMehedi">🔗 Telegram: @uKnowMehedi</a>')
        link.setOpenExternalLinks(True)
        layout.addWidget(link)
        layout.addWidget(QLabel("🤓 Smart work will give you a better opportunity."))
        panel.setLayout(layout)
        return panel

    # Switch active panel when sidebar selection changes
    def display_panel(self, index):
        self.panels.setCurrentIndex(index)

    # Toggle Light/Dark Theme using checkbox
    def toggle_theme(self, state):
        if state == Qt.CheckState.Checked.value:
            self.setStyleSheet("background-color: #2e2e2e; color: white;")
        else:
            self.setStyleSheet("background-color: #f0f0f0; color: black;")

    # ▶️ START Automation button is clicked
    def start_account_creation(self):
        print("▶️ Starting account creation with headless tabs...")

        from controllers.automation import start_account_creation
        from PyQt6.QtWidgets import QMessageBox
        import threading
        from controllers.export_logs import export_results
        import logging

        # Setup logging format
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S')

        # Will launch automation in background (next step)

    # Export logs manually from Logs panel button
    def export_logs(self):
        from PyQt6.QtWidgets import QMessageBox
        # Dummy sample data — can be replaced with real runtime stats
        success = ["user123456"]
        failed = ["Tab 1"]
        emails = ["demo@gmail.com"]
        success_path, failed_path, email_path = export_results(success, failed, emails)

        msg = QMessageBox()
        msg.setWindowTitle("Export Complete")
        msg.setText(f"✅ Exported to:\n{success_path}\n{failed_path}")
        msg.exec()