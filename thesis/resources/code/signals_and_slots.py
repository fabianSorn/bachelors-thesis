import sys
from qtpy import QtWidgets


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.label = QtWidgets.QLabel()
        self.edit = QtWidgets.QLineEdit()
        # Connect Text-Changed-Signal to the Set-Text-Slot
        self.edit.textChanged.connect(self.label.setText)
        self.setup_layout()
        self.show()

    def setup_layout(self):
        """Take the widgets and put them into a layout"""
        central_widget = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
        central_layout.addWidget(self.label)
        central_layout.addWidget(self.edit)
        self.setWindowTitle("Signals and Slots Demo")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    _ = MainWindow()
    sys.exit(app.exec())
