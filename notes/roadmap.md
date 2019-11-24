# Thesis Roadmap and Notes

## Gathering user requirements
Currently, we are aware of the following use-cases for charting components:

- 25 FPS refresh rate. Up to 100k points in a single curve. Should plot up to 8 curves like that. Only one chart per application. (BE-CO-HT)
- 2D plot with 1000x1000 points at most. Data is viewable offline, therefore refresh rate for the new data is not important. What matters is responsiveness when rendering the static data set. (BE-OP-SPS)
- Display 3000 datasets on the same chart, 2 hours long each, updating every second. 2 * 3600 * 3000 points. (BE-OP-LHC)
- ScatterPlot with three 1h long sequences of data with a new point arriving every 1.2 seconds

If current solution proves to be inefficient, we shall investigate QCustomPlot and plausibility to generate Python bindings with SIP. There have been attempts in the past, but it's 2 years old. We need to check if it's still valid.

## Research benchmarking metrics and implement benchmarking application

3D Graphic Benchmarks for Hardware

1. Drawing -> How long does it take to draw one Frame?
2. Interaction -> Same, since QtApplications EventLoop will only react to interaction
   if it is not occupied by anything

References / Books for benchmarking:
- Roger W. Hockney, The science of computer benchmarking

## Analysis + Profiling
- 

## Enhancments
- Improve qt paint cycle and only redraw if wanted
  - Partial redraws? -> Does not make sense with zooming in any way
- Graphics View is optimized for a lot of small items, but pyqtgraph uses one
  item that is completely drawn by the paint() function of each item
- OpenGL example on line graph?
