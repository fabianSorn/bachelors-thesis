from qtpy import QtCore, QtGui, QtWidgets

class ChangingLabelOne(QtWidgets.QLabel):
    pass

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        widget = ChangingLabelOne("Test")
        self.setCentralWidget(widget)
        event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonPress,
            QtCore.QPoint(0.0, 0.0),
            QtCore.QPoint(0.0, 0.0),
            QtCore.QPoint(0.0, 0.0),
            QtCore.Qt.LeftButton,
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoModifier
        )
        QtCore.QCoreApplication.postEvent(widget, event)
        self.show()
