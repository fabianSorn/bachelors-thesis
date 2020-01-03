import sys
from qtpy import QtWidgets

import numpy as np
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

class MatplotlibWindow(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Data
        x = np.array(range(100)) * 0.2
        y = np.sin(x)
        # Plot + Navigation Bar
        self._canvas = FigureCanvas(Figure())
        self._plot = self._canvas.figure.subplots()
        self._toolbar = NavigationToolbar(canvas=self._canvas, parent=self)
        # Data Visualization
        curve = self._plot.plot(x, y, "-")
        scatter = self._plot.plot(x, y + 2, "o")
        bars = self._plot.bar(x=x, height=y + 1, bottom=-3, width=0.15)
        # Setup Window Content
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._toolbar)
        layout.addWidget(self._canvas)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Matplotlib Demo")
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    _ = MatplotlibWindow()
    sys.exit(app.exec())