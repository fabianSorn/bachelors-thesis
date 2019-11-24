from PyQt5.QtCore import QTimer
from pyqtgraph.ptime import time
import numpy as np


class FPSCounter:

    def __init__(self, app):
        self.lastTime = time()
        self.fps: int = None
        self.fps_collection: list[int] = []
        self.redrawCounter: int = 0
        self.timer: QTimer = QTimer()
        self.maximum_redraw_count: int = None
        self.app = app

    def start_fps_counter_for(
            self, redraw: classmethod, fps_update: classmethod,
            timer_top: classmethod, maximum_redraw_count: int):
        self.lastTime = time()
        self.fps = 0
        self.fps_collection = []
        self.redrawCounter = 0
        self.timer = QTimer()
        self.maximum_redraw_count = maximum_redraw_count
        self.timer.timeout.connect(lambda: self.__util_update_fps_and_redraw(
            redraw, fps_update, timer_top))
        self.timer.start(0)


# FPS capture from pyqtgraph.examples
    def __util_update_fps_and_redraw(
            self, redraw_function: classmethod, fps_update_function: classmethod, timer_stop_function: classmethod):
        # Passed function for redrawing image
        redraw_function()
        # Record time in needs to redraw all n datasets
        self.now = time()
        dt = self.now - self.lastTime
        self.lastTime = self.now
        if self.fps is None:
            self.fps = 1.0/dt
            self.fps_collection.append(self.fps)
        else:
            s = np.clip(dt*3., 0, 1)
            self.fps = self.fps * (1-s) + (1.0/dt) * s
            fps_update_function(self.fps, self.fps_collection)
        if self.redrawCounter == 0:
            self.fps_collection = []
        if self.maximum_redraw_count is not None:
            if self.redrawCounter <= self.maximum_redraw_count:
                self.redrawCounter += 1
                self.fps_collection.append(self.fps)
                if len(self.fps_collection) >= 1000:
                    self.fps_collection = self.fps_collection[500:]
            else:
                self.redrawCounter = 0
                self.timer.stop()
                timer_stop_function()
        self.app.processEvents()
