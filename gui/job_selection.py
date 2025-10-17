from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QInputDialog, QMessageBox, QListWidgetItem, QDialog, QComboBox, QHBoxLayout
)

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
import config
from db.connection import get_connection
from gui.counter_dashboard import CounterDashboardWindow
from utils.log_entry import add_log_entry_db

class JobSelectionWindow(QMainWindow):
    def __init__(self, user_name, is_admin=False):
        super().__init__()
        self.user_name = user_name
        self.is_admin = is_admin

        self.setWindowTitle("Job Selection")
        self.setFixedSize(1000, 600)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)

        # In __init__ after setting up layout
        arrow_btn = QPushButton("◀")  # or "⬅", "↩", "⮐", "◀" — pick any arrow you like
        arrow_btn.setObjectName("arrow_btn")
        arrow_btn.setFixedSize(40, 36)
        arrow_btn.setToolTip("Back to Home")
        arrow_btn.clicked.connect(self.go_to_init_window)


        # Welcome label
        self.welcome_label = QLabel(f"Welcome, {self.user_name}!")

        # Place arrow and welcome label in a horizontal layout
        top_row = QHBoxLayout()
        top_row.addWidget(arrow_btn)
        top_row.addWidget(self.welcome_label)
        top_row.addStretch()
        layout.insertLayout(0, top_row)  # Add at the top

        # layout.addWidget(self.welcome_label)

        # Jobs list
        self.jobs_list = QListWidget()
        self.jobs_list.setObjectName("jobs_list")
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
                    SELECT id, job_name, crew_cell, district, status, session_user
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

        # Add header row
        header_text = f"{'Job Name':<15} | {'Crew Cell':<15} | {'District':<15} | {'Status':<15} | {'Session User':<15}"
        header_item = QListWidgetItem(header_text)
        header_item.setFlags(Qt.ItemFlag.NoItemFlags)
        header_item.setForeground(Qt.GlobalColor.cyan)
        self.jobs_list.addItem(header_item)

        for job in active_jobs:
            id = job['id']
            job_name = job['job_name']
            crew_cell = job['crew_cell']
            crew_district= job['district']
            status = job['status']
            session_user = job['session_user'] if 'session_user' in job else None
            item_text = (
                f"{job_name:<15} | "
                f"{crew_cell:<15} | "
                f"{crew_district:<15} | "
                f"{status:<15} | "
                f"{session_user:<15}"
            )
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, id)  # Store job_id
            self.jobs_list.addItem(item)

    def select_job(self):
        """Handle job selection."""
        selected_items = self.jobs_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a job first.")
            return

        item = selected_items[0]
        job_id = item.data(Qt.ItemDataRole.UserRole)

        try:
            conn = get_connection(db_name=config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute("SELECT session_user FROM jobs WHERE id=%s", (job_id,))
                row = cursor.fetchone()
            conn.close()

            if not row:
                QMessageBox.warning(self, "Error", "Selected job not found in database.")
                return

            current_session_user = row["session_user"]

            # If no session_user, assign it to this user
            if not current_session_user:
                self.assign_session_user(job_id)
                self.launch_dashboard(job_id)

            # If same user — allow entry
            elif current_session_user == self.user_name:
                add_log_entry_db(job_id=job_id, user_name=self.user_name, event_type="Session",
                                 new_value=None, message=f"Session user Allowed to: {self.user_name}")
                self.launch_dashboard(job_id)

            # If different user — confirm override
            else:
                reply = QMessageBox.question(
                    self,
                    "Job In Use",
                    f"This job is currently controlled by '{current_session_user}'.\n"
                    f"Do you want to take over (this will disconnect them)?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    add_log_entry_db(job_id=job_id, user_name=self.user_name, event_type="Session",
                                     new_value=None, message=f"Force Session Selected: {self.user_name}")
                    self.assign_session_user(job_id)
                    self.launch_dashboard(job_id)
                else:
                    return

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not check job session: {e}")
            return

    def assign_session_user(self, job_id):
        """Assign this user as the current session user."""
        try:
            conn = get_connection(db_name=config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE jobs SET session_user=%s, session_updated_at=NOW() WHERE id=%s",
                    (self.user_name, job_id)
                )
                conn.commit()
            conn.close()
            add_log_entry_db(job_id=job_id, user_name=self.user_name, event_type="Session",
                             new_value=None, message=f"Session user set to {self.user_name}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update session user: {e}")

    def launch_dashboard(self, job_id):
        """Open the dashboard window."""
        print(f"✅ Job id selected: {job_id} by {self.user_name}")
        self.job_counter_dashboard = CounterDashboardWindow(job_id=job_id, user_name=self.user_name)
        self.job_counter_dashboard.show()
        self.close()

    def create_new_job(self):
        """Handle creation of a new job with crew cell selection."""
        try:
            conn = get_connection(db_name=config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute("SELECT crew_name FROM cells")
                crew_cells = [row['crew_name'] for row in cursor.fetchall()]
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

            try:
                conn = get_connection(db_name=config.DB_NAME)
                with conn.cursor() as cursor:
                    # Get district for the selected crew_cell
                    cursor.execute(
                        "SELECT district FROM cells WHERE crew_name=%s LIMIT 1",
                        (crew_cell,)
                    )
                    row = cursor.fetchone()
                    district = row['district'] if row else None
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not retrieve district: {e}")
                dialog.reject()
                return



            try:
                conn = get_connection(db_name=config.DB_NAME)
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM jobs WHERE crew_cell=%s AND status='active' LIMIT 1",
                        (crew_cell,)
                    )
                    exists = cursor.fetchone() is not None
                    if exists:
                        QMessageBox.warning(self, "Warning", f"Crew '{crew_cell}' already has an active job.")
                        dialog.reject()
                        return

                    # Insert new job
                    cursor.execute(
                        """
                        INSERT INTO jobs (job_name, crew_cell, district, status, started_at, session_user)
                        VALUES (%s, %s, %s, 'active', NOW(), %s)
                        """,
                        (job_name, crew_cell, district,  self.user_name)
                    )

                    job_id = cursor.lastrowid

                    # Initialize counters for the new job
                    cursor.execute(
                        """
                        INSERT INTO counters (
                            job_id, roh, top_rubber, middle_rubber, low_rubber, shot, remain, total,
                            asset_1, asset_1_name, asset_2, asset_2_name, asset_3, asset_3_name,
                            asset_4, asset_4_name, asset_5, asset_5_name, asset_6, asset_6_name
                        ) VALUES (
                            %s, 0, 0, 0, 0, 0, 0, 0,
                            0, 'Asset 1', 0, 'Asset 2', 0, 'Asset 3',
                            0, 'Asset 4', 0, 'Asset 5', 0, 'Asset 6'
                        )
                        """,
                        (job_id,)
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

    def go_to_init_window(self):
        from gui.init_window import InitWindow
        self.init_window = InitWindow()
        self.init_window.show()
        self.close()