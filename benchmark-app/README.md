# PyQtGraph Benchmarking Application
This application allows configuration and recording of the performance of PyQtGraph
components in different use cases. The performance calculation in FPS is based on
examples in PyQtGraphs list of examples. Those can be checked out after the
PyQtGraph installation by starting them in your python console via

`import pyqtgraph.examples`
 `pyqtgraph.examples.run() `
 
 ## FPS calculation
 The performance of each graph is evaluated by calculating how long it takes to
 redraw a single frame, which is done by using PyQt's Timer from the `PyQt5.QCore` 
 module.
 
 ## Supported test scenarios
 1. Line graphs with n plots per dataset with m datasets; n,m > 0
 2. Draw an image of the size x * y (for display of heatmaps)
 3. Draw line from dataset stored in an HDF5 file
 
 Many of the parameters can be configured `<...>Config.py` files. To make these
 changes work, you currently have to restart the application.
 
 ### Linegraphs
 The performance of the linegraph can be tested by running an the benchmark by
 clicking the button in the User Interface. This will cycle to different dataset
 sizes and dataset counts and will record the average Frames that could be drawn
 per second. Additionally the shown graph can also be altered by hand to simulate
 a fitting scenario.
 
 Additionally you can choose a HDF5 file as data-input instead of generating random
 data by switching in the User Interface.
 
 ### Image Graphs
 The image graph can be used to display an greyscale or colored image by providing
 data in an two/three dimensional array like `image[column][row] =greyscale value`
 or `image[column][row][rgba-color-channel] = color value`. Heatmaps, that map one
 value to a specific color would need the `pyqtgraph.ColorMap` for display.
 
