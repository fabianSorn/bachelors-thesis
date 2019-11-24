from src.linegraph.benchmarkLineGraphConfig import LineGraphConfig
from src.heatmap.benchmarkHeatmapConfig import HeatmapConfig
import datetime
import subprocess

class BenchmarkResultWriter():

    def __init__(self, file_location: str = "results/benchmarkresults.txt"):
        self.file_location = file_location

    def write_linegraph_benchmark_result_header(self):
        self.__write_generic_benchmark_result_header(self.__print_linegraph_header)

    def write_heatmap_benchmark_result_header(self):
        self.__write_generic_benchmark_result_header(self.__print_linegraph_header())

    def write_result_end(self):
        self.append_line("~~~~~~~~~~~~~~~~~~~~~~ End of Benchmark ~~~~~~~~~~~~~~~~~~~~~")
        self.append_line("")

    def append_line(self, text: str):
        if not text.endswith("\n"):
            text += "\n"
        try:
            with open(self.file_location, 'a') as file:
                file.write(text)
        except IOError:
            with open(self.file_location, "w+") as file:
                file.write(text)

    # Private

    def __write_generic_benchmark_result_header(self, print_benchmark_specific_stuff_function):
        self.append_line("~~~~~~~~~~~~~~~~~~~~~~~ New Benchmark ~~~~~~~~~~~~~~~~~~~~~~~")
        print_benchmark_specific_stuff_function()
        self.append_line("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self.__print_linegraph_header()
        self.append_line("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def __print_linegraph_header(self):
        self.append_line("Type of Benchmark:      Linegraph Benchmark")
        self.append_line("Test Started at:        " + str(datetime.datetime.now()))
        self.append_line("Test for Datasetsize:   " + str(LineGraphConfig.benchmark_dataset_sizes))
        self.append_line("Test for Datasetcounts: " + str(LineGraphConfig.benchmark_linecounts))
        self.append_line("Graph Size:             " + str(LineGraphConfig.graph_size_width) + " x "
                         + str(LineGraphConfig.graph_size_height))

    def __print_heatmap_header(self):
        self.append_line("Type of Benchmark:      Heatmap Benchmark")
        self.append_line("Test Started at:        " + str(datetime.datetime.now()))
        self.append_line("Size of shown image:    " + str(HeatmapConfig.x_range) + "x" + str(HeatmapConfig.y_range))
        self.append_line("Graph Size:             " + str(HeatmapConfig.graph_display_size_x) + " x "
                         + str(HeatmapConfig.graph_display_size_y))

    def __print_hardware_information(self):
        result = subprocess.run(['lspci'], stdout=subprocess.PIPE)
        self.append_line(result.stdout.decode('utf-8'))
