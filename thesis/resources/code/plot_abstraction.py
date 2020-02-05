import sys
from qtpy import QtWidgets
from math import pi

import numpy as np
from widgetmark import AbstractBasePlot, PlottingLibraryEnum, DataItemType


class Window(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        """
        Changing the library passed to the factory method of AbtractBasePlot
        allows switching between the libraries used in for the visualization.
        """
        super().__init__(*args, **kwargs)
        # self.plot = AbstractBasePlot.using(PlottingLibraryEnum.PYQTGRAPH)
        self.plot = AbstractBasePlot.using(PlottingLibraryEnum.MATPLOTLIB)
        # Add Scatter Plot Data Item to the plot.
        item = self.plot.add_item(DataItemType.SCATTER)
        # Set Data of the Scatter Plot
        x = np.linspace(0, 2 * pi, 20)
        y = np.sin(x)
        item.set_data([x, y])
        # Set visible view range
        x_range = [0, 2 * pi]
        y_range = [-1, 1]
        self.plot.set_range([x_range, y_range])
        # Add plot to the window
        self.setCentralWidget(self.plot)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

