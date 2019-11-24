import time

import numpy as np
import pyqtgraph as pg
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
)
from qtpy.QtCore import Signal, Slot, QTimer
from qtpy.QtGui import QShowEvent

from src.benchmark import BenchmarkWindow, BenchmarkResults


class TemplateBenchmark(BenchmarkWindow):

    """ This is a basic Benchmarking class """

    sig_completed = Signal([BenchmarkResults])

    def __init__(self, app: QApplication, max_repeat: int = 100):
        BenchmarkWindow.__init__(
            self,
            app=app,
            max_repeat=max_repeat,
        )
        self._results = None
        self.main_container = QWidget()
        self.main_layout = QGridLayout()
        self.plot = pg.PlotWidget()
        self.redraw_counter = 0
        self._init_ui()
        # This we have to clean up a bit
        self.item = pg.ScatterPlotItem()
        self.plot.addItem(self.item)
        self.ptr = 0
        self.lastTime = time.time()
        self.fps = None

    def _init_ui(self):
        self.setCentralWidget(self.main_container)
        self.main_container.setLayout(self.main_layout)
        self.main_layout.addWidget(self.plot)
        self.setWindowTitle("Template Benchmark Window")

    def init_operation(self):
        self.item.setData(
            x=[0, 1, 2],
            y=[1, 2, 3]
        )

    def process_operation(self):
        pass


# This constant defines, which class is the benchmark main window
BENCHMARK_CLASS = TemplateBenchmark