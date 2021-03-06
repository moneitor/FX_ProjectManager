from PySide2.QtWidgets import QWidget, QListWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QStyleFactory, QMessageBox, QFormLayout
from PySide2 import QtCore

from .files_handling import Houdini_Files

import os

from sys import platform

import hou
parentHou = hou.ui.mainQtWindow()


class Files(QDialog):
    def __init__(self, parent=parentHou ):
        super(Files, self).__init__()
        self.setWindowTitle("Open File")
        self.setMinimumSize(600,300)
        self.setMaximumSize(600,700)
        
        self._full_file_path = ""    
        self._file_time_created = ""    
        
        self.widgets()
        self.layouts()
        self.connections()
        
        self.populate_list()
        
        
    def widgets(self):
        self.lbl_files = QLabel("Houdini Files:")
        self.lst_files = QListWidget()  
        self.lst_files.setSortingEnabled(True)
        self.lst_files.setMinimumWidth(400)        
        self.btn_open = QPushButton("Open")
        self.btn_cancel = QPushButton("Cancel")
        self.lbl_file_date = QLabel("")
        self.lbl_file_size = QLabel("")
        
    
    def layouts(self):
        self.lyt_main = QVBoxLayout()
        
        self.lyt_list = QHBoxLayout()
        self.lyt_list.addWidget(self.lst_files)
        self.lyt_list.addStretch()
        
        self.lyt_buttons = QHBoxLayout()
        self.lyt_buttons.addStretch()
        self.lyt_buttons.addWidget(self.btn_open)
        self.lyt_buttons.addWidget(self.btn_cancel)
        
        self.form_date = QFormLayout()
        self.form_date.addRow("Last Modificated: ", self.lbl_file_date)
        self.form_date.addRow("File Size MB: ", self.lbl_file_size)
        
        self.lyt_main.addWidget(self.lbl_files) 
        self.lyt_main.addLayout(self.lyt_list)        
        self.lyt_main.addStretch()      
        self.lyt_main.addLayout(self.form_date) 
        self.lyt_main.addLayout(self.lyt_buttons)               
        
        
        self.setLayout(self.lyt_main)
        
    
    def connections(self):
        
        self.btn_cancel.clicked.connect(self.close)    
        self.lst_files.itemClicked.connect(self.return_file_path)  
        self.lst_files.itemClicked.connect(self.file_info)
        self.lst_files.itemDoubleClicked.connect(self.open_file)
        self.lst_files.itemDoubleClicked.connect(self.accept)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_open.clicked.connect(self.accept)
        

    def populate_list(self):
        file_handler = Houdini_Files()
        files = file_handler.return_file_names()
        
        if files:
            self.lst_files.addItems(files)
            
        self.lst_files.sortItems(QtCore.Qt.SortOrder(0)) # Sort items in alphabetical order
        
        
    def return_file_path(self, f):
        file_handler = Houdini_Files()
        path = file_handler.return_full_path(f.text())
        if os.path.isfile(path):
            self._full_file_path = path
            print (path)
            
    
    def open_file(self):
        if len(self._full_file_path ) > 0:
            #if not hou.hipFile.hasUnsavedChanges():    
            if platform == "win32":
                print ("Fixing path slashes for windows")
                self._full_file_path = self._full_file_path.replace("\\",'/')       
            
            print("\n =============================\n")
            print ("Opening file at: " + self._full_file_path )
            print("\n =============================\n")

            

            hou.hipFile.load(self._full_file_path )
            #else:
                #pass
                #msgBoxSave = QMessageBox(self)
                #msgBoxSave.setText("Save your changes first")
                #msgBoxSave.exec_()

        else:
            print("Please select a file")
            
    
    def file_info(self, f):
        file_handler = Houdini_Files()        
        
        self._file_time_created = file_handler.return_file_info(f.text())[0]
        self._file_size = file_handler.return_file_info(f.text())[1]
        
        self.lbl_file_date.setText(self._file_time_created)
        self.lbl_file_size.setText(self._file_size)
        
        
        
        
        


def show_files():
    try:
        open_app.close()
        open_app.deleteLater()
    except:
        pass

    open_app = Files()
    open_app.setParent(parentHou, QtCore.Qt.Window)

    open_app.setStyle(QStyleFactory.create("fusion"))    

    open_app.show()
