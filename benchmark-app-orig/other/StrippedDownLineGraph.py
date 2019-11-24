import pyqtgraph as pg
import numpy as np
import sys
from PyQt5.QtWidgets import *

# Stripped down example to compare if the FPS counting has any negative effects on
# Performance of PyQtGraph.

class StrippedDownLineGraph(QMainWindow):

    def __init__(self, app):
        super(StrippedDownLineGraph, self).__init__()
        self.app = app
        self.ds_size = 100000
        self.ds_count = 8
        self.home()
        self.show()

    def home(self):
        main_container = QWidget()
        self.setCentralWidget(main_container)
        main_layout = QGridLayout()
        main_container.setLayout(main_layout)
        plot = pg.PlotWidget()
        plot.setFixedSize(800, 600)
        plot.showGrid(x=True, y=True)
        plot.setDownsampling(auto=True, mode="peak")
        plot.setClipToView(True)
        main_layout.addWidget(plot)
        datasets = np.random.normal(size=(self.ds_count, self.ds_size))
        for i in range(0, self.ds_count):
            plot.plot(pen=(i, self.ds_count)).setData(datasets[i])


def run():
    app = QApplication(sys.argv)
    gui = StrippedDownLineGraph(app)
    sys.exit(app.exec_())

run()
