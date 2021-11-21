from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys

class PipeGalleryManager(QDialog):

    def __init__(self):
        super(PipeGalleryManager, self).__init__()
        self.setWindowTitle("Open/Import/Reference")
        self.setMinimumSize(300,80)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.le_text = QLineEdit("text", self)
        self.button1 = QPushButton("myButton1gdga",self)
        self.button2 = QPushButton("myButton2", self)



    def create_layouts(self):
        self.ui_horizontal_lay = QHBoxLayout()
        self.ui_horizontal_lay.addWidget(self.le_text)

        self.ui_vertical_lay = QVBoxLayout()
        self.ui_vertical_lay.addWidget(self.button1)
        
        self.ui_vertical_lay.addWidget(self.button2)

        self.ui_main_lay = QHBoxLayout(self)
        self.ui_main_lay.addLayout(self.ui_horizontal_lay)
        self.ui_main_lay.addLayout(self.ui_vertical_lay)


    def create_connections(self):
        self.button1.clicked.connect(self.on_button_pressed)



    def on_button_pressed(self):
        print("su madre")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PipeGalleryManager()
    window.show()
    app.exec_()

