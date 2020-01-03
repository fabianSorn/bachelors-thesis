import sys
from qtpy import QtCore, QtGui, QtWidgets

class MouseClickFilter(QtCore.QObject):

    def eventFilter(self, _: QtCore.QObject, e: QtCore.QEvent):
        """Filter out all Mouse Clicks, single or double"""
        intercept = [QtCore.QEvent.MouseButtonDblClick,
                     QtCore.QEvent.MouseButtonPress]
        if e.type() in intercept:
            print("Filter Mouse Click.")
            return True
        return super().eventFilter(_, e)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.installEventFilter(MouseClickFilter(parent=app))
    win = QtWidgets.QMainWindow()
    win.show()
    sys.exit(app.exec())