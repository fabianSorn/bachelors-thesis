import widgetmark
import numpy as np
import pyqtgraph as pg


class Eval(widgetmark.UseCase):

    backend = widgetmark.GuiBackend.QT
    goal = 30.0
    minimum = 20.0
    tolerance = 0.05
    repeat = 1000
    timeout = 100
    parameters = {
        "size": [1000, 10000, 50000, 100000],
    }

    def setup_widget(self):
        pg = widgetmark.PlottingLibraryEnum.PYQTGRAPH
        curve = widgetmark.DataItemType.CURVE
        self._plot = widgetmark.AbstractBasePlot.using(pg)
        self._curve = self._plot.add_item(curve)
        self._x = np.linspace(0, 10, self.size)
        self._y = np.random.normal(size=(50, self.size))
        self._plot.set_range(((0, 10), (-5, 5)))
        return self._plot

    def operate(self):
        y = self._y[self.runtime_context.current_run % 50]
        self._curve.set_data([self._x, y])
