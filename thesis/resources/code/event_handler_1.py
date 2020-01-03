from qtpy import QtWidgets, QtCore, QtGui

class ChangingLabelOne(QtWidgets.QLabel):

    def event(self, e: QtCore.QEvent) -> bool:
        """Change Label Font Size thorugh Mouse Click"""
        if e.type() == QtCore.QEvent.MouseButtonPress:
            font: QtGui.QFont = self.font()
            if e.button() == QtCore.Qt.RightButton:
                font.setPointSize(font.pointSize() - 1)
            elif e.button() == QtCore.Qt.LeftButton:
                font.setPointSize(font.pointSize() + 1)
            self.setFont(font)
            return True
        else:
            return super().event(e)
