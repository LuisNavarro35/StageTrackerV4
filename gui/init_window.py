from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog
import sys

class InitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stage Tracker")
        self.setFixedSize(400, 300)

        # USER button
        self.user_button = QPushButton("USER", self)
        self.user_button.setGeometry(150, 100, 100, 40)
        self.user_button.clicked.connect(self.user_login)

        # ADMIN button
        self.admin_button = QPushButton("ADMIN", self)
        self.admin_button.setGeometry(150, 160, 100, 40)
        self.admin_button.clicked.connect(self.admin_login)

    def user_login(self):
        user_name, ok = QInputDialog.getText(self, "USER Login", "Enter your name:")
        if ok and user_name:
            print(f"USER logged in: {user_name}")
            # Here we will move to Job Selection later

    def admin_login(self):
        password, ok = QInputDialog.getText(self, "ADMIN Login", "Enter password:")
        if ok:
            # For now, just print for testing
            print(f"ADMIN login attempted with password: {password}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InitWindow()
    window.show()
    sys.exit(app.exec())
