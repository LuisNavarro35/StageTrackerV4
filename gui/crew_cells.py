# gui/crew_cells_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QHBoxLayout, QInputDialog, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
import config
from db.connection import get_connection

class CrewCellsWindow(QMainWindow):
    """
    Admin full window to manage Crew Cells:
     - List all crew cells grouped by district
     - Add / Edit / Delete
    """
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.setWindowTitle("Update Crew Cells")
        self.setFixedSize(800, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Top row: back arrow + title
        top_row = QHBoxLayout()
        arrow_btn = QPushButton("◀")
        arrow_btn.setFixedSize(40, 36)
        arrow_btn.setToolTip("Back to Admin")
        arrow_btn.clicked.connect(self.go_back_to_admin)

        title_label = QLabel("Manage Crew Cells")
        top_row.addWidget(arrow_btn)
        top_row.addWidget(title_label)
        top_row.addStretch()
        layout.addLayout(top_row)

        # Crew cells list
        self.crew_list = QListWidget()
        layout.addWidget(self.crew_list, stretch=1)

        # Action buttons
        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("Add Crew Cell")
        self.edit_btn = QPushButton("Edit Selected")
        self.delete_btn = QPushButton("Delete Selected")
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.delete_btn)
        layout.addLayout(btn_row)

        # Connect actions
        self.add_btn.clicked.connect(self.add_crew_cell)
        self.edit_btn.clicked.connect(self.edit_crew_cell)
        self.delete_btn.clicked.connect(self.delete_crew_cell)

        # Load initial list
        self.load_crew_cells()

    def load_crew_cells(self):
        """Load all crew cells from DB, grouped by district"""
        try:
            conn = get_connection(config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, crew_name, district FROM cells ORDER BY district, crew_name")
                rows = cursor.fetchall()
            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load crew cells: {e}")
            return

        self.crew_list.clear()
        for row in rows:
            item_text = f"{row['crew_name']} ({row['district']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, row['id'])
            self.crew_list.addItem(item)

    def add_crew_cell(self):
        """Add a new crew cell"""
        # Input district
        district, ok = QInputDialog.getText(self, "New Crew Cell", "Enter district:")
        if not ok or not district:
            return

        # Input crew name
        crew_name, ok = QInputDialog.getText(self, "New Crew Cell", "Enter crew cell name:")
        if not ok or not crew_name:
            return

        try:
            conn = get_connection(config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO cells (crew_name, district) VALUES (%s, %s)",
                    (crew_name, district)
                )
                conn.commit()
            conn.close()
            self.load_crew_cells()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not add crew cell: {e}")

    def edit_crew_cell(self):
        """Edit selected crew cell"""
        selected = self.crew_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Select", "Select a crew cell first.")
            return
        item = selected[0]
        crew_id = item.data(Qt.ItemDataRole.UserRole)

        # Input new name
        new_name, ok = QInputDialog.getText(self, "Edit Crew Cell", "Enter new crew name:", text=item.text().split("(")[0].strip())
        if not ok or not new_name:
            return

        try:
            conn = get_connection(config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute("UPDATE cells SET crew_name=%s WHERE id=%s", (new_name, crew_id))
                conn.commit()
            conn.close()
            self.load_crew_cells()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not edit crew cell: {e}")

    def delete_crew_cell(self):
        """Delete selected crew cell"""
        selected = self.crew_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Select", "Select a crew cell first.")
            return
        item = selected[0]
        crew_id = item.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(self, "Confirm Delete", f"Delete {item.text()}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            conn = get_connection(config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cells WHERE id=%s", (crew_id,))
                conn.commit()
            conn.close()
            self.load_crew_cells()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not delete crew cell: {e}")

    def go_back_to_admin(self):
        from gui.admin_window import AdminWindow
        self.admin_window = AdminWindow(user_name=self.user_name)
        self.admin_window.show()
        self.close()
