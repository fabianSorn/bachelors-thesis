import sys
from qtpy import QtWidgets, QtGui, QtCore


class ChangingLabel(QtWidgets.QLabel):

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        font: QtGui.QFont = self.font()
        if e.button() == QtCore.Qt.RightButton:
            font.setPointSize(font.pointSize() - 1)
        elif e.button() == QtCore.Qt.LeftButton:
            font.setPointSize(font.pointSize() + 1)
        self.setFont(font)


class LabelMouseClickFilter(QtCore.QObject):

    def eventFilter(self, o: QtCore.QObject, e: QtCore.QEvent):
        """Filter out all Mouse Clicks, single or double"""
        intercept = [QtCore.QEvent.MouseButtonDblClick,
                     QtCore.QEvent.MouseButtonPress]
        if e.type() in intercept and isinstance(o, QtWidgets.QLabel):
            return True
        return super().eventFilter(o, e)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()
        self._app = app
        self.setWindowTitle("Event Demo")
        cw = QtWidgets.QWidget()
        self.setCentralWidget(cw)
        cl = QtWidgets.QGridLayout()
        cw.setLayout(cl)
        self._filter = LabelMouseClickFilter(parent=app)
        self._label_1 = ChangingLabel("I react to Mouse Clicks!")
        self._label_2 = ChangingLabel("I react to Mouse Clicks as well!")
        self._checkbox = QtWidgets.QCheckBox("Install Event Filter")
        self._button = QtWidgets.QPushButton("Send Left Click to Labels")
        self._checkbox.stateChanged.connect(self._install_filter)
        self._button.pressed.connect(self._send)
        cl.addWidget(self._label_1, 0, 0)
        cl.addWidget(self._label_2, 0, 1)
        cl.addWidget(self._checkbox, 1, 0)
        cl.addWidget(self._button, 1, 1)
        self.show()

    def _install_filter(self, checked: int):
        if checked:
            self._app.installEventFilter(self._filter)
        else:
            self._app.removeEventFilter(self._filter)

    def _send(self):
        for label in [self._label_1, self._label_2]:
            event = QtGui.QMouseEvent(
                QtCore.QEvent.MouseButtonPress,
                QtCore.QPoint(0.0, 0.0),
                QtCore.QPoint(0.0, 0.0),
                QtCore.QPoint(0.0, 0.0),
                QtCore.Qt.LeftButton,
                QtCore.Qt.LeftButton,
                QtCore.Qt.NoModifier
            )
            QtCore.QCoreApplication.postEvent(label, event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    event_filter = LabelMouseClickFilter(parent=app)
    window = MainWindow(app)
    sys.exit(app.exec())