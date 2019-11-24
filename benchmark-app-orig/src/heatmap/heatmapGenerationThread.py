from PyQt5.QtCore import QThread, pyqtSignal
from src.heatmap.benchmarkHeatmapConfig import HeatmapConfig as Config
import numpy as np
from numpy import ndarray
import pickle


class HeatmapGenerationThread(QThread):

    image_generation_completed = pyqtSignal(ndarray, name="image_data_created")

    # Images are only cached by resolution -> Image from same resolution can be loaded from cache, if not wanted
    # set force_recalc on True
    def __init__(self, image_width=1000, image_height=1000, heat_center_x=500, heat_center_y=500, heat_center_radius=50, force_recalc=False):
        self.image_width = image_width
        self.image_height = image_height
        self.heat_center_x = heat_center_x
        self.heat_center_y = heat_center_y
        self.heat_center_radius = heat_center_radius
        self.force_recalc = force_recalc
        self.image_file_full_name = Config.image_file_base_name
        self.image_file_full_name += "_" + str(self.image_width) + "x" + str(self.image_height)
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        # get Parameters from Benchmark Configuration
        self.generate_heatmap_image()

    # Simulates Heatmap Image around a center
    def generate_heatmap_image(self):
        if self.force_recalc:
            data = self.create_and_write_image()
        else:
            try:
                data = self.readImageFromFile()
            except IOError:
                data = self.create_and_write_image()
        self.image_generation_completed.emit(np.array(data))
        self.sleep(2)

    def readImageFromFile(self):
        with open(self.image_file_full_name, 'rb') as file:
            image_data = pickle.load(file)
        return image_data

    def create_and_write_image(self):
        # Create image as 3D List
        data = [[[HeatmapGenerationThread.calc_heatmap_pixel_color(c, r, cc, self.heat_center_x, self.heat_center_y, self.heat_center_radius) for cc in range(0, 3)] for r in range(0, self.image_height)] for c in range(0, self.image_width)]
        with open(self.image_file_full_name, 'wb') as file:
            pickle.dump(data, file)
        return data

    @staticmethod
    def calc_heatmap_pixel_color(column, row, channel, center_x, center_y, radius):
        distance_from_center = HeatmapGenerationThread.distance(column, row, center_x, center_y)
        distance_perc = (distance_from_center / radius)
        if distance_perc > 1:
            distance_perc = 1
        color = 85 * channel - ((85 * channel) * distance_perc)
        if color > 255:
            color = 255
        elif color < 80 and channel == 0:
            color = 80
        elif color < 0 and channel != 0:
            color = 30
        # random variation in color
        return color + np.random.uniform(-30, 30)

    @staticmethod
    def distance(x1, y1, x2, y2):
        return np.sqrt((abs(x2 - x1) ** 2) + (abs(y2 - y1) ** 2))