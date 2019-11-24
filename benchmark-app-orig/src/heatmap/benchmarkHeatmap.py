from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from pyqtgraph.ptime import time
from src.fpsCounter.FPSCounter import FPSCounter
from src.heatmap.benchmarkHeatmapConfig import HeatmapConfig
from src.heatmap.heatmapGenerationThread import HeatmapGenerationThread
import pyqtgraph as pg
import numpy as np


# Parameters can be configured in the Config Class

class BenchmarkHeatmap(QWidget):

    def __init__(self, app):
        super(BenchmarkHeatmap, self).__init__()
        self.app = app
        # self.writer = BenchmarkResultWriter(HeatmapConfig.result_file_name)
        self.main_container = QWidget()
        self.main_layout = QGridLayout()
        self.graphics_layout_widget = pg.GraphicsLayoutWidget()
        self.timer = QTimer()
        self.fps_counter = FPSCounter(app)
        self.current_fps = QLabel('Current FPS:')
        # Image related
        self.plot = self.graphics_layout_widget.addPlot()
        self.image_item = pg.ImageItem()
        self.generate_heatmap_image()
        self.data_generation_thread = None
        self.data = None
        self.fps_collection = []
        self.home()

    def get_self_widget(self):
        return self.main_container

    def home(self):
        self.main_container.setLayout(self.main_layout)
        self.main_layout.addWidget(self.graphics_layout_widget)
        graph_width = HeatmapConfig.x_range
        graph_height = HeatmapConfig.y_range
        self.main_layout.addWidget(self.current_fps)
        self.graphics_layout_widget.setFixedSize(800, 800)

    def generate_heatmap_image(self):
        # call image creation in seperate thread
        self.data_generation_thread = HeatmapGenerationThread(
            HeatmapConfig.x_range, HeatmapConfig.y_range, HeatmapConfig.heat_center_x, HeatmapConfig.heat_center_y,
            HeatmapConfig.heat_area_radius, HeatmapConfig.force_rerendering)
        self.data_generation_thread.image_generation_completed.connect(self.imageGenerationDone)
        self.data_generation_thread.start()

    def imageGenerationDone(self, image_data):
        self.data = image_data
        self.fps_counter.start_fps_counter_for(
            self.redraw_function, self.fps_update_function, self.timer_stop_function, None)

    def redraw_function(self):
        self.plot.addItem(self.image_item)
        self.image_item.setImage(self.data)
        self.app.processEvents()

    def fps_update_function(self, current_fps: int, fps_collection):
        self.main_container.setWindowTitle(str(current_fps))
        self.current_fps.setText('%0.2f fps' % current_fps)
        self.fps_collection = fps_collection

    def timer_stop_function(self):
        print("Redraw stopped.")
