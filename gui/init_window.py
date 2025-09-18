from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QInputDialog, QLineEdit
)
from PyQt6.QtCore import Qt
import sys


class InitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stage Tracker")
        self.setFixedSize(800, 600)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)

        # --- TOP section (labels) ---
        top_layout = QVBoxLayout()
        self.title_label = QLabel("Welcome Horizontal Stage Tracker")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.version_label = QLabel("Version 4.0")
        self.version_label.setStyleSheet("font-size: 14px; color: gray;")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        top_layout.addWidget(self.title_label)
        top_layout.addWidget(self.version_label)

        # --- MIDDLE section (buttons) ---
        middle_layout = QVBoxLayout()

        button_style = "font-size: 16px; padding: 10px 20px;"
        button_width = 200  # pixels

        self.user_button = QPushButton("USER")
        self.user_button.setFixedWidth(button_width)
        self.user_button.setStyleSheet(button_style)
        self.user_button.clicked.connect(self.user_login)

        self.admin_button = QPushButton("ADMIN")
        self.admin_button.setFixedWidth(button_width)
        self.admin_button.setStyleSheet(button_style)
        self.admin_button.clicked.connect(self.admin_login)

        middle_layout.addWidget(self.user_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        middle_layout.addSpacing(20)  # space between buttons
        middle_layout.addWidget(self.admin_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # --- FOOTER section (copyright) ---
        footer_layout = QHBoxLayout()
        self.copyright_label = QLabel("Copyright © 2025 by Dev. Luis Navarro")
        self.copyright_label.setStyleSheet("font-size: 14px; color: gray;")
        footer_layout.addStretch()  # push to the right
        footer_layout.addWidget(self.copyright_label)

        # --- Assemble main layout ---
        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)       # push labels up
        main_layout.addLayout(middle_layout)
        main_layout.addStretch(2)       # keep buttons centered
        main_layout.addLayout(footer_layout)  # add footer at bottom

    def user_login(self):
        user_name, ok = QInputDialog.getText(self, "USER Login", "Enter your name:")
        if ok and user_name:
            print(f"USER logged in: {user_name}")

    def admin_login(self):
        password, ok = QInputDialog.getText(
            self,
            "ADMIN Login",
            "Enter password:",
            QLineEdit.EchoMode.Password)
        if ok:
            print(f"ADMIN login attempted with password: {password}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InitWindow()
    window.show()
    sys.exit(app.exec())
