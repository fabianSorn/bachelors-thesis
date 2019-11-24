import time
from typing import List, Callable
from abc import ABC, ABCMeta, abstractmethod

from qtpy.QtCore import (
    Signal,
    Slot,
    QTimer,
    QObject,
)
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
)
from qtpy.QtGui import (
    QShowEvent,
)


class AbstractQMainWindowMeta(type(QMainWindow), ABCMeta):  # type: ignore

    """ Metaclass for abstract classes based on QObject

    A class inheriting from QObject with ABCMeta as metaclass will lead to
    an metaclass conflict:

    TypeError: metaclass conflict: the metaclass of a derived class must be
    a (non-strict) subclass of the meta-classes of all its bases
    """

    pass


class BenchmarkResults(QObject):

    """
    Benchmark results need to be derived from QObject to be usable
    as a data type in signals.
    """

    def __init__(
            self,
            operations_per_seconds: float,
    ):
        super().__init__()
        self._ops_ps = operations_per_seconds

    @property
    def operations_per_seconds(self):
        return self._ops_ps


class BenchmarkWindow(QMainWindow, metaclass=AbstractQMainWindowMeta):

    """
    Abstract Base class for all benchmarks to define a common
    interface that can be used by the launcher to run it.
    """

    sig_completed = Signal([BenchmarkResults])

    def __init__(self, app: QApplication, max_repeat: int = 100):
        # super().__init__()
        QMainWindow.__init__(self)
        self.shown = False
        self._app: QApplication = app
        self._running: bool = False
        self.performance_recorder = PerformanceRecorder(
            init_operation=self.init_operation,
            process_operation=self.process_operation,
            max_repeat=max_repeat
        )
        self.performance_recorder.sig_recording_completed.connect(
            self._completed
        )

    def showEvent(self, event: QShowEvent):
        """We want to execute the benchmark"""
        self.shown = True
        if not self._running:
            self._running = True
            self._run()
        QMainWindow.showEvent(self, event)

    @Slot()
    def _run(self):
        """
        Entrypoint for the actual benchmark. All operations executed in here are
        part of the performance measuring.
        """
        self.performance_recorder.launch()

    @Slot(BenchmarkResults)
    def _completed(self, results: BenchmarkResults):
        self.sig_completed.emit(results)
        self._running = False

    @abstractmethod
    def init_operation(self):
        """
        Initializer that will trigger
        """
        pass

    def process_operation(self):
        """
        Process events that are pending because of the launch
        operation. The default is to tell the QApplication to process
        pending events. Overwrite this function to pass or make other
        processing events happen.
        """
        self._app.processEvents()


class PerformanceRecorder(QObject):

    """
    The performance recorder is a class that triggers an operation
    by using a QTimer and records the time that it took until the
    operation is called again.
    We use the QTimer to make sure that we do not create a blocking
    benchmark and allow the QApplication to return to the EventLoop
    to process events.
    """

    sig_recording_completed = Signal([BenchmarkResults])

    def __init__(
            self,
            init_operation: Callable,
            process_operation: Callable,
            max_repeat: int
    ):
        QObject.__init__(self)
        # Operations
        self._init_operation = init_operation
        self._process_operation = process_operation
        # Performance metrics
        self._last_time = time.time()
        self._timer: QTimer = QTimer()
        self._execution_recorder: int = 0
        self._max_repeat = max_repeat
        self._timing_recorder: List[float] = []

    def launch(self):
        """Launch the performance recorder"""
        # self.reset()
        self._timer.timeout.connect(self._execute)
        self._timer.start(0)

    def _execute(self):
        self._init_operation()
        now = time.time()
        delta = now - self._last_time
        self._last_time = now
        self._timing_recorder.append(delta)
        if len(self._timing_recorder) > self._max_repeat:
            self._timer.stop()
            results = BenchmarkResults(
                operations_per_seconds=self.operations_per_second
            )
            self.sig_recording_completed[BenchmarkResults].emit(results)
        self._process_operation()

    @property
    def avg_timing(self):
        return sum(self._timing_recorder) / len(self._timing_recorder)

    @property
    def operations_per_second(self):
        return 1.0 / self.avg_timing

    @property
    def results(self):
        return 0.0
