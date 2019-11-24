import sys
from PyQt5.QtWidgets import *
from src.benchmarkDashboard import BenchmarkDashboard

def run():
    app = QApplication(sys.argv)
    gui = BenchmarkDashboard(app)
    sys.exit(app.exec_())

run()