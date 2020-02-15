import sys
import time
from qtpy import QtWidgets, QtCore, QtGui


class WatchLabel(QtWidgets.QLabel):

    def __init__(self):
        QtWidgets.QLabel.__init__(self)
        font = QtGui.QFont("Courier")
        font.setWeight(QtGui.QFont.ExtraBold)
        self.setFont(font)

    @QtCore.Slot(float)
    def set_time(self, timestamp: float):
        """Takes timestamp and displays it in a readable format."""
        self.setText(str(time.ctime(timestamp)))


class WatchTick(QtCore.QObject):

    sig_time = QtCore.Signal(float)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.emit_time)

    def emit_time(self):
        self.sig_time.emit(time.time())

    def start(self):
        self.timer.start(1000/60)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.label = QtWidgets.QLabel()
        self.edit = QtWidgets.QLineEdit()
        self.watch_tick = WatchTick()
        self.watch = WatchLabel()
        # Update the watch label as soon as the ticker sends an update.
        self.watch_tick.sig_time.connect(self.watch.set_time)
        self.watch_tick.start()
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
        central_layout.addWidget(self.watch)
        central_layout.addWidget(self.label)
        central_layout.addWidget(self.edit)
        self.setWindowTitle("Signals and Slots Demo")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    _ = MainWindow()
    sys.exit(app.exec())
