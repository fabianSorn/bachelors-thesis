class LineGraphConfig:

    min_line_count = 1
    max_line_count = 3000
    min_dataset_size_in_K = 1
    max_dataset_size_in_K = 21600
    # min redraws for max datasets, max for min ones, linear in between
    min_number_of_redraws = 50
    max_number_of_redraws = 100
    # List should be between the boundaries in the lines above
    # Dataset Sizes in Thousands => 10  -> 10.000 points to draw
    benchmark_dataset_sizes = [100]
    benchmark_linecounts = [1, 4, 8]
    graph_size_width = 800
    graph_size_height = 600
    result_file_name = "results/benchmarkresults.txt"
    table_headers = ('Dataset Size', 'Dataset Count', 'PyQtGraph Type', 'Average FPS')
