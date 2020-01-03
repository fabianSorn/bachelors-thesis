import sys
import numpy as np
from qtpy import QtWidgets
import pyqtgraph

class PyQtGraphWindow(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Data
        x = np.array(range(100)) * 0.2
        y = np.sin(x)
        # Plot
        self._plot = pyqtgraph.PlotWidget()
        # Data Visualization
        curve = pyqtgraph.PlotDataItem(x=x, y=y)
        scatter = pyqtgraph.PlotDataItem(x=x, y=y + 2, pen=None, symbol="o")
        bars = pyqtgraph.BarGraphItem(x=x, height=y + 1, y0=-3, width = 0.15)
        self._plot.addItem(curve)
        self._plot.addItem(scatter)
        self._plot.addItem(bars)
        # Setup window content
        self.setCentralWidget(self._plot)
        self.setWindowTitle("PyQtGraph Demo")
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    _ = PyQtGraphWindow()
    sys.exit(app.exec())