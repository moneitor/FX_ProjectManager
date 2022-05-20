from telnetlib import SE
from .create_hda_logic import PPM_HDA
from PySide2.QtWidgets import QDialog, QStyleFactory
from PySide2 import QtCore

import hou
from .hda_saver_compile import Ui_HDA_Manager_UI

from utilityFunctions import fix_name

import os
import sys


parentHou = hou.ui.mainQtWindow()




class HDA_Save(QDialog, Ui_HDA_Manager_UI):
    """
    File Saving dialog
    """
    def __init__(self, parent=parentHou):
        super(HDA_Save, self).__init__()
        
        self._name = "default"
        self._path = ""
        self._version = "1"
        self._description = ""
        self._number_of_inputs = 1
        
        self.setMinimumWidth(600)
        self.setWindowTitle("HDA Publisher")
        
        self.setupUi(self)
        self.btn_save.setEnabled(False)
        
        self.connections()
        
    
    def connections(self):
        
        self.btn_cancel.clicked.connect(self.close)
        self.ln_name.textChanged.connect(self.set_name)
        self.ln_name.textChanged.connect(self._fix_name)
        self.ln_name.textChanged.connect(self.activate_save)
        self.ln_description.textChanged.connect(self.set_name)
        self.ln_description.textChanged.connect(self.activate_save)
        self.spn_version.valueChanged.connect(self.set_name)
        self.spn_inputs.valueChanged.connect(self.set_name)
        self.btn_save.clicked.connect(self.set_name)        
        self.btn_save.clicked.connect(self.accept)      


  
        
    def activate_save(self):
        if (self.ln_name.text()) != "" and self.ln_description.toPlainText() != "":
            self.btn_save.setEnabled(True)
        else:
            self.btn_save.setEnabled(False)
            
        
        
    def set_name(self):
            
        self._name = self.ln_name.text()
        self._version = self.spn_version.text()
        self._number_of_inputs = int(self.spn_inputs.text())
        
        global_parameter = self.cb_global.currentText()
        
        if global_parameter == "Project":
            self._path = os.path.join(os.getenv("PPM_COMMON_HOU"), "otls", self._name) + "_{}.otllc".format(self._version.zfill(3))   
        if global_parameter == "Globally":
            self._path = os.path.join(os.getenv("GLOBAL_COMMON_HOU"), "otls", self._name) + "_{}.otllc".format(self._version.zfill(3))  
            
        self.lbl_path.setText(self._path)      


    def _fix_name(self, t):
        new_text = fix_name(t)
        self.ln_name.setText(new_text) 

        
   
        
    
    def return_name(self):
        self.set_name()
        return self._name
    
    
    def return_path(self):
        self.set_name()
        return self._path
    
    
    def return_inputs(self):
        self.set_name()
        return self._number_of_inputs
    
    def return_version(self):
        self.set_name()
        return self._version
    
    def return_description(self):
        self.set_name()
        return self._description         
        
        
        

def show_ui():
    try:
        open_app.close()
        open_app.deleteLater()
    except:
        pass

    open_app = HDA_Save()
    open_app.setParent(parentHou, QtCore.Qt.Window)

    open_app.setStyle(QStyleFactory.create("fusion"))    

    open_app.show()
