from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from pyqtgraph.ptime import time
from src.fpsCounter.FPSCounter import FPSCounter
from src.linegraph.benchmarkLineGraphConfig import *
from src.linegraph.benchmarkResultWriter import BenchmarkResultWriter
import pyqtgraph as pg
import numpy as np

# Parameters can be configured in the Config Class

class BenchmarkLineGraph(QWidget):

    def __init__(self, app):
        super(BenchmarkLineGraph, self).__init__()
        self.app = app
        self.writer = BenchmarkResultWriter(LineGraphConfig.result_file_name)
        self.fps_collection = []
        self.dataset_size = 1000 * LineGraphConfig.min_dataset_size_in_K
        self.curve = []
        self.benchmarkTuples = []
        self.benchmarkTupleCounter = -1
        self.data = np.random.normal(size=(LineGraphConfig.max_line_count, self.dataset_size))
        self.one_line_data = None
        self.lastTime = time()
        self.fps = None
        self.linenumber = 1
        self.visible_redraw_toggle = False
        self.timer = QTimer()
        self.now = time()
        self.fps_counter = FPSCounter(app)
        self.visible_redraw: bool = False
        self.auto_downsample: bool = True
        self.clip_to_view: bool = True
        self.one_line_hack: bool = False
        self.downsample_modes = ["peak", "mean", "subsample"]
        self.downsample_mode: str = self.downsample_modes[0]
        # UI Widgets Definition
        self.main_container = QWidget()
        self.main_layout = QGridLayout()
        self.spinner_dataset_size = QSpinBox()
        self.spinner_linenumber = QSpinBox()
        self.visible_redraw_checkbox = QCheckBox("Visible Redraw")
        self.auto_downsample_checkbox = QCheckBox("Auto Downsample")
        self.clip_to_view_checkbox = QCheckBox("Clip to View")
        self.downsample_mode_combobox = QComboBox()
        self.one_line_hack_checkbox = QCheckBox("Draw Sets as One Line")
        self.current_fps = QLabel('Current FPS:')
        self.benchmarkStartButton = QPushButton("Start Benchmark")
        self.table = QTableWidget()
        self.plot = pg.PlotWidget()
        self.home()

    def get_self_widget(self):
        return self.main_container

    def home(self):
        self.init_instance_variables()
        self.main_container.setLayout(self.main_layout)
        self.create_input_ui_for_graph_params(self.main_layout, 0, 0)
        self.create_linegraph_ui(self.main_layout, 2, 0)
        self.create_button_ui_for_benchmark_start(self.main_layout, 3, 0)
        self.setFixedWidth(LineGraphConfig.graph_size_width + 20)

    def init_instance_variables(self):
        self.linenumber = 1
        self.dataset_size = 1000 * LineGraphConfig.min_dataset_size_in_K
        self.curve = []
        self.benchmarkTuples = []
        self.benchmarkTupleCounter = -1
        for dataset_size in LineGraphConfig.benchmark_dataset_sizes:
            for line_count in LineGraphConfig.benchmark_linecounts:
                self.benchmarkTuples.append([dataset_size * 1000, line_count])

    # ~~~~~~~~~~~~~~~~~~~~~~~ Add Dashboard Components ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def create_input_ui_for_graph_params(self, parent_widget, x, y):
        input_container = QWidget()
        config_container = QWidget()
        input_layout = QHBoxLayout()
        config_layout = QHBoxLayout()
        input_container.setLayout(input_layout)
        config_container.setLayout(config_layout)
        self.spinner_dataset_size.setMaximum(LineGraphConfig.max_dataset_size_in_K)
        self.spinner_dataset_size.setMinimum(1)
        self.spinner_dataset_size.resize(self.spinner_dataset_size.minimumSizeHint())
        self.spinner_dataset_size.valueChanged.connect(self.__util_dataset_size_input_handle_change)
        self.spinner_linenumber.setMaximum(LineGraphConfig.max_line_count)
        self.spinner_linenumber.setMinimum(LineGraphConfig.min_line_count)
        self.spinner_linenumber.resize(self.spinner_linenumber.minimumSizeHint())
        self.spinner_linenumber.valueChanged.connect(self.__util_dataset_count_input_handle_change)
        spinner_dataset_size_label = QLabel('k Points to Display')
        spinner_linenumber_label = QLabel('Datasets to Display')
        downsample_combobox_label = QLabel('Downsample Method')
        self.downsample_mode_combobox.addItems(self.downsample_modes)
        self.downsample_mode_combobox.setCurrentIndex(0)
        self.downsample_mode_combobox.currentIndexChanged.connect(self.__update_plot_downsample_settings)
        input_layout.addWidget(self.current_fps)
        input_layout.addWidget(self.spinner_dataset_size)
        input_layout.addWidget(spinner_dataset_size_label)
        input_layout.addWidget(self.spinner_linenumber)
        input_layout.addWidget(spinner_linenumber_label)
        config_layout.addWidget(self.visible_redraw_checkbox)
        config_layout.addWidget(self.auto_downsample_checkbox)
        config_layout.addWidget(self.clip_to_view_checkbox)
        config_layout.addWidget(self.one_line_hack_checkbox)
        config_layout.addWidget(self.downsample_mode_combobox)
        config_layout.addWidget(downsample_combobox_label)
        self.visible_redraw_checkbox.setChecked(self.visible_redraw)
        self.visible_redraw_checkbox.toggled.connect(lambda: self.__change_visible_redraw())
        self.one_line_hack_checkbox.setChecked(self.one_line_hack)
        self.one_line_hack_checkbox.toggled.connect(lambda: self.__change_one_line_hack_usage())
        self.auto_downsample_checkbox.setChecked(True)
        self.auto_downsample_checkbox.toggled.connect(lambda: self.plot.setDownsampling(
            auto=self.auto_downsample_checkbox.isChecked()))
        self.__update_plot_downsample_settings()
        self.plot.setClipToView(True)
        self.clip_to_view_checkbox.setChecked(True)
        self.clip_to_view_checkbox.toggled.connect(lambda: self.plot.setClipToView(
            self.clip_to_view_checkbox.isChecked()
        ))

        parent_widget.addWidget(input_container, x, y)
        parent_widget.addWidget(config_container, x+1, y)

    def create_button_ui_for_benchmark_start(self, parent_widget, x, y):
        self.benchmarkStartButton.clicked.connect(self.start_benchmark)
        parent_widget.addWidget(self.benchmarkStartButton, x, y)

    def create_table_ui_for_benchmark_results(self, parent_widget, x, y):
        self.table.setRowCount(len(LineGraphConfig.benchmark_linecounts) * len(LineGraphConfig.benchmark_dataset_sizes))
        self.table.setColumnCount(len(LineGraphConfig.table_headers))
        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(LineGraphConfig.table_headers)
        parent_widget.addWidget(self.table, x, y)

    def create_linegraph_ui(self, parent_widget, x, y):
        self.plot.setFixedSize(LineGraphConfig.graph_size_width, LineGraphConfig.graph_size_height)
        self.plot.showGrid(x=True, y=True)
        self.create_new_curves_and_start_timer()
        parent_widget.addWidget(self.plot, x, y)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Benchmarking ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def start_benchmark(self):
        self.benchmarkTupleCounter = -1
        self.spinner_dataset_size.setEnabled(False)
        self.spinner_linenumber.setEnabled(False)
        self.create_table_ui_for_benchmark_results(self.main_layout, 4, 0)
        self.writer.write_linegraph_benchmark_result_header()
        self.benchmarkStartButton.deleteLater()
        self.trigger_redraw_for_benchmark()

    def cleanup_after_benchmark(self):
        self.linenumber = LineGraphConfig.min_line_count
        self.dataset_size = LineGraphConfig.min_dataset_size_in_K * 1000
        self.fps_collection = []
        self.spinner_dataset_size.setEnabled(True)
        self.spinner_dataset_size.setValue(self.dataset_size / 1000)
        self.spinner_linenumber.setEnabled(True)
        self.spinner_linenumber.setValue(self.linenumber)
        self.update_curves_in_plot_widget()
        self.writer.write_result_end()

    def trigger_redraw_for_benchmark(self):
        if self.incr_dataset_size_and_linecount_for_benchmark():
            self.update_curves_in_plot_widget(self.__util_calc_benchmark_redraw_counter())
        else:
            self.cleanup_after_benchmark()

    def update_curves_in_plot_widget(self, benchmark_max_redraw: int = None):
        self.plot.clear()
        self.curve.clear()
        self.create_new_curves_and_start_timer(benchmark_max_redraw)

    def incr_dataset_size_and_linecount_for_benchmark(self):
        if self.benchmarkTupleCounter < (len(self.benchmarkTuples) - 1):
            self.benchmarkTupleCounter += 1
            self.dataset_size = self.benchmarkTuples[self.benchmarkTupleCounter][0]
            self.linenumber = self.benchmarkTuples[self.benchmarkTupleCounter][1]
            self.spinner_dataset_size.setValue(self.dataset_size / 1000)
            self.spinner_linenumber.setValue(self.linenumber)
            return True
        else:
            return False

    # ~~~~~~~~~~~~~~ Timer and FPS Counting ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def create_new_curves_and_start_timer(self, benchmark_max_redraw: int = None):
        if self.one_line_hack:
            self.draw_datasets_with_one_line_hack()
        else:
            self.draw_datasets_seperatly(benchmark_max_redraw)


    def draw_datasets_seperatly(self, benchmark_max_redraw: int = None):
        for i in range(0, self.linenumber):
            self.curve.append(self.plot.plot(pen=(i, self.linenumber)))
        self.data = np.random.normal(size=(self.linenumber * 2, self.dataset_size))
        self.fps_counter.start_fps_counter_for(
            self.redraw_function, self.fps_update_function, self.timer_stop_function, benchmark_max_redraw)


    # https://groups.google.com/forum/#!topic/pyqtgraph/kz4U6dswEKg
    # Combine multiple datasets in advance to one with disconnected lines in between
    # Improves performance with thousands of seperate datasets
    def draw_datasets_with_one_line_hack(self):
        x = np.empty((self.linenumber, self.dataset_size))
        x[:] = np.arange(self.dataset_size)
        y = np.random.normal(size=(self.linenumber, self.dataset_size))
        connect = np.ones((self.linenumber, self.dataset_size), dtype=np.ubyte)
        connect[:, -1] = 0  # disconnect segment between lines
        path = pg.arrayToQPath(x.reshape(self.linenumber * self.dataset_size),
                               y.reshape(self.linenumber * self.dataset_size),
                               connect.reshape(self.linenumber * self.dataset_size))
        self.one_line_data = pg.QtGui.QGraphicsPathItem(path)
        self.one_line_data.setPen(pg.mkPen('w'))

    def redraw_function(self):
        if self.one_line_hack:
            self.redraw_with_one_line_hack()
        else:
            self.redraw_without_one_line_hack()

    def redraw_without_one_line_hack(self):
        for i in range(0, self.linenumber):
            data_index: int = i
            # Toggle between two different datasets when redraw is supposed to visible
            data_index += self.linenumber if self.visible_redraw_toggle and self.visible_redraw else 0
            data = self.data[data_index % (self.linenumber * 2)]
            self.curve[i].setData(data)
        self.visible_redraw_toggle = not self.visible_redraw_toggle

    def redraw_with_one_line_hack(self):
        self.plot.addItem(self.one_line_data)

    def fps_update_function(self, current_fps, fps_collection):
        self.current_fps.setText('%0.2f fps' % current_fps)
        self.fps_collection = fps_collection

    def timer_stop_function(self):
        self.persist_results()
        self.trigger_redraw_for_benchmark()

    def persist_results(self):
        # Cut first to values generated between changes of graph
        self.fps_collection = self.fps_collection[2:]
        average_fps = sum(self.fps_collection) / len(self.fps_collection)
        self.write_benchmark_result_to_table(
            self.dataset_size, self.linenumber, self.benchmarkTupleCounter, type(self.plot).__name__, average_fps)
        self.writer.append_line(type(self.plot).__name__ + "(" + str(self.linenumber) + "x" + str(self.dataset_size)
                                + "): " + ("%.2f" % average_fps) + " FPS")

    def write_benchmark_result_to_table(self, data_size, line_count, table_row_index, graph_type, average_fps):
        self.table.setItem(table_row_index, 0, QTableWidgetItem(str(data_size)))
        self.table.setItem(table_row_index, 1, QTableWidgetItem(str(line_count)))
        self.table.setItem(table_row_index, 2, QTableWidgetItem(graph_type))
        self.table.setItem(table_row_index, 3, QTableWidgetItem("%.2f" % average_fps))

    # ~~~~~~~~~~~~~~ Utils ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __util_calc_benchmark_redraw_counter(self):
        percentage = (self.dataset_size / (
                LineGraphConfig.max_dataset_size_in_K * 1000 - LineGraphConfig.min_dataset_size_in_K * 1000))
        redraw_range = (LineGraphConfig.max_number_of_redraws - LineGraphConfig.min_number_of_redraws)
        recommended_redraw = LineGraphConfig.max_number_of_redraws - percentage * redraw_range
        return int(recommended_redraw)

    def __util_dataset_size_input_handle_change(self):
        self.dataset_size = self.spinner_dataset_size.value() * 1000
        self.update_curves_in_plot_widget()

    def __util_dataset_count_input_handle_change(self):
        self.linenumber = self.spinner_linenumber.value()
        self.update_curves_in_plot_widget()

    def __change_visible_redraw(self):
        self.visible_redraw = self.visible_redraw_checkbox.isChecked()

    def __change_one_line_hack_usage(self):
        self.one_line_hack = self.one_line_hack_checkbox.isChecked()
        self.update_curves_in_plot_widget()

    def __update_plot_downsample_settings(self):
        auto = self.auto_downsample_checkbox.isChecked()
        mode = self.downsample_modes[self.downsample_mode_combobox.currentIndex()]
        self.plot.setDownsampling(auto=auto, mode=mode)
