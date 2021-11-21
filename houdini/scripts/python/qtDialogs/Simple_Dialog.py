#import hou
import os

#from file_scripts import palette
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
        self.lineedit = QtWidgets.QLineEdit()
        self.checkbox1 = QtWidgets.QCheckBox("")
        self.checkbox2 = QtWidgets.QCheckBox("")
        self.btn_ok = QtWidgets.QPushButton("OK")
        self.btn_cancel = QtWidgets.QPushButton("Cancel")

    def layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Label: ", self.lineedit)
        form_layout.addRow("To Publish", self.checkbox1)
        form_layout.addRow("Only Cache", self.checkbox2)


        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_ok)
        buttons_layout.addWidget(self.btn_cancel)        

        main_layout = QtWidgets.QVBoxLayout(self)        
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)
        

    def connections(self):
        self.btn_cancel.clicked.connect(self.close)
        self.btn_ok.clicked.connect(self.close)




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