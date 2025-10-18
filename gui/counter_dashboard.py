# gui/counter_dashboard.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QSpinBox, QCheckBox, QPushButton, QTextEdit, QLineEdit, QMessageBox

)
from PyQt6.QtCore import QTimer, QPropertyAnimation, QPoint, QEasingCurve
import config
from db.connection import get_connection
from utils.log_entry import add_log_entry_db

from datetime import datetime
import pytz

log_events_types= ["Login", "AddStage", "MinusStage", "Rehead", "Edit", "Database", "Error"] # Predefined event types for logging

class CounterDashboardWindow(QMainWindow):
    def __init__(self, job_id, user_name="USER"):
        super().__init__()
        self.job_id = job_id
        self.user_name = user_name
        self.job_name = "JOB NAME"  # Placeholder
        self.crew_cell = "CREW CELL"  # Placeholder

        # Start periodic session validation
        self.session_check_timer = QTimer(self)
        self.session_check_timer.timeout.connect(self.check_session_validity)
        self.session_check_timer.start(60000)  # every 60 seconds

        self.setWindowTitle("Counter Dashboard")
        self.setFixedSize(1000, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Section0: Info
        self.info_label = QLabel(f"Stage Tracker | Job: {self.job_name} | Crew: {self.crew_cell}")
        self.info_label.setObjectName("info_label")

        top_row = QHBoxLayout()

        #button to job_selection
        job_select_btn = QPushButton("◀")
        job_select_btn.setObjectName("job_select_btn")
        job_select_btn.setFixedSize(40, 36)
        job_select_btn.setToolTip("Back to Job Selection")
        job_select_btn.clicked.connect(self.go_to_job_selection)
        top_row.addWidget(job_select_btn)

        top_row.addWidget(self.info_label)
        top_row.addStretch()
        main_layout.insertLayout(0, top_row)


        # Section1: Edit counters checkbox
        self.edit_counters_checkbox = QCheckBox("Edit Counters")
        self.edit_counters_checkbox.setChecked(False)

        self.edit_counters_checkbox.stateChanged.connect(self.toggle_all_counters)
        main_layout.addWidget(self.edit_counters_checkbox)

        # Section2: Main counter controls grid (7 columns, 3 rows)
        main_grid = QGridLayout()

        # Row 0: Checkboxes (only for first 4 counters)
        self.roh_enable_checkbox = QCheckBox()
        self.roh_enable_checkbox.setChecked(True)
        main_grid.addWidget(self.roh_enable_checkbox, 0, 0)
        self.top_rubber_enable_checkbox = QCheckBox()
        main_grid.addWidget(self.top_rubber_enable_checkbox, 0, 1)
        self.middle_rubber_enable_checkbox = QCheckBox()
        main_grid.addWidget(self.middle_rubber_enable_checkbox, 0, 2)
        self.low_rubber_enable_checkbox = QCheckBox()
        self.low_rubber_enable_checkbox.setChecked(True)
        main_grid.addWidget(self.low_rubber_enable_checkbox, 0, 3)
        # No checkbox for Shot, Remain, Total
        main_grid.addWidget(QWidget(), 0, 4)  # Empty placeholder
        main_grid.addWidget(QWidget(), 0, 5)
        main_grid.addWidget(QWidget(), 0, 6)

        # Row 1: Labels
        self.roh_label = QLabel("ROH")
        self.roh_label.setObjectName("roh_label")
        main_grid.addWidget(self.roh_label, 1, 0)

        self.top_rubber_label = QLabel("Top\nRubber")
        self.top_rubber_label.setObjectName("top_rubber_label")
        main_grid.addWidget(self.top_rubber_label, 1, 1)

        self.middle_rubber_label = QLabel("Middle\nRubber")
        self.middle_rubber_label.setObjectName("middle_rubber_label")
        main_grid.addWidget(self.middle_rubber_label, 1, 2)

        self.low_rubber_label = QLabel("Low\nRubber")
        self.low_rubber_label.setObjectName("low_rubber_label")
        main_grid.addWidget(self.low_rubber_label, 1, 3)

        self.shot_label = QLabel("Shot")
        self.shot_label.setObjectName("shot_label")
        main_grid.addWidget(self.shot_label, 1, 4)

        self.remain_label = QLabel("Remain")
        self.remain_label.setObjectName("remain_label")
        main_grid.addWidget(self.remain_label, 1, 5)

        self.total_label = QLabel("Total")
        self.total_label.setObjectName("total_label")
        main_grid.addWidget(self.total_label, 1, 6)


        # Row 2: Spinboxes
        self.roh_spinbox = QSpinBox()
        self.roh_spinbox.setObjectName("roh_spinbox")
        self.roh_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.roh_spinbox, 2, 0)

        self.top_rubber_spinbox = QSpinBox()
        self.top_rubber_spinbox.setObjectName("top_rubber_spinbox")
        self.top_rubber_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.top_rubber_spinbox, 2, 1)

        self.middle_rubber_spinbox = QSpinBox()
        self.middle_rubber_spinbox.setObjectName("middle_rubber_spinbox")
        self.middle_rubber_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.middle_rubber_spinbox, 2, 2)

        self.low_rubber_spinbox = QSpinBox()
        self.low_rubber_spinbox.setObjectName("low_rubber_spinbox")
        self.low_rubber_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.low_rubber_spinbox, 2, 3)

        self.shot_spinbox = QSpinBox()
        self.shot_spinbox.setObjectName("shot_spinbox")
        self.shot_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.shot_spinbox, 2, 4)

        self.remain_spinbox = QSpinBox()
        self.remain_spinbox.setObjectName("remain_spinbox")
        self.remain_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.remain_spinbox, 2, 5)
        self.remain_spinbox.setEnabled(False)  # Remain is not editable

        self.total_spinbox = QSpinBox()
        self.total_spinbox.setObjectName("total_spinbox")
        self.total_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.total_spinbox, 2, 6)

        main_layout.addLayout(main_grid)



        # Section3: Assets & buttons
        row3_layout = QHBoxLayout()
        assets_grid = QGridLayout()

        # Asset 1
        self.asset1_checkbox = QCheckBox()
        self.asset1_checkbox.setChecked(True)
        self.asset1_serial_entry = QLineEdit()
        self.asset1_serial_entry.setObjectName("asset1_serial_entry")
        self.asset1_spinbox = QSpinBox()
        self.asset1_spinbox.setObjectName("asset1_spinbox")
        assets_grid.addWidget(self.asset1_checkbox, 0, 0)
        assets_grid.addWidget(self.asset1_serial_entry, 0, 1)
        assets_grid.addWidget(self.asset1_spinbox, 0, 2)
        self.asset1_serial_entry.setPlaceholderText("Asset 1 Serial")

        # Asset 2
        self.asset2_checkbox = QCheckBox()
        self.asset2_serial_entry = QLineEdit()
        self.asset2_serial_entry.setObjectName("asset2_serial_entry")
        self.asset2_spinbox = QSpinBox()
        self.asset2_spinbox.setObjectName("asset2_spinbox")
        assets_grid.addWidget(self.asset2_checkbox, 1, 0)
        assets_grid.addWidget(self.asset2_serial_entry, 1, 1)
        assets_grid.addWidget(self.asset2_spinbox, 1, 2)
        self.asset2_serial_entry.setPlaceholderText("Asset 2 Serial")

        # Asset 3
        self.asset3_checkbox = QCheckBox()
        self.asset3_serial_entry = QLineEdit()
        self.asset3_serial_entry.setObjectName("asset3_serial_entry")
        self.asset3_spinbox = QSpinBox()
        self.asset3_spinbox.setObjectName("asset3_spinbox")
        assets_grid.addWidget(self.asset3_checkbox, 2, 0)
        assets_grid.addWidget(self.asset3_serial_entry, 2, 1)
        assets_grid.addWidget(self.asset3_spinbox, 2, 2)
        self.asset3_serial_entry.setPlaceholderText("Asset 3 Serial")

        # Asset 4
        self.asset4_checkbox = QCheckBox()
        self.asset4_serial_entry = QLineEdit()
        self.asset4_serial_entry.setObjectName("asset4_serial_entry")
        self.asset4_spinbox = QSpinBox()
        self.asset4_spinbox.setObjectName("asset4_spinbox")
        assets_grid.addWidget(self.asset4_checkbox, 3, 0)
        assets_grid.addWidget(self.asset4_serial_entry, 3, 1)
        assets_grid.addWidget(self.asset4_spinbox, 3, 2)
        self.asset4_serial_entry.setPlaceholderText("Asset 4 Serial")

        # Asset 5
        self.asset5_checkbox = QCheckBox()
        self.asset5_serial_entry = QLineEdit()
        self.asset5_serial_entry.setObjectName("asset5_serial_entry")
        self.asset5_spinbox = QSpinBox()
        self.asset5_spinbox.setObjectName("asset5_spinbox")
        assets_grid.addWidget(self.asset5_checkbox, 4, 0)
        assets_grid.addWidget(self.asset5_serial_entry, 4, 1)
        assets_grid.addWidget(self.asset5_spinbox, 4, 2)
        self.asset5_serial_entry.setPlaceholderText("Asset 5 Serial")

        # Asset 6
        self.asset6_checkbox = QCheckBox()
        self.asset6_serial_entry = QLineEdit()
        self.asset6_serial_entry.setObjectName("asset6_serial_entry")
        self.asset6_spinbox = QSpinBox()
        self.asset6_spinbox.setObjectName("asset6_spinbox")
        assets_grid.addWidget(self.asset6_checkbox, 5, 0)
        assets_grid.addWidget(self.asset6_serial_entry, 5, 1)
        assets_grid.addWidget(self.asset6_spinbox, 5, 2)
        self.asset6_serial_entry.setPlaceholderText("Asset 6 Serial")

        row3_layout.addLayout(assets_grid)

        # Section 3 - Buttons: Buttons vertical layout
        btn_layout = QVBoxLayout()
        self.plus_stage_btn = QPushButton("+Stage")
        self.minus_stage_btn = QPushButton("-Stage")
        self.rehead_btn = QPushButton("Rehead")
        self.finish_job_btn = QPushButton("Finish Job")
        btn_layout.addWidget(self.plus_stage_btn)
        btn_layout.addWidget(self.minus_stage_btn)
        btn_layout.addWidget(self.rehead_btn)
        btn_layout.addWidget(self.finish_job_btn)
        row3_layout.addLayout(btn_layout)
        main_layout.addLayout(row3_layout)



        # Section4: Footer
        self.log_window = QTextEdit()
        self.log_window.setObjectName("log_window")
        self.log_window.setReadOnly(True)
        self.log_window.setFixedHeight(100)  # Adjust height as needed
        main_layout.addWidget(self.log_window)

        # Button connections
        self.plus_stage_btn.clicked.connect(self.increase_stage)
        self.minus_stage_btn.clicked.connect(self.decrease_stage)
        self.rehead_btn.clicked.connect(self.rehead_roh)
        self.finish_job_btn.clicked.connect(self.finish_job)

        #Initialize Counter_dashboard state
        self.download_counters()  # Load counters from DB
        self.init_disable_all_counters()  # Disable all counters initially
        #self.download_logs()
        self.update_logs(event_type="Login", message=f"User '{self.user_name}' logged in.")

    def toggle_all_counters(self, state):
        enabled = state == 2

        button_symbols = QSpinBox.ButtonSymbols.UpDownArrows if enabled else QSpinBox.ButtonSymbols.NoButtons

        spinboxes = [
            self.roh_spinbox, self.top_rubber_spinbox, self.middle_rubber_spinbox,
            self.low_rubber_spinbox, self.shot_spinbox, self.remain_spinbox, self.total_spinbox,
            self.asset1_spinbox, self.asset2_spinbox, self.asset3_spinbox,
            self.asset4_spinbox, self.asset5_spinbox, self.asset6_spinbox
        ]

        for spinbox in spinboxes:
            spinbox.setEnabled(enabled)
            spinbox.setButtonSymbols(button_symbols)

        serial_entries = [
            self.asset1_serial_entry, self.asset2_serial_entry, self.asset3_serial_entry,
            self.asset4_serial_entry, self.asset5_serial_entry, self.asset6_serial_entry
        ]
        for entry in serial_entries:
            entry.setEnabled(enabled)

            # Disable stage/job buttons and gray out when editing is enabled
            for btn in [self.plus_stage_btn, self.minus_stage_btn, self.rehead_btn, self.finish_job_btn]:
                btn.setEnabled(not enabled)
                if enabled:
                    btn.setStyleSheet("background-color: lightgray;")
                else:
                    btn.setStyleSheet("")

        self.update_remain()

        if state == 0:
            self.update_logs(event_type="Edit", message="Counter Values Edited Manually.")
            self.update_counters()

    def increase_stage(self):
        self.show_floating_text("+1 Stage")
        if self.roh_enable_checkbox.isChecked():
            self.roh_spinbox.setValue(self.roh_spinbox.value() + 1)
        if self.top_rubber_enable_checkbox.isChecked():
            self.top_rubber_spinbox.setValue(self.top_rubber_spinbox.value() + 1)
        if self.middle_rubber_enable_checkbox.isChecked():
            self.middle_rubber_spinbox.setValue(self.middle_rubber_spinbox.value() + 1)
        if self.low_rubber_enable_checkbox.isChecked():
            self.low_rubber_spinbox.setValue(self.low_rubber_spinbox.value() + 1)
        if self.shot_spinbox.value() >= 0:
            self.shot_spinbox.setValue(self.shot_spinbox.value() + 1)
        if self.asset1_checkbox.isChecked():
            self.asset1_spinbox.setValue(self.asset1_spinbox.value() + 1)
        if self.asset2_checkbox.isChecked():
            self.asset2_spinbox.setValue(self.asset2_spinbox.value() + 1)
        if self.asset3_checkbox.isChecked():
            self.asset3_spinbox.setValue(self.asset3_spinbox.value() + 1)
        if self.asset4_checkbox.isChecked():
            self.asset4_spinbox.setValue(self.asset4_spinbox.value() + 1)
        if self.asset5_checkbox.isChecked():
            self.asset5_spinbox.setValue(self.asset5_spinbox.value() + 1)
        if self.asset6_checkbox.isChecked():
            self.asset6_spinbox.setValue(self.asset6_spinbox.value() + 1)

        self.update_remain()
        self.update_logs(event_type="AddStage", message="Counters increased +1 Stage.")
        self.update_counters()

    def decrease_stage(self):
        self.show_floating_text("-1 Stage")
        if self.roh_enable_checkbox.isChecked() and self.roh_spinbox.value() > 0:
            self.roh_spinbox.setValue(self.roh_spinbox.value() - 1)
        if self.top_rubber_enable_checkbox.isChecked() and self.top_rubber_spinbox.value() > 0:
            self.top_rubber_spinbox.setValue(self.top_rubber_spinbox.value() - 1)
        if self.middle_rubber_enable_checkbox.isChecked() and self.middle_rubber_spinbox.value() > 0:
            self.middle_rubber_spinbox.setValue(self.middle_rubber_spinbox.value() - 1)
        if self.low_rubber_enable_checkbox.isChecked() and self.low_rubber_spinbox.value() > 0:
            self.low_rubber_spinbox.setValue(self.low_rubber_spinbox.value() - 1)
        if self.shot_spinbox.value()>= 1:
            self.shot_spinbox.setValue(self.shot_spinbox.value() - 1)
        if self.asset1_checkbox.isChecked() and self.asset1_spinbox.value() > 0:
            self.asset1_spinbox.setValue(self.asset1_spinbox.value() - 1)
        if self.asset2_checkbox.isChecked() and self.asset2_spinbox.value() > 0:
            self.asset2_spinbox.setValue(self.asset2_spinbox.value() - 1)
        if self.asset3_checkbox.isChecked() and self.asset3_spinbox.value()> 0:
            self.asset3_spinbox.setValue(self.asset3_spinbox.value() - 1)
        if self.asset4_checkbox.isChecked() and self.asset4_spinbox.value() > 0:
            self.asset4_spinbox.setValue(self.asset4_spinbox.value() - 1)
        if self.asset5_checkbox.isChecked() and self.asset5_spinbox.value() > 0:
            self.asset5_spinbox.setValue(self.asset5_spinbox.value() - 1)
        if self.asset6_checkbox.isChecked() and self.asset6_spinbox.value() > 0:
            self.asset6_spinbox.setValue(self.asset6_spinbox.value() - 1)

        self.update_remain()
        self.update_logs(event_type="MinusStage", message="Counters decreased -1 Stage.")
        self.update_counters()

    def rehead_roh(self):
        self.show_floating_text("Rehead")
        self.roh_spinbox.setValue(0)
        self.update_logs(event_type="Rehead", message="ROH counter reheaded to 0.")
        self.update_counters()

    def update_remain(self):
        remain_value = self.total_spinbox.value() - self.shot_spinbox.value()
        self.remain_spinbox.setValue(remain_value)

    def download_counters(self):
        try:
            conn = get_connection(db_name=config.DB_NAME)
            with conn.cursor() as cursor:
                # Get job_name and crew_cell by key
                cursor.execute("SELECT job_name, crew_cell FROM jobs WHERE id = %s", (self.job_id,))
                job_row = cursor.fetchone()
                if job_row:
                    self.job_name = job_row['job_name'] if job_row['job_name'] is not None else "JOB NAME"
                    self.crew_cell = job_row['crew_cell'] if job_row['crew_cell'] is not None else "CREW CELL"
                    self.info_label.setText(f"Stage Tracker | Job: {self.job_name} | Crew: {self.crew_cell}")
                else:
                    self.job_name = "JOB NAME"
                    self.crew_cell = "CREW CELL"

                # Get counters row by key
                cursor.execute(
                    "SELECT roh, top_rubber, middle_rubber, low_rubber, shot, remain, total, asset_1, asset_1_name, asset_2, asset_2_name, asset_3, asset_3_name, asset_4, asset_4_name, asset_5, asset_5_name, asset_6, asset_6_name FROM counters WHERE job_id = %s",
                    (self.job_id,))
                row = cursor.fetchone()
            conn.close()

            if row:
                self.roh_spinbox.setValue(row['roh'])
                self.top_rubber_spinbox.setValue(row['top_rubber'])
                self.middle_rubber_spinbox.setValue(row['middle_rubber'])
                self.low_rubber_spinbox.setValue(row['low_rubber'])
                self.shot_spinbox.setValue(row['shot'])
                self.remain_spinbox.setValue(row['remain'])
                self.total_spinbox.setValue(row['total'])

                self.asset1_spinbox.setValue(row['asset_1'])
                self.asset1_serial_entry.setText(row['asset_1_name'])
                self.asset2_spinbox.setValue(row['asset_2'])
                self.asset2_serial_entry.setText(row['asset_2_name'])
                self.asset3_spinbox.setValue(row['asset_3'])
                self.asset3_serial_entry.setText(row['asset_3_name'])
                self.asset4_spinbox.setValue(row['asset_4'])
                self.asset4_serial_entry.setText(row['asset_4_name'])
                self.asset5_spinbox.setValue(row['asset_5'])
                self.asset5_serial_entry.setText(row['asset_5_name'])
                self.asset6_spinbox.setValue(row['asset_6'])
                self.asset6_serial_entry.setText(row['asset_6_name'])

                self.update_logs(event_type="Database", message="Counter values loaded from database.")
            else:
                self.update_logs(event_type="Database", message="No counter values found for this job in database.")

        except Exception as e:
            self.update_logs(event_type="Error", message=f"Error loading counters from database: {e}")

    def update_counters(self):
        try:
            conn = get_connection(db_name=config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE counters SET
                        roh = %s,
                        top_rubber = %s,
                        middle_rubber = %s,
                        low_rubber = %s,
                        shot = %s,
                        remain = %s,
                        total = %s,
                        asset_1 = %s,
                        asset_1_name = %s,
                        asset_2 = %s,
                        asset_2_name = %s,
                        asset_3 = %s,
                        asset_3_name = %s,
                        asset_4 = %s,
                        asset_4_name = %s,
                        asset_5 = %s,
                        asset_5_name = %s,
                        asset_6 = %s,
                        asset_6_name = %s
                    WHERE job_id = %s
                    """,
                    (
                        self.roh_spinbox.value(),
                        self.top_rubber_spinbox.value(),
                        self.middle_rubber_spinbox.value(),
                        self.low_rubber_spinbox.value(),
                        self.shot_spinbox.value(),
                        self.remain_spinbox.value(),
                        self.total_spinbox.value(),
                        self.asset1_spinbox.value(),
                        self.asset1_serial_entry.text(),
                        self.asset2_spinbox.value(),
                        self.asset2_serial_entry.text(),
                        self.asset3_spinbox.value(),
                        self.asset3_serial_entry.text(),
                        self.asset4_spinbox.value(),
                        self.asset4_serial_entry.text(),
                        self.asset5_spinbox.value(),
                        self.asset5_serial_entry.text(),
                        self.asset6_spinbox.value(),
                        self.asset6_serial_entry.text(),
                        self.job_id
                    )
                )
                conn.commit()
            conn.close()
            self.update_logs(event_type="Database", message="Counter values updated in database.")
        except Exception as e:
            self.update_logs(event_type="Database", message=f"Error updating counters in database: {e}")

    def get_widget_values(self):
        return {
            "roh": self.roh_spinbox.value(),
            "top_rubber": self.top_rubber_spinbox.value(),
            "middle_rubber": self.middle_rubber_spinbox.value(),
            "low_rubber": self.low_rubber_spinbox.value(),
            "shot": self.shot_spinbox.value(),
            "remain": self.remain_spinbox.value(),
            "total": self.total_spinbox.value(),
            "asset_1": self.asset1_spinbox.value(),
            "asset_1_name": self.asset1_serial_entry.text(),
            "asset_2": self.asset2_spinbox.value(),
            "asset_2_name": self.asset2_serial_entry.text(),
            "asset_3": self.asset3_spinbox.value(),
            "asset_3_name": self.asset3_serial_entry.text(),
            "asset_4": self.asset4_spinbox.value(),
            "asset_4_name": self.asset4_serial_entry.text(),
            "asset_5": self.asset5_spinbox.value(),
            "asset_5_name": self.asset5_serial_entry.text(),
            "asset_6": self.asset6_spinbox.value(),
            "asset_6_name": self.asset6_serial_entry.text()
        }

    def download_logs(self):
        try:
            conn = get_connection(db_name=config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM (
                        SELECT id, timestamp, user_name, event_type, message
                        FROM logs
                        WHERE job_id = %s
                        ORDER BY id DESC
                        LIMIT 20
                    ) AS sub
                    ORDER BY id ASC
                    """,
                    (self.job_id,)
                )
                logs = cursor.fetchall()
            conn.close()
            self.log_window.clear()
            for log in logs:
                # Convert UTC timestamp to America/Chicago
                utc = pytz.utc
                chicago = pytz.timezone("America/Chicago")
                utc_dt = utc.localize(datetime.strptime(str(log['timestamp']), "%Y-%m-%d %H:%M:%S"))
                local_dt = utc_dt.astimezone(chicago)
                local_timestamp = local_dt.strftime("%Y-%m-%d %H:%M:%S")
                entry = (
                    f"[{local_timestamp}] "
                    f"[{log['event_type']}] | "
                    f"user_name: {log['user_name']} | "
                    f"message: {log['message']}"
                )
                self.log_window.append(entry)
        except Exception as e:
            self.log_window.append(f"Error loading logs: {e}")

    def update_logs(self, event_type, message):
        log_job_id = self.job_id
        log_user_name = self.user_name
        log_event_type = event_type
        log_new_value = self.get_widget_values()
        log_message = message
        add_log_entry_db(job_id=log_job_id, user_name=log_user_name, event_type=log_event_type,
                         new_value=log_new_value, message=log_message)
        # Also update the log window in the GUI
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry= (
            f"[{timestamp}] "
            f"[{log_event_type}] "
            f"user_name: {log_user_name} | "
            f"event_type: {log_event_type} | "
            #f"new_value: {log_new_value} | "
            f"message: {log_message}"
        )
        self.log_window.append(entry)

    def init_disable_all_counters(self):
        spinboxes = [
            self.roh_spinbox, self.top_rubber_spinbox, self.middle_rubber_spinbox,
            self.low_rubber_spinbox, self.shot_spinbox, self.remain_spinbox,  self.total_spinbox,
            self.asset1_spinbox, self.asset2_spinbox, self.asset3_spinbox,
            self.asset4_spinbox, self.asset5_spinbox, self.asset6_spinbox
        ]

        for spinbox in spinboxes:
            spinbox.setEnabled(False)
            spinbox.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)

        self.asset1_serial_entry.setEnabled(False)
        self.asset2_serial_entry.setEnabled(False)
        self.asset3_serial_entry.setEnabled(False)
        self.asset4_serial_entry.setEnabled(False)
        self.asset5_serial_entry.setEnabled(False)
        self.asset6_serial_entry.setEnabled(False)

    def finish_job(self):
        reply = QMessageBox.question(
            self,
            "Finish Job",
            f"Finish the Job: {self.job_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = get_connection(db_name=config.DB_NAME)
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE jobs SET status = %s, finished_at = %s WHERE id = %s",
                        ("finished", datetime.now(), self.job_id)
                    )
                    conn.commit()
                conn.close()

                self.update_logs(event_type="Database", message=f"Job '{self.job_name}' marked as finished.")

                from init_window import InitWindow  # Import here to avoid circular import
                self.init_win = InitWindow()
                self.init_win.show()
                self.close()  # Close the dashboard

            except Exception as e:
                self.update_logs(event_type="Error", message=f"Error finishing job: {e}")

    def check_session_validity(self):
        """Periodically check if current session user still matches this user."""
        try:
            conn = get_connection(db_name=config.DB_NAME)
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT session_user FROM jobs WHERE id = %s", (self.job_id,)
                )
                result = cursor.fetchone()
            conn.close()

            if result and result['session_user'] != self.user_name:
                # Stop timer immediately
                self.session_check_timer.stop()

                self.update_logs(event_type="Session",
                                 message=f"Session taken over by '{result['session_user']}'. Logging out '{self.user_name}'.")

                # Notify user
                QMessageBox.warning(
                    self,
                    "Session Taken",
                    f"Session has been taken by user '{result['session_user']}'.\nYou will be logged out.",
                )

                # Close this dashboard and return to job selection
                from gui.job_selection import JobSelectionWindow
                self.job_selection_window = JobSelectionWindow(user_name=self.user_name)
                self.job_selection_window.show()
                self.close()

        except Exception as e:
            print("Error checking session validity:", e)

    def show_floating_text(self, text: str):
        floating_label = QLabel(text, self)
        floating_label.setObjectName("floating_text")
        floating_label.adjustSize()

        # Center it
        center_x = (self.width() - floating_label.width()) // 2
        center_y = (self.height() - floating_label.height()) // 2
        floating_label.move(center_x, center_y)
        floating_label.show()

        # Position animation
        pos_anim = QPropertyAnimation(floating_label, b"pos", floating_label)
        pos_anim.setDuration(2000)
        pos_anim.setStartValue(QPoint(center_x, center_y))
        pos_anim.setEndValue(QPoint(center_x, center_y - 80))
        pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Opacity animation
        opacity_anim = QPropertyAnimation(floating_label, b"windowOpacity", floating_label)
        opacity_anim.setDuration(2000)
        opacity_anim.setStartValue(1.0)
        opacity_anim.setEndValue(0.0)
        opacity_anim.setEasingCurve(QEasingCurve.Type.InCubic)

        # Delete after finishing
        opacity_anim.finished.connect(floating_label.deleteLater)

        # Start animations
        pos_anim.start()
        opacity_anim.start()

    def go_to_job_selection(self):
        from gui.job_selection import JobSelectionWindow
        self.job_selection_window = JobSelectionWindow(user_name=self.user_name)
        self.job_selection_window.show()
        self.close()




