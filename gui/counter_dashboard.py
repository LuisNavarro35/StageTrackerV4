# gui/counter_dashboard.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QSpinBox, QCheckBox, QPushButton, QTextEdit, QLineEdit

)

class CounterDashboardWindow(QMainWindow):
    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id
        self.job_name = "JOB NAME"  # Placeholder
        self.crew_cell = "CREW CELL"  # Placeholder

        self.setWindowTitle("Counter Dashboard")
        self.setFixedSize(1000, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Section0: Info
        info_label = QLabel(f"Stage Tracker | Job: {self.job_name} | Crew: {self.crew_cell}")
        main_layout.addWidget(info_label)


        # Section1: Edit counters checkbox
        self.edit_counters_checkbox = QCheckBox("Enable editing all counters")
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
        main_grid.addWidget(QLabel("ROH"), 1, 0)
        main_grid.addWidget(QLabel("Top Rubber"), 1, 1)
        main_grid.addWidget(QLabel("Middle Rubber"), 1, 2)
        main_grid.addWidget(QLabel("Low Rubber"), 1, 3)
        main_grid.addWidget(QLabel("Shot"), 1, 4)
        main_grid.addWidget(QLabel("Remain"), 1, 5)
        main_grid.addWidget(QLabel("Total"), 1, 6)

        # Row 2: Spinboxes
        self.roh_spinbox = QSpinBox()
        self.roh_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.roh_spinbox, 2, 0)

        self.top_rubber_spinbox = QSpinBox()
        self.top_rubber_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.top_rubber_spinbox, 2, 1)

        self.middle_rubber_spinbox = QSpinBox()
        self.middle_rubber_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.middle_rubber_spinbox, 2, 2)

        self.low_rubber_spinbox = QSpinBox()
        self.low_rubber_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.low_rubber_spinbox, 2, 3)

        self.shot_spinbox = QSpinBox()
        self.shot_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.shot_spinbox, 2, 4)

        self.remain_spinbox = QSpinBox()
        self.remain_spinbox.setRange(0, 9999)
        main_grid.addWidget(self.remain_spinbox, 2, 5)
        self.remain_spinbox.setEnabled(False)  # Remain is not editable

        self.total_spinbox = QSpinBox()
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
        self.asset1_spinbox = QSpinBox()
        assets_grid.addWidget(self.asset1_checkbox, 0, 0)
        assets_grid.addWidget(self.asset1_serial_entry, 0, 1)
        assets_grid.addWidget(self.asset1_spinbox, 0, 2)
        self.asset1_serial_entry.setPlaceholderText("Asset 1 Serial")

        # Asset 2
        self.asset2_checkbox = QCheckBox()
        self.asset2_serial_entry = QLineEdit()
        self.asset2_spinbox = QSpinBox()
        assets_grid.addWidget(self.asset2_checkbox, 1, 0)
        assets_grid.addWidget(self.asset2_serial_entry, 1, 1)
        assets_grid.addWidget(self.asset2_spinbox, 1, 2)
        self.asset2_serial_entry.setPlaceholderText("Asset 2 Serial")

        # Asset 3
        self.asset3_checkbox = QCheckBox()
        self.asset3_serial_entry = QLineEdit()
        self.asset3_spinbox = QSpinBox()
        assets_grid.addWidget(self.asset3_checkbox, 2, 0)
        assets_grid.addWidget(self.asset3_serial_entry, 2, 1)
        assets_grid.addWidget(self.asset3_spinbox, 2, 2)
        self.asset3_serial_entry.setPlaceholderText("Asset 3 Serial")

        # Asset 4
        self.asset4_checkbox = QCheckBox()
        self.asset4_serial_entry = QLineEdit()
        self.asset4_spinbox = QSpinBox()
        assets_grid.addWidget(self.asset4_checkbox, 3, 0)
        assets_grid.addWidget(self.asset4_serial_entry, 3, 1)
        assets_grid.addWidget(self.asset4_spinbox, 3, 2)
        self.asset4_serial_entry.setPlaceholderText("Asset 4 Serial")

        # Asset 5
        self.asset5_checkbox = QCheckBox()
        self.asset5_serial_entry = QLineEdit()
        self.asset5_spinbox = QSpinBox()
        assets_grid.addWidget(self.asset5_checkbox, 4, 0)
        assets_grid.addWidget(self.asset5_serial_entry, 4, 1)
        assets_grid.addWidget(self.asset5_spinbox, 4, 2)
        self.asset5_serial_entry.setPlaceholderText("Asset 5 Serial")

        # Asset 6
        self.asset6_checkbox = QCheckBox()
        self.asset6_serial_entry = QLineEdit()
        self.asset6_spinbox = QSpinBox()
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
        self.log_window.setReadOnly(True)
        self.log_window.setFixedHeight(100)  # Adjust height as needed
        main_layout.addWidget(self.log_window)

        # Button connections
        self.plus_stage_btn.clicked.connect(self.increase_stage)
        self.minus_stage_btn.clicked.connect(self.decrease_stage)
        self.rehead_btn.clicked.connect(self.rehead_roh)

        self.toggle_all_counters(state=0)  # Disable all counters initially
        self.add_log_entry(message="Counter Dashboard initialized.")

    def toggle_all_counters(self, state):
        enabled = state == 2
        self.roh_spinbox.setEnabled(enabled)
        self.top_rubber_spinbox.setEnabled(enabled)
        self.middle_rubber_spinbox.setEnabled(enabled)
        self.low_rubber_spinbox.setEnabled(enabled)
        self.shot_spinbox.setEnabled(enabled)
        self.total_spinbox.setEnabled(enabled) # Total is editable only if checkbox is checked
        self.asset1_spinbox.setEnabled(enabled)
        self.asset2_spinbox.setEnabled(enabled)
        self.asset3_spinbox.setEnabled(enabled)
        self.asset4_spinbox.setEnabled(enabled)
        self.asset5_spinbox.setEnabled(enabled)
        self.asset6_spinbox.setEnabled(enabled)
        self.asset1_serial_entry.setEnabled(enabled)
        self.asset2_serial_entry.setEnabled(enabled)
        self.asset3_serial_entry.setEnabled(enabled)
        self.asset4_serial_entry.setEnabled(enabled)
        self.asset5_serial_entry.setEnabled(enabled)
        self.asset6_serial_entry.setEnabled(enabled)

        self.update_remain()


    def increase_stage(self):
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

    def decrease_stage(self):
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


    def rehead_roh(self):
        self.roh_spinbox.setValue(0)

    def update_remain(self):
        remain_value = self.total_spinbox.value() - self.shot_spinbox.value()
        self.remain_spinbox.setValue(remain_value)

    def add_log_entry(self, message):
        self.log_window.append(message)
