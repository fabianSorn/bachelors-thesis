# Print Project structure
foo@mbp ~ $: ll my_benchmarks
    -rw-r--r--  1 foo  bar   100B  1 Jan 00:00 bench_plot.py
    -rw-r--r--  1 foo  bar   100B  1 Jan 00:00 bench_image.py
    -rw-r--r--  1 foo  bar   100B  1 Jan 00:00 b_video.py
# Search files recursively from current working directory
foo@mbp ~ $: widgetmark
    Executing bench_plot.py
    - SinusCurve
    - ZoomingPlot
    Executing bench_image.py
    - HdImage
# Search files recursively from current working directory
foo@mbp ~ $: widgetmark .
    Executing bench_plot.py
    - SinusCurve
    - ZoomingPlot
    Executing bench_image.py
    - HdImage
# Search files recursively from given folder 
foo@mbp ~ $: widgetmark my_benchmarks
    Executing bench_plot.py
    - SinusCurve
    - ZoomingPlot
    Executing bench_image.py
    - HdImage
# Search use cases in given file
foo@mbp ~ $: widgetmark my_benchmarks/bench_plot.py
    Executing bench_plot.py
    - SinusCurve
    - ZoomingPlot
# Execute only single specific use case
foo@mbp ~ $: widgetmark my_benchmarks/bench_plot.py::SinusCurve
    Executing bench_plot.py
    - SinusCurve
# Search for files with different pattern
foo@mbp ~ $: widgetmark --pattern "b_*"
    Executing b_video.py
    - HdVideo
# Start widgetmark and create a profile
foo@mbp ~ $: widgetmark --profile --profile-output=profiles .
    Executing bench_plot.py
    - SinusCurve
    - ZoomingPlot
    Executing bench_image.py
    - HdImage
    Saving 3 profile files to ./profiles
# Profile outputs
foo@mbp ~ $: ll profiles
    -rw-r--r--  1 foo  bar   100B  1 Jan 00:00 bench_plot_SinusCurve.profile
    -rw-r--r--  1 foo  bar   100B  1 Jan 00:00 bench_plot_ZoomingPlot.profile
    -rw-r--r--  1 foo  bar   100B  1 Jan 00:00 bench_image_HdImage.profile
# Visualize profiles after creation
foo@mbp ~ $: widgetmark -p -o=profiles --visualize .
    ...
    Profile visualization is now available under http://localhost:8080/profiles
    ...
# Usage explaination for the command line interface
foo@mbp ~ $: widgetmark --help
    usage: widgetmark [-h] [-o PROFILE_FILES_LOCATION] [-p]
                      [--pattern USE_CASE_FILE_NAME_PATTERN] [--visualize]
                      [--loglevel LOGGING_MODULE_LEVEL]
                      [locations [locations ...]]

    A short explaination what widgetmark is.

    Explaination of the individual arguments:
        ...
# Output after the benchmark execution
foo@mbp ~ $: widgetmark .
---------------------------- WIDGET-MARK ----------------------------
> bench_image.py
  + HdImage              GOAL=30.0, MIN=20.0: .............      21.2
> bench_plot.py
  + SinusCurve
    - PYQTGRAPH          GOAL=30.0, MIN=20.0: .................. 56.6
    - MATPLOTLIB         GOAL=30.0, MIN=20.0: .                   1.3
      - Timed out after 20 seconds.
---------------------------------------------------------------------
Summary (Executed 3 Use Cases)
GOAL        1 Use Cases
MIN         1 Use Cases
NONE        1 Use Cases
---------------------------------------------------------------------
Exceptions  0 Use Cases
Timed Out   1 Use Cases
---------------------------------------------------------------------
