from PyQt5.QtWidgets import *
from src.linegraph.benchmarkLineGraph import BenchmarkLineGraph
from src.heatmap.benchmarkHeatmap import BenchmarkHeatmap


# Parameters can be configured in the Config Class

class BenchmarkDashboard(QMainWindow):

    def __init__(self, app):
        super(BenchmarkDashboard, self).__init__()
        self.app = app
        self.main_container = QWidget()
        self.main_layout = QGridLayout()
        self.launcher_container = QWidget()
        self.launcher_layout = QHBoxLayout()
        self.line_benchmark_button = QPushButton("Launch Linegraph Dashboard")
        self.heatmap_benchmark_button = QPushButton("Launch Heatmap Dashboard")
        self.home()
        self.line_benchmark = None
        self.heatmap_benchmark = None

    def home(self):
        self.setCentralWidget(self.main_container)
        self.setWindowTitle("PyQtGraph Benchmark Dashboard")
        self.main_container.setLayout(self.main_layout)
        self.launcher_container.setLayout(self.launcher_layout)
        self.main_layout.addWidget(self.launcher_container, 0, 0)
        self.config_ui_content()

    def config_ui_content(self):
        self.line_benchmark_button.resize(self.line_benchmark_button.minimumSizeHint())
        self.launcher_layout.addWidget(self.line_benchmark_button)
        self.heatmap_benchmark_button.resize(self.heatmap_benchmark_button.minimumSizeHint())
        self.launcher_layout.addWidget(self.heatmap_benchmark_button)
        self.wire_buttons()
        self.show()

    def wire_buttons(self):
        self.line_benchmark_button.clicked.connect(self.launch_linegraph_benchmark)
        self.heatmap_benchmark_button.clicked.connect(self.launch_heatmap_benchmark)

    def launch_linegraph_benchmark(self):
        self.reset_main_layout()
        self.line_benchmark = BenchmarkLineGraph(self.app)
        self.main_layout.addWidget(self.line_benchmark.get_self_widget(), 1, 0)

    def launch_heatmap_benchmark(self):
        self.reset_main_layout()
        self.heatmap_benchmark = BenchmarkHeatmap(self.app)
        self.main_layout.addWidget(self.heatmap_benchmark.get_self_widget(), 1, 0)

    def reset_main_layout(self):
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)
        self.hide()
        self.__init__(self.app)
