# admin/admin_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
import config
from db.connection import get_connection

class AdminWindow(QMainWindow):
    """
    Admin home page:
     - Shows active jobs (same listing as JobSelectionWindow)
     - Provides top menu bar:
         * Update Crew Cells
         * View All Jobs
    """

    def __init__(self, user_name, is_admin=True):
        super().__init__()
        self.user_name = user_name
        self.is_admin = is_admin

        self.setWindowTitle("Admin Dashboard")
        self.setFixedSize(1000, 600)

        # Central widget & main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # ===== Top row: Back arrow + title =====
        top_row = QHBoxLayout()
        arrow_btn = QPushButton("◀")
        arrow_btn.setObjectName("arrow_btn")
        arrow_btn.setFixedSize(40, 36)
        arrow_btn.setToolTip("Back to Home")
        arrow_btn.clicked.connect(self.go_to_init_window)

        title_label = QLabel(f"Admin Dashboard — Welcome, {self.user_name}!")
        title_label.setObjectName("admin_title")

        top_row.addWidget(arrow_btn)
        top_row.addWidget(title_label)
        top_row.addStretch()
        layout.addLayout(top_row)

        # ===== Menu Bar =====
        menu_bar = self.menuBar()
        options_menu = menu_bar.addMenu("Options")

        action_update_cells = options_menu.addAction("Update Crew Cells")
        action_view_all_jobs = options_menu.addAction("View All Jobs")

        # Connect menu actions
        action_update_cells.triggered.connect(self.open_update_crew_cells_window)
        action_view_all_jobs.triggered.connect(self.open_view_all_jobs_window)

        # ===== Horizontal Separator =====
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        # ===== Active Jobs List =====
        self.jobs_list = QListWidget()
        self.jobs_list.setObjectName("admin_jobs_list")
        layout.addWidget(self.jobs_list, stretch=1)

        # Load jobs after UI init
        self.load_jobs()

    def load_jobs(self):
        """Load active jobs from the database and populate the QListWidget."""
        try:
            conn = get_connection(db_name=config.DB_NAME)
            with conn.cursor() as cursor:
                query = """
                    SELECT id, job_name, crew_cell, district, status, session_user
                    FROM jobs
                    WHERE status = 'active'
                    ORDER BY job_name
                """
                cursor.execute(query)
                active_jobs = cursor.fetchall()
            conn.close()
        except Exception as e:
            self.jobs_list.clear()
            self.jobs_list.addItem(f"Error loading jobs: {e}")
            return

        self.jobs_list.clear()

        # Header (non-selectable)
        header_text = f"{'Job Name':<20} | {'Crew Cell':<18} | {'District':<18} | {'Status':<10} | {'Session User':<15}"
        header_item = QListWidgetItem(header_text)
        header_item.setFlags(Qt.ItemFlag.NoItemFlags)
        header_item.setForeground(Qt.GlobalColor.cyan)
        self.jobs_list.addItem(header_item)

        for job in active_jobs:
            job_id = job['id']
            job_name = job['job_name'] or ""
            crew_cell = job['crew_cell'] or ""
            crew_district = job['district'] or ""
            status = job['status'] or ""
            session_user = job.get('session_user') or ""

            item_text = (
                f"{job_name:<20} | "
                f"{crew_cell:<18} | "
                f"{crew_district:<18} | "
                f"{status:<10} | "
                f"{session_user:<15}"
            )
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, job_id)
            self.jobs_list.addItem(item)

    # --- Navigation / Window launching ---
    def open_update_crew_cells_window(self):
        """Open the full window that allows CRUD on crew cells."""
        try:
            from gui.crew_cells import CrewCellsWindow
        except Exception as e:
            print("Could not import CrewCellsWindow yet:", e)
            placeholder = self._placeholder_window("Update Crew Cells", "CrewCellsWindow not implemented yet.")
            placeholder.show()
            return

        self.crew_cells_window = CrewCellsWindow(user_name=self.user_name)
        self.crew_cells_window.show()
        self.close()

    def open_view_all_jobs_window(self):
        """Open a full window for 'View All Jobs'. Placeholder implementation now."""
        try:
            from admin.view_all_jobs_window import ViewAllJobsWindow
        except Exception as e:
            print("Could not import ViewAllJobsWindow yet:", e)
            placeholder = self._placeholder_window("View All Jobs", "Feature under development.")
            placeholder.show()
            return

        self.view_all_jobs_window = ViewAllJobsWindow(user_name=self.user_name)
        self.view_all_jobs_window.show()
        self.close()

    def _placeholder_window(self, title, message):
        """Minimal placeholder full window in case the real window is not implemented yet."""
        from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
        w = QMainWindow()
        w.setWindowTitle(title)
        w.setFixedSize(700, 400)
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(QLabel(message))
        back_btn = QPushButton("Back to Admin")
        back_btn.clicked.connect(lambda: (self.show(), w.close()))
        layout.addWidget(back_btn)
        w.setCentralWidget(central)
        return w

    def go_to_init_window(self):
        """Return to the init/home window (mirror JobSelection behavior)."""
        from init_window import InitWindow
        self.init_window = InitWindow()
        self.init_window.show()
        self.close()
