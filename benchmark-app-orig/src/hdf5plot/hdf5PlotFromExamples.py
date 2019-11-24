# -*- coding: utf-8 -*-
"""
In this example we create a subclass of PlotCurveItem for displaying a very large
data set from an HDF5 file that does not fit in memory.

The basic approach is to override PlotCurveItem.viewRangeChanged such that it
reads only the portion of the HDF5 data that is necessary to display the visible
portion of the data. This is further downsampled to reduce the number of samples
being displayed.

A more clever implementation of this class would employ some kind of caching
to avoid re-reading the entire visible waveform at every update.
"""

#import initExample  ## Add path to library (just for examples; you do not need this)

import sys, os
import numpy as np
import h5py
import pyqtgraph as pg
from hdf5Plot import HDF5Plot
from pyqtgraph.Qt import QtCore, QtGui

pg.mkQApp()

plt = pg.plot()
plt.setWindowTitle('pyqtgraph example: HDF5 big data')
plt.enableAutoRange(False, False)
plt.setXRange(0, 500)

def createFile(finalSize=2000000000):
    """Create a large HDF5 data file for testing.
    Data consists of 1M random samples tiled through the end of the array.
    """

    chunk = np.random.normal(size=1000000).astype(np.float32)

    f = h5py.File('test.hdf5', 'w')
    f.create_dataset('data', data=chunk, chunks=True, maxshape=(None,))
    data = f['data']

    nChunks = finalSize // (chunk.size * chunk.itemsize)
    with pg.ProgressDialog("Generating test.hdf5...", 0, nChunks) as dlg:
        for i in range(nChunks):
            newshape = [data.shape[0] + chunk.shape[0]]
            data.resize(newshape)
            data[-chunk.shape[0]:] = chunk
            dlg += 1
            if dlg.wasCanceled():
                f.close()
                os.remove('test.hdf5')
                sys.exit()
        dlg += 1
    f.close()


if len(sys.argv) > 1:
    fileName = sys.argv[1]
else:
    fileName = 'test.hdf5'
    if not os.path.isfile(fileName):
        size, ok = QtGui.QInputDialog.getDouble(None, "Create HDF5 Dataset?",
                                                "This demo requires a large HDF5 array. To generate a file, enter the array size (in GB) and press OK.",
                                                2.0)
        if not ok:
            sys.exit(0)
        else:
            createFile(int(size * 1e9))
        # raise Exception("No suitable HDF5 file found. Use createFile() to generate an example file.")

f = h5py.File(fileName, 'r')
curve = HDF5Plot()
curve.setHDF5(f['data'])
plt.addItem(curve)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':

    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()