import widgetmark
from typing import List, Tuple
import numpy as np
from qtpy.QtWidgets import QWidget, QGridLayout


class UseCaseHelper:

    """
    The following three use cases would require duplicating
    a lot of code, since they all share a lot of their
    functionality, except parameterization and other details.

    Since Widget-Mark does only pickup and execute classes
    derived from use-case, we can safely define a helper base
    class that implements these common functionalities without
    widgetmark picking it up an trying to executed them
    """

    @staticmethod
    def quick_setup(lib: widgetmark.PlottingLibraryEnum,
                    item_type: widgetmark.DataItemType,
                    item_amount: List[int],
                    ds_length: int,
                    ds_count: int) -> Tuple[List[widgetmark.AbstractBasePlot],
                                            List[widgetmark.AbstractDataItem],
                                            List[np.ndarray]]:
        """
        Function for setting up plots, data items and datasets for filling
        these data items.

        Args:
            lib: Library to use for initializing the plot widgets
            item_type: type of items that should be added to the plots
            item_amount: array with data item counts for each of the produced
                         plots
            ds_length: How long should the datasets for each curve be
            ds_count: How many different datasets per curve

        Returns:
            Plots, curves, data-sets for these curves
        """
        plots = []
        curves = []
        data = []
        for pc in item_amount:
            plot = widgetmark.AbstractBasePlot.using(lib)
            plot.set_range(((0, 10), (0, pc)))
            plots.append(plot)
            for i, _ic in enumerate(range(pc)):
                bounds = [0, 10, i, i + 1]
                d = UseCaseHelper._prepare_data(ds_count,
                                                ds_length,
                                                *bounds)
                data.append(d)
                curves.append(plot.add_item(item_type=item_type))
        return plots, curves, data

    @staticmethod
    def _prepare_data(ds_count, ds_amount, xmin=0, xmax=10, ymin=0, ymax=1):
        """
        This function is not part of the interface, but we use it in the
        setup_widget phase to calculate some data we can display later.
        """
        result: List[np.ndarray] = []
        for _ in range(ds_count):
            x = np.linspace(xmin, xmax, ds_amount)
            y = np.random.uniform(ymin, ymax, ds_amount)
            result.append(np.array([x, y]))
        return result


class HtUseCase(UseCaseHelper, widgetmark.UseCase):

    """
    Use case for the BE-CO-HT's distributed oscilloscope
    gui application.
    """

    backend = widgetmark.GuiBackend.QT
    goal = 50.0
    minimum = 25.0
    tolerance = 0.05
    repeat = 1000
    timeout = 100
    # These will be available during runtime as instance attributes
    parameters = {"plot_lib": list(widgetmark.PlottingLibraryEnum),
                  "data_count": [1000, 10000, 100000],
                  "curve_count": [1, 4, 8]}

    def setup_widget(self):
        """Setup widgets for the """
        self._ds_count = 5
        self._plots, self._curves, self._data = self.quick_setup(
            lib=self.plot_lib,
            item_type=widgetmark.DataItemType.CURVE,
            item_amount=[self.curve_count],
            ds_length=self.data_count,
            ds_count=self._ds_count,
        )
        return self._plots[0]

    def operate(self):
        for ci, c in enumerate(self._curves):
            di = self.runtime_context.current_run % self._ds_count
            c.set_data(self._data[ci][di])


class LhcUseCase(UseCaseHelper, widgetmark.UseCase):

    """
    Use case for the BE-OP-LHC's gui application showing
    bunches of LHC settings.
    """

    backend = widgetmark.GuiBackend.QT
    goal = 50.0
    minimum = 1.0
    tolerance = 0.05
    repeat = 1000
    timeout = 100
    # These will be available during runtime as instance attributes
    parameters = {"plot_lib": list(widgetmark.PlottingLibraryEnum),
                  "data_count": [360, 720, 3600, 7200],
                  "curve_count": [300, 3000]}

    def setup_widget(self):
        """Setup widgets for the """
        self._ds_count = 5
        self._plots, self._curves, self._data = self.quick_setup(
            lib=self.plot_lib,
            item_type=widgetmark.DataItemType.CURVE,
            item_amount=[self.curve_count],
            ds_length=self.data_count,
            ds_count=self._ds_count,
        )
        return self._plots[0]

    def operate(self):
        for ci, c in enumerate(self._curves):
            di = self.runtime_context.current_run % self._ds_count
            c.set_data(self._data[ci][di])


class ApsUseCase(UseCaseHelper, widgetmark.UseCase):

    """
    Use case for the BE-CO-APS's gui application showing
    Linac4 Settings.
    """

    backend = widgetmark.GuiBackend.QT
    goal = 50.0
    minimum = 30.0
    tolerance = 0.05
    repeat = 1000
    timeout = 100
    # These will be available during runtime as instance attributes
    parameters = {"plot_lib": list(widgetmark.PlottingLibraryEnum),
                  "data_count": [3600 / 1.2],
                  "curve_count": [3],
                  "plot_count": [(1, 1), (4, 2)]}

    def setup_widget(self):
        """Wrap multiple plots inside a QWidget"""
        self._ds_count = 5
        self._plots, self._curves, self._data = self.quick_setup(
            lib=self.plot_lib,
            item_type=widgetmark.DataItemType.SCATTER,
            item_amount=[self.curve_count for _ in range(self.plot_count[0])],
            ds_length=self.data_count,
            ds_count=self._ds_count,
        )
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)
        for index, plot in enumerate(self._plots):
            row = int(index / self.plot_count[1])
            column = index % self.plot_count[1]
            layout.addWidget(plot, row, column)
        return widget

    def operate(self):
        for ci, c in enumerate(self._curves):
            di = self.runtime_context.current_run % self._ds_count
            c.set_data(self._data[ci][di])
