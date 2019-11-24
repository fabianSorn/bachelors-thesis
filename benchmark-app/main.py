import sys
import logging

from qtpy.QtWidgets import QApplication
from src.browser import BenchmarkBrowser

logging.basicConfig(level=logging.DEBUG)

def run():
    """Start the Benchmark Launcher"""
    app = QApplication(sys.argv)
    _ = BenchmarkBrowser(app=app)
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()