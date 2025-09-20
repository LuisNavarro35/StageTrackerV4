from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QInputDialog, QMessageBox, QListWidgetItem, QDialog, QComboBox
)

import config
from db.connection import get_connection

class JobSelectionWindow(QMainWindow):
    def __init__(self, user_name, is_admin=False):
        super().__init__()
        self.user_name = user_name
        self.is_admin = is_admin

        self.setWindowTitle("Job Selection")
        self.setFixedSize(800, 600)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)

        # Welcome label
        self.welcome_label = QLabel(f"Welcome, {self.user_name}!")
        layout.addWidget(self.welcome_label)

        # Jobs list
        self.jobs_list = QListWidget()
        layout.addWidget(self.jobs_list)

        # Load jobs (later: filter by crew cell & active status)
        self.load_jobs()

        # Buttons row
        self.select_button = QPushButton("Select Job")
        self.create_button = QPushButton("Create New Job")

        layout.addWidget(self.select_button)
        layout.addWidget(self.create_button)

        # Connect actions
        self.select_button.clicked.connect(self.select_job)
        self.create_button.clicked.connect(self.create_new_job)

    def load_jobs(self):
        """Load active jobs from the database."""
        try:
            conn = get_connection(db_name=config.DB_NAME)
            with conn.cursor() as cursor:
                query = """
                    SELECT job_name, crew_cell, status
                    FROM jobs
                    WHERE status = 'active'
                """
                cursor.execute(query)
                active_jobs = cursor.fetchall()
            conn.close()
        except Exception as e:
            self.jobs_list.clear()
            self.jobs_list.addItem(f"Error loading jobs: {e}")
            return

        self.jobs_list.clear()
        for job in active_jobs:
            job_name, crew_cell, status = job
            item_text = f"{job_name} | {crew_cell} | {status}"
            self.jobs_list.addItem(QListWidgetItem(item_text))

    def select_job(self):
        """Handle job selection."""
        selected_items = self.jobs_list.selectedItems()
        if selected_items:
            job = selected_items[0].text()
            print(f"✅ Job selected: {job}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a job first.")


    def create_new_job(self):
        """Handle creation of a new job with crew cell selection."""
        try:
            conn = get_connection(db_name=config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute("SELECT crew_name FROM cells")
                crew_cells = [row[0] for row in cursor.fetchall()]
            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load crew cells: {e}")
            return

        # Custom dialog for job name and crew cell
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New Job")
        layout = QVBoxLayout(dialog)

        job_label = QLabel("Enter job name:")
        layout.addWidget(job_label)
        job_name_input = QInputDialog()
        job_name, ok = QInputDialog.getText(self, "New Job", "Enter job name:")
        if not ok or not job_name:
            return

        crew_label = QLabel("Select crew cell:")
        layout.addWidget(crew_label)
        crew_combo = QComboBox()
        crew_combo.addItems(crew_cells)
        layout.addWidget(crew_combo)

        ok_button = QPushButton("Create")
        layout.addWidget(ok_button)
        dialog.setLayout(layout)

        def on_create():
            crew_cell = crew_combo.currentText()
            # Check for active job
            try:
                conn = get_connection(db_name=config.DB_NAME)
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM jobs WHERE crew_cell=%s AND status='active'",
                        (crew_cell,)
                    )
                    exists = cursor.fetchone()[0]
                    if exists:
                        QMessageBox.warning(self, "Warning", f"Crew '{crew_cell}' already has an active job.")
                        dialog.reject()
                        return
                    cursor.execute(
                        "INSERT INTO jobs (job_name, crew_cell, status, started_at) VALUES (%s, %s, 'active', NOW())",
                        (job_name, crew_cell)
                    )
                    conn.commit()
                conn.close()
                QMessageBox.information(self, "Job Created", f"New job '{job_name}' for '{crew_cell}' created!")
                self.load_jobs()
                dialog.accept()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not create job: {e}")
                dialog.reject()

        ok_button.clicked.connect(on_create)
        dialog.exec()
