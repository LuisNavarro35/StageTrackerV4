from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QSpinBox, QCheckBox, QPushButton
)
import sys

class CounterDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stage Tracker Counter")

        layout = QVBoxLayout()

        # SpinBox
        self.spinbox = QSpinBox()
        self.spinbox.setRange(0, 100)
        self.spinbox.setValue(10)

        # Style: black when enabled, green when disabled
        self.spinbox.setStyleSheet("""
            QSpinBox {
                color: black;
                font-weight: bold;
            }
            QSpinBox:disabled {
                color: green;
                font-weight: bold;
            }
        """)

        layout.addWidget(QLabel("Counter:"))
        layout.addWidget(self.spinbox)

        # Checkbox to lock/unlock manual editing
        self.checkbox = QCheckBox("Enable manual editing")
        self.checkbox.setChecked(False)
        self.checkbox.stateChanged.connect(self.toggle_edit)
        layout.addWidget(self.checkbox)

        # External buttons (still work when spinbox is locked)
        btn_inc = QPushButton("+1")
        btn_dec = QPushButton("-1")
        btn_inc.clicked.connect(lambda: self.spinbox.setValue(self.spinbox.value() + 1))
        btn_dec.clicked.connect(lambda: self.spinbox.setValue(self.spinbox.value() - 1))
        layout.addWidget(btn_inc)
        layout.addWidget(btn_dec)

        self.setLayout(layout)

        # Start locked (disabled → green)
        self.spinbox.setEnabled(False)

    def toggle_edit(self):
        if self.checkbox.isChecked():
            self.spinbox.setEnabled(True)    # black text
        else:
            self.spinbox.setEnabled(False)   # green text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CounterDemo()
    window.show()
    sys.exit(app.exec())
