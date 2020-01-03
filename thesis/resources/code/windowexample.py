import sys
from qtpy import QtWidgets


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)
        self.setup_widgets()
        self.setup_layout()
        self.set_widgets_text()
        self.show()

    def setup_widgets(self):
        # Upper part of the window (horizontally aligned widgets)
        self.central_widget = QtWidgets.QWidget(self)
        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.upper_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.check_box = QtWidgets.QCheckBox(self.central_widget)
        self.label = QtWidgets.QLabel(self.central_widget)
        self.push_button = QtWidgets.QPushButton(self.central_widget)
        # Lower part of the window (tabs)
        self.tab_widget = QtWidgets.QTabWidget(self.central_widget)
        self.content_tab_1 = QtWidgets.QWidget(self.tab_widget)
        self.content_tab_2 = QtWidgets.QWidget(self.tab_widget)
        self.layout_tab_1 = QtWidgets.QGridLayout(self.content_tab_1)
        self.layout_tab_2 = QtWidgets.QGridLayout(self.content_tab_2)
        self.label_tab_1 = QtWidgets.QLabel(self.content_tab_1)
        self.label_tab_2 = QtWidgets.QLabel(self.content_tab_2)

    def setup_layout(self):
        # Set size and central widget
        self.resize(360, 200)
        self.setCentralWidget(self.central_widget)
        # Fill upper half of the window
        self.central_layout.addLayout(self.upper_layout)
        self.upper_layout.addWidget(self.check_box)
        self.upper_layout.addWidget(self.label)
        self.upper_layout.addWidget(self.push_button)
        self.central_layout.addWidget(self.tab_widget)
        # Fill lower half of the window
        self.tab_widget.addTab(self.content_tab_1, "")
        self.tab_widget.addTab(self.content_tab_2, "")
        self.layout_tab_1.addWidget(self.label_tab_1)
        self.layout_tab_2.addWidget(self.label_tab_2)
        self.tab_widget.setCurrentIndex(0)

    def set_widgets_text(self):
        self.setWindowTitle("Example Application")
        # Set texts in the upper half of the window
        self.check_box.setText("CheckBox")
        self.label.setText("TextLabel")
        self.push_button.setText("PushButton")
        # Set texts in the lower half of the window
        self.tab_widget.setTabText(0, "Tab 1")
        self.tab_widget.setTabText(1, "Tab 2")
        self.label_tab_1.setText("This is the content of Tab I")
        self.label_tab_2.setText("This is the content of Tab II")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    _ = MainWindow()
    sys.exit(app.exec())
