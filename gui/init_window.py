from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QInputDialog, QLineEdit, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
import sys
import config
from db.connection import get_connection
from werkzeug.security import check_password_hash
from gui.job_selection import JobSelectionWindow

class InitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stage Tracker")
        self.setFixedSize(1000, 600)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout setup
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 30, 40, 20)
        main_layout.setSpacing(8)

        # --- TOP ---
        top_layout = QVBoxLayout()
        self.title_label = QLabel("Welcome to Wireline Stage Tracker")
        self.title_label.setObjectName("title")
        self.title_label.setFont(QFont("Segoe UI", 24))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.version_label = QLabel("Version 4.0")
        self.version_label.setObjectName("version")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        top_layout.addWidget(self.title_label)
        top_layout.addWidget(self.version_label)

        # --- MIDDLE ---
        middle_layout = QVBoxLayout()
        middle_layout.setSpacing(18)

        self.user_button = QPushButton("USER")
        self.admin_button = QPushButton("ADMIN")

        self.user_button.clicked.connect(self.user_login)
        self.admin_button.clicked.connect(self.admin_login)

        middle_layout.addWidget(self.user_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        middle_layout.addWidget(self.admin_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # --- FOOTER ---
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)

        footer_layout = QHBoxLayout()

        # 👽 Emoji logo (left corner)
        logo_label = QLabel("👽")
        logo_label.setObjectName("logo_label")
        logo_label.setToolTip("Hola!")

        self.footer_label = QLabel("© 2025 Luis Navarro — All rights reserved")
        self.footer_label.setObjectName("footer")

        # Add both to layout
        footer_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignLeft)
        footer_layout.addStretch(1)
        footer_layout.addWidget(self.footer_label, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(middle_layout)
        main_layout.addStretch(2)
        main_layout.addWidget(divider)
        main_layout.addLayout(footer_layout)

    def user_login(self):
        user_name, ok = QInputDialog.getText(self, "USER Login", "Enter user name:")
        if ok and user_name:

            if self.validate_user(user_name):
                print(f"✅ USER logged in: {user_name}")
                # Open Job Selection window
                self.job_window = JobSelectionWindow(user_name=user_name, is_admin=False)
                self.job_window.show()
                self.close()  # close InitWindow
            else:
                QMessageBox.warning(self, "Invalid User", f"User '{user_name}' not found in system.")

    def admin_login(self):
        password, ok = QInputDialog.getText(
            self,
            "ADMIN Login",
            "Enter password:",
            QLineEdit.EchoMode.Password
        )
        if ok:
            if self.validate_admin(password):
                print("✅ ADMIN logged in successfully")
                # Here we will move to Job Management / Dashboard later
            else:
                QMessageBox.warning(self, "Invalid Password", "Incorrect admin password.")

    def validate_user(self, username):
        """
        Check if the username exists in Asset Manager DB.
        Returns True if valid, False otherwise.
        """
        import traceback

        try:
            print("DEBUG: About to connect to DB...")
            conn = get_connection(db_name=config.DB_NAME_ASSETMANAGER)  # Asset Manager DB
            if conn is None:
                print("DEBUG: get_connection returned None")
                return False

            with conn.cursor() as cursor:
                query = "SELECT username FROM user WHERE BINARY username = %s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()

            conn.close()
            print(f"DEBUG: Query result = {result}")
            return result is not None

        except Exception as e:
            print(f"❌ Exception in validate_user: {e}")
            traceback.print_exc()
            return False

    def validate_admin(self, password):
        """
        Check if the entered password matches the hashed admin password in the DB.
        Returns True if correct, False otherwise.
        """
        try:
            conn = get_connection(db_name="assetmanagerdb2")
            cursor = conn.cursor()

            # Parameterized query to get admin hashed password
            query = "SELECT password_hash FROM user WHERE username = %s LIMIT 1"
            cursor.execute(query, ("admin",))

            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result is None:
                return False

            stored_password_hash = result["password_hash"]
            # Use check_password_hash to compare plain password with hashed password
            return check_password_hash(stored_password_hash, password)

        except Exception as e:
            print(f"Error validating admin: {e}")
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ✅ Apply dark theme globally
    try:
        with open("../themes/dark.qss", "r") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print("Error loading theme:", e)

    window = InitWindow()
    window.show()
    sys.exit(app.exec())
