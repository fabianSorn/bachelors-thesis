import os
from typing import List
import logging

from qtpy.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel,
    QListView,
    QComboBox,
)

from .benchmark import BenchmarkWindow

logger = logging.getLogger(__name__)


_EXAMPLE_CONFIG = "__init__.py"
_LAUNCHER_FILE_NAME = "launcher.py"
_BENCHMARK_DIRECTORY = "benchmarks"
_BENCHMARK_NAME_ENDING = "_benchmark.py"
_BENCHMARK_NAME_EXCLUDES = [

]


_CURR_DIR = os.path.dirname(__file__)


class BenchmarkBrowser(QMainWindow):

    """Main Launcher for the different benchmarks"""

    def __init__(self, app: QApplication):
        super().__init__()
        self.q_app = app
        self._setup_ui()
        self._find_benchmarks()
        self.show()

    def _setup_ui(self):
        self.main_container = QWidget()
        self.main_layout = QGridLayout()
        self.setCentralWidget(self.main_container)
        self.main_container.setLayout(self.main_layout)
        self.setWindowTitle("Graph Library Benchmark Launcher")

    def _find_benchmarks(self):
        self.benchmark_list = QListView()
        self.launch_button = QPushButton("Launch Benchmark")
        self.launch_button.clicked.connect(self._launch_benchmark)
        self._benchmark_files = BenchmarkBrowser._get_benchmark_files()
        self._benchmark_combobox = QComboBox()
        self._benchmark_combobox.addItems(
            [os.path.basename(file) for file in self._benchmark_files]
        )
        self.main_layout.addWidget(self._benchmark_combobox)
        self.main_layout.addWidget(self.launch_button)

    def _launch_benchmark(self):
        """
        We want the benchmark to be executed in a separate process to make sure
        that its performance is measured more accurately by having its completely
        separated Qt Event Loop.
        Results from the subprocess can simply be captured by reading the sub
        processes stdout and stderr.
        """
        launcher = os.path.join(os.path.dirname(os.path.realpath(__file__)), _LAUNCHER_FILE_NAME)
        benchmark_window = self._benchmark_files[self._benchmark_combobox.currentIndex()]
        args: List[str] = ['python', launcher, benchmark_window]
        # Copied from comrad, see if I really need this?
        env = os.environ
        python_path = env.get('PYTHONPATH', '')
        env['PYTHONPATH'] = f'{_CURR_DIR}:{python_path}'
        # Launch subprocess and setup communication
        import subprocess
        try:
            process = subprocess.run(
                args=args,
                shell=False,
                env=env,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logger.debug(f" Benchmark subprocess stdout: \n{process.stdout.decode('utf-8')}")
            return process
        except subprocess.CalledProcessError as ex:
            name = os.path.basename(benchmark_window)
            logger.error(f"Launching {name} failed with Error Code {ex.returncode}.")
            logger.error(f" Benchmark subprocess output: \n{ex.output.decode('utf-8')}")
            logger.error(f" Benchmark subprocess error: \n{ex.stderr.decode('utf-8')}")

    @staticmethod
    def _get_benchmark_files() -> List[str]:
        benchmark_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), _BENCHMARK_DIRECTORY)
        logger.debug(f"Search benchmarks in directory '{benchmark_dir}'.")
        entries = os.listdir(benchmark_dir)
        file_locations: List[str] = []
        for entry in entries:
            if BenchmarkBrowser._is_benchmark_file(entry):
                logger.debug(f"Check file '{entry}' to list of benchmarks.")
                file_locations.append(os.path.join(benchmark_dir, entry))
        return file_locations

    @staticmethod
    def _is_benchmark_file(file_name: str) -> bool:
        """Check if the file is a benchmark."""
        logger.debug(f"Check if file '{file_name}' is benchmark.")
        return not file_name.startswith("_") and \
               not file_name.startswith(".") and \
               file_name not in _BENCHMARK_NAME_EXCLUDES and \
               file_name.endswith(_BENCHMARK_NAME_ENDING)
