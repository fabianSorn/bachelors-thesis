import time

from qtpy.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
)
from qtpy.QtCore import Signal

from src.benchmark import BenchmarkWindow, BenchmarkResults


class LabelBenchmark(BenchmarkWindow):

    """ This is a basic Benchmarking class """

    sig_completed = Signal([BenchmarkResults])

    def __init__(self, app: QApplication, max_repeat: int = 240):
        BenchmarkWindow.__init__(
            self,
            app=app,
            max_repeat=max_repeat,
        )
        self._results = None
        self.main_container = QWidget()
        self.main_layout = QGridLayout()
        self.label = QLabel()
        self._init_ui()
        self._counter = 0

    def _init_ui(self):
        self.setCentralWidget(self.main_container)
        self.main_container.setLayout(self.main_layout)
        self.main_layout.addWidget(self.label)
        self.setWindowTitle("Simple Label Benchmark Window")

    def init_operation(self):
        self.label.setText(str(self._counter))
        self._counter += 1
