# Account Creator GUI Application
# Developed using PyQt6
# GUI controls Playwright-based Facebook automation with Gmail OTP

import logging

# Custom log handler to redirect logs into the GUI log box
class LogHandler(logging.Handler):
    def __init__(self, output_widget):
        super().__init__()
        self.output_widget = output_widget

    def emit(self, record):
        msg = self.format(record)
        self.output_widget.appendPlainText(msg)

import sys
from PyQt6.QtWidgets import (
    QPlainTextEdit, QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QListWidget, QStackedWidget,
    QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Account Creator")
        self.setGeometry(100, 100, 1158, 540)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Setup GUI log redirection to the Logs panel
        self.logger_handler = LogHandler(self.log_output)
        self.logger_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S'))
        logging.getLogger().addHandler(self.logger_handler)
        logging.getLogger().setLevel(logging.INFO)

        # Sidebar navigation panel
        self.sidebar = QListWidget()
        self.sidebar.addItems(["Home", "Tracker", "Retry Config", "Email Preview", "Logs", "Themes", "Developer"])
        self.sidebar.setFixedWidth(200)
        self.sidebar.currentRowChanged.connect(self.display_panel)
        main_layout.addWidget(self.sidebar)

        # Central stacked panel switching between GUI sections
        self.panels = QStackedWidget()
        main_layout.addWidget(self.panels)

        # Each section panel
        self.panels.addWidget(self.home_panel())
        self.panels.addWidget(self.tracker_panel())
        self.panels.addWidget(self.retry_panel())
        self.panels.addWidget(self.email_panel())
        self.panels.addWidget(self.logs_panel())
        self.panels.addWidget(self.themes_panel())
        self.panels.addWidget(self.developer_panel())