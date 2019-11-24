"""A simple example """

from time import sleep

from src.benchmarks.label_benchmark import LabelBenchmark
from src.launcher import BenchmarkLauncher

launcher = BenchmarkLauncher(LabelBenchmark)
# Repeat the operation, which should be benchmarked, 120 times
launcher.run(max_repeat=120)
sleep(1)
launcher.run(max_repeat=120)