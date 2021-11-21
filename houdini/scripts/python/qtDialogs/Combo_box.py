import hou
import os

from file_scripts import palette
from PySide2 import QtCore, QtWidgets, QtGui

parentHou = hou.ui.mainQtWindow()

class SimpleDialog(QtWidgets.QWidget):
    def __init__(self, parent=parentHou):
        super(SimpleDialog, self).__init__()
        
        self.setMaximumSize(500,400)
        self.setMinimumSize(200,200)
        self.setWindowTitle("Simple Dialog")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.widgets()
        self.layout()
        self.connections()
        

    def widgets(self):
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(["Shot1", "Shot2", "Shot3", "Shot4"])

        self.btn_ok = QtWidgets.QPushButton("Ok")
        self.btn_cancel = QtWidgets.QPushButton("Cancel")

    def layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("combobox:", self.combobox)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.btn_ok)
        button_layout.addWidget(self.btn_cancel)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
      
        

    def connections(self):
        self.combobox.activated.connect(self.on_activated_int)
        self.combobox.activated[str].connect(self.on_activated_str)
        self.btn_cancel.clicked.connect(self.close)
        self.btn_ok.clicked.connect(self.close)

    @QtCore.Slot(int)
    def on_activated_int(self, index):
        print("ComboBox Index: {}".format(index))

    @QtCore.Slot(str)
    def on_activated_str(self, text):
        print("Combobox string: {}".format(text))




def run_app():
    # check if the dialog already exist and delete it
    # so it opens a new one
    try:
        app.close()
        app.deleteLater()
    except:
        pass

    app = SimpleDialog()
    app.setParent(parentHou, QtCore.Qt.Window)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    dark_palette = QtGui.QPalette()
    palette.Palette(dark_palette)

    app.setPalette(dark_palette)
    app.show()