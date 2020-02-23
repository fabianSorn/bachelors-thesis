from collections import namedtuple
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import sys
import numpy as np
import pyqtgraph as pg
from time import time
import signal
from pdb import set_trace
import sys


DATASET_SIZE = 100000
"""Length of the data set used for this application"""

REPEAT_COUNTER = 1000
"""How often should the plot be redrawn"""


class PyQtGraphWindow(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if len(sys.argv) > 1:
            try:
                ds = int(sys.argv[1])
            except:
                ds = DATASET_SIZE
        else:
            ds = DATASET_SIZE

        self._x = np.linspace(0, 10, ds)
        self._y = np.random.normal(size=(50, ds))
        self._counter = 0
        self._times = []

        self._plot = pg.PlotWidget()
        self._curve = self._plot.plot()
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._update)
        self._timer.start(0)

        self.setCentralWidget(self._plot)
        self.setWindowTitle("PyQtGraph Evaluation Application")
        self.resize(800, 600)
        self._plot.setRange(xRange=(0, 10), yRange=(-5, 5))
        self.show()

    def _update(self):
        x = self._x
        y = self._y[self._counter % 50]
        self._curve.setData(x=x, y=y)
        self._counter += 1
        self._times.append(time())
        if self._counter >= REPEAT_COUNTER:
            self._timer.stop()
            self.results()

    def results(self):
        fps = "%0.2f" % self.fps
        self._plot.setTitle(f"Results: {fps} FPS")

    @property
    def fps(self) -> float:
        """The current frames per second from all the recorded data"""
        dts = []
        for i in range(len(self._times) - 2):
            dt = self._times[i + 1] - self._times[i]
            dts.append(dt)
        # np.save(f"eval_app_{DATASET_SIZE}", np.array(dts))
        return 1 / (sum(dts) / len(dts))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtGraphWindow()
    return_value = app.exec()
    print(window.fps)
    sys.exit(return_value)


if __name__ == "__main__":
    main()
