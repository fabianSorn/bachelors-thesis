from qtpy import QtWidgets, QtCore, QtGui

class ChangingLabelTwo(QtWidgets.QLabel):

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        """Change Label Font Size thorugh Mouse Click"""
        font: QtGui.QFont = self.font()
        if e.button() == QtCore.Qt.RightButton:
            font.setPointSize(font.pointSize() - 1)
        elif e.button() == QtCore.Qt.LeftButton:
            font.setPointSize(font.pointSize() + 1)
        self.setFont(font)