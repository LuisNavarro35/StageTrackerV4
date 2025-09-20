# gui/counter_dashboard.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QCheckBox, QPushButton
)

class CounterDashboardWindow(QMainWindow):
    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id
        self.job_name = "JOB NAME"  # Placeholder, should be fetched from DB
        self.crew_cell = "CREW CELL"  # Placeholder, should be fetched from

        self.setWindowTitle("Counter Dashboard")
        self.setFixedSize(1000, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Row0: Stage Tracker / job / crew
        info_label = QLabel(f"Stage Tracker | Job: {self.job_name} | Crew: {self.crew_cell}")
        main_layout.addWidget(info_label)

        # Row2: ROH counter controls
        row_layout = QHBoxLayout()
        self.roh_label = QLabel("ROH:")
        row_layout.addWidget(self.roh_label)

        self.roh_spin = QSpinBox()
        self.roh_spin.setRange(0, 9999)
        row_layout.addWidget(self.roh_spin)

        self.roh_checkbox = QCheckBox("Enable ROH Stage")
        row_layout.addWidget(self.roh_checkbox)

        main_layout.addLayout(row_layout)

        # Row3: Control buttons
        btn_layout = QHBoxLayout()
        self.plus_stage_btn = QPushButton("+Stage")
        self.minus_stage_btn = QPushButton("-Stage")
        self.rehead_btn = QPushButton("Rehead")
        btn_layout.addWidget(self.plus_stage_btn)
        btn_layout.addWidget(self.minus_stage_btn)
        btn_layout.addWidget(self.rehead_btn)
        main_layout.addLayout(btn_layout)

        # Connect buttons
        self.plus_stage_btn.clicked.connect(self.increase_roh)
        self.minus_stage_btn.clicked.connect(self.decrease_roh)
        self.rehead_btn.clicked.connect(self.rehead_roh)

    def increase_roh(self):
        if self.roh_checkbox.isChecked():
            self.roh_spin.setValue(self.roh_spin.value() + 1)

    def decrease_roh(self):
        if self.roh_checkbox.isChecked() and self.roh_spin.value() > 0:
            self.roh_spin.setValue(self.roh_spin.value() - 1)

    def rehead_roh(self):
        self.roh_spin.setValue(0)
