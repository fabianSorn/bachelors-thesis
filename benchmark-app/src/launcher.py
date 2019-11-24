"""
Launcher for starting a QApplication with a window which is
loaded from a python module that is passed as the parameter
"file" when invoking this script. The loaded window should
be a QMainWindow which inherits from the Benchmark class to
have a common interface for executing the Benchmark and
getting its results.
"""

import sys
import os
import importlib.util
import inspect
import argparse
from typing import Union, Type, List, Optional
import logging

from qtpy.QtCore import QObject, Slot, Qt, QMetaObject
from qtpy.QtWidgets import QApplication

from src.benchmark import BenchmarkWindow, BenchmarkResults

logger = logging.getLogger(__name__)
_BENCHMARK_REFERENCE_NAME = "BENCHMARK_CLASS"


class InvalidBenchmarkError(BaseException):
    pass


class BenchmarkLauncher:

    """
    Class for launching any benchmark windows. This launcher
    can either be constructed from a passed class or from a
    class loaded from a given module path.

    If a path is passed, the module has to contain a global
    variable BENCHMARK_CLASS
    """

    def __init__(
            self,
            benchmark_class: Union[str, Type],
            class_reference_attribute: str = _BENCHMARK_REFERENCE_NAME
    ):
        self._benchmark_window_type: Type
        self._class_reference_attribute = class_reference_attribute
        if isinstance(benchmark_class, str):
            self._benchmark_window_type = self._import_benchmark_class(
                benchmark_class
            )
        elif issubclass(benchmark_class, BenchmarkWindow):
            self._benchmark_window_type = benchmark_class
        else:
            raise TypeError(
                "The passed benchmark class is not from type BenchmarkWindow"
            )

    def run(
            self,
            max_repeat: Optional[int] = None,
            sys_exit_on_complete: bool = False,
            app_args: List[str] = None,
    ):
        if not app_args:
            app_args = []
        app = QApplication(app_args)
        benchmark: BenchmarkWindow = self._benchmark_window_type(
            app=app,
            max_repeat=max_repeat
        )
        _ = BenchmarkResultHandler(app, benchmark)
        if sys_exit_on_complete:
            sys.exit(app.exec_())
        else:
            app.exec_()

    def _import_benchmark_class(self, file_name: str):
        """
        Try to import a benchmark window class from the module the given
        file path is referencing. First, see if any class is referenced
        by the BENCHMARK_CLASS or an other passed attribute and if not
        search for classes derived from
        """
        module_name: str = os.path.basename(file_name)
        path: str = file_name
        spec = importlib.util.spec_from_file_location(module_name, path)
        benchmark_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(benchmark_module)
        logger.debug(
            f"Search for benchmark in module {module_name}."
        )
        try:
            return getattr(benchmark_module, self._class_reference_attribute)
        except AttributeError:
            logger.debug(
                f"Reference attribute {self._class_reference_attribute} "
                f"could not be found in module {module_name}."
            )
            for name, obj in inspect.getmembers(benchmark_module, inspect.isclass):
                possible_benchmark_classes: List[Type] = []
                if issubclass(obj, BenchmarkWindow):
                    logger.debug(
                        f"Found benchmark class {name} derived from {BenchmarkWindow.__name__}."
                    )
                    possible_benchmark_classes.append(obj)
                logger.warning(f"Module {module_name} contains multiple benchmark "
                               f"classes derived from {BenchmarkWindow.__name__}.")
                return possible_benchmark_classes[0]
            raise InvalidBenchmarkError(
                f"No benchmark window could be found in module {module_name}."
            )


class BenchmarkResultHandler(QObject):

    """
    The Benchmark will notify about its completion by emitting a signal.
    This Handler will wait for receiving this signal and
    """

    def __init__(self, app: QApplication, benchmark: BenchmarkWindow):
        super().__init__()
        self._app: QApplication = app
        if not benchmark.shown:
            benchmark.show()
        benchmark.sig_completed.connect(self._benchmark_completed)
        # benchmark.metaObject().invokeMethod(benchmark, "run", Qt.QueuedConnection)

    @Slot(BenchmarkResults)
    def _benchmark_completed(self, result: BenchmarkResults):
        # Finally quit the subprocess
        print(f"On average, {result.operations_per_seconds} "
              f"operations per second were executed.")
        self._app.closeAllWindows()
        self._app.quit()


def main():
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        "file",
        type=str,
        help=""
    )
    args = parser.parse_args()
    app_args = sys.argv
    app_args.remove(args.file)
    BenchmarkLauncher(args.file).run(
        sys_exit_on_complete=True,
        app_args=app_args
    )


if __name__ == '__main__':
    main()