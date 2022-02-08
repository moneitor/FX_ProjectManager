from PySide2.QtWidgets import QDialog, QLineEdit, QPushButton, QSpinBox, QLabel, QHBoxLayout, QFormLayout, QVBoxLayout, QMessageBox, QStyleFactory, QWidget
from PySide2 import QtCore, QtGui
import hou
from .save_file_logic import fix_name

import os
import sys


parentHou = hou.ui.mainQtWindow()




class FileSave(QWidget):
    """
    File Saving dialog
    """
    def __init__(self, parent=parentHou):
        super(FileSave, self).__init__()
        self.setWindowTitle("Pipeline Save")
        self.file_name = ""        
        self.shot_path = os.getenv("SHOT")        
        self.version_value = 1
        self.full_name_for_save = ""
               

        self.setMinimumSize(800, 200)
        

        self.create_widgets()
        self.create_connections()
        self.create_layout()


    def create_widgets(self):
        """
        Widget creation for the interface
        """
        self.save_file = QPushButton("Save")
        self.save_file.setMaximumSize(100,50)      

        self.version = QSpinBox()
        self.version.setMaximumSize(70, 20)
        self.version.setMinimum(1)

        self.name = QLineEdit()
        self.name.setFrame(True)
        self.name.setPlaceholderText("Write the name of the file without spaces")

        self.cancel = QPushButton("Cancel")
        self.cancel.setMaximumSize(100, 50)

        self.display_name = QLabel("...")
        self.display_path = QLabel(os.getenv("SHOT"))
        

    def create_connections(self):
        """
        Connections between the widgets and the functions
        """       
        self.name.textChanged.connect(self._fix_name)
        self.name.textChanged.connect(self._concatenate_full_path)
        self.save_file.clicked.connect(self.save_file_ui)
        self.version.valueChanged.connect(self._concatenate_full_path)
        self.save_file.clicked.connect(self.close)
        self.cancel.clicked.connect(self.close)



    def create_layout(self):
        """
        Layout configuration and addition of the Widgets
        """

        form_layout_parms = QFormLayout()
        form_layout_parms.addRow("Name: ", self.name)        
        form_layout_parms.addRow("Version", self.version)

        form_layout_names = QFormLayout()
        form_layout_names.addRow("Name Display: ", self.display_name)
        form_layout_names.addRow("Full Path Display: ", self.display_path)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_file)
        buttons_layout.addWidget(self.cancel)

        main_layout = QVBoxLayout(self)  
        main_layout.addStretch()
        main_layout.addLayout(form_layout_parms)
        main_layout.addStretch()
        main_layout.addLayout(form_layout_names)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)
        
    
    def _fix_name(self, t):
        new_text = fix_name(t)
        self.name.setText(new_text)
        
        self.display_name.setText(new_text)
        
        self.file_name = new_text
        
        
    def _return_version(self):
        ver = self.version.text()
        
        version = ver.zfill(3)
        return version
        
        
    def _concatenate_full_path(self):
        shot_path = self.shot_path
        file_name = self.file_name
        shot_name = os.path.basename(shot_path)
        version = self._return_version()
        
        
        full_path = os.path.join(shot_path, "work", "fx", shot_name + "_" + file_name + "_v" + version + ".hipnc")
        self.full_name_for_save = full_path
        
        self.display_path.setText(self.full_name_for_save)
        
        


    def save_file_ui(self):
        if(os.path.isdir(self.shot_path)) and len(self.name.text())>0:
            print("Saving file on {}".format(self.full_name_for_save))
            hou.hipFile.save(self.full_name_for_save, True)
           
        else:
            msgBox = QMessageBox(self)
            msgBox.setText("The shot folder doesn't exist")
            msgBox.exec_()


    #####################################################################################

def run_app():
    try:
        app.close()
        app.deleteLater()
    except:
        pass
    
    app = FileSave()
    app.setParent(parentHou, QtCore.Qt.Window)
    app.setStyle(QStyleFactory.create("fusion"))


    app.show()



