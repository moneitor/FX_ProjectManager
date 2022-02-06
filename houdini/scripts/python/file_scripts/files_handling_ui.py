from PySide2.QtWidgets import QWidget, QListWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QStyleFactory, QMessageBox
from PySide2 import QtCore
from .files_handling import Houdini_Files
import os


import hou
parentHou = hou.ui.mainQtWindow()


class Files(QDialog):
    def __init__(self, parent=parentHou ):
        super(Files, self).__init__()
        self.setWindowTitle("Open File")
        self.setMinimumSize(400,300)
        
        self._full_file_path = ""        
        
        self.widgets()
        self.layouts()
        self.connections()
        
        self.populate_list()
        
        
    def widgets(self):
        self.lbl_files = QLabel("Houdini Files:")
        self.lst_files = QListWidget()  
        self.btn_open = QPushButton("Open")
        self.btn_cancel = QPushButton("Cancel")
        
    
    def layouts(self):
        self.lyt_main = QVBoxLayout()
        
        self.lyt_buttons = QHBoxLayout()
        self.lyt_buttons.addStretch()
        self.lyt_buttons.addWidget(self.btn_open)
        self.lyt_buttons.addWidget(self.btn_cancel)
        
        self.lyt_main.addWidget(self.lbl_files)
        self.lyt_main.addWidget(self.lst_files)
        
        self.lyt_main.addLayout(self.lyt_buttons)        
        
        
        self.setLayout(self.lyt_main)
        
    
    def connections(self):
        
        self.btn_cancel.clicked.connect(self.close)    
        self.lst_files.itemClicked.connect(self.return_file_path)  
        self.btn_open.clicked.connect(self.open_file)
        self.btn_open.clicked.connect(self.accept)
        

    def populate_list(self):
        file_handler = Houdini_Files()
        files = file_handler.return_file_names()
        
        self.lst_files.addItems(files)
        
        
    def return_file_path(self, f):
        file_handler = Houdini_Files()
        path = file_handler.return_full_path(f.text())
        if os.path.isfile(path):
            self._full_file_path = path
            print (path)
            
    
    def open_file(self):
        if len(self._full_file_path ) > 0:
            if not hou.hipFile.hasUnsavedChanges():
                hou.hipFile.load(self._full_file_path )
                print("\n =============================\n")
                print ("Opening file at: " + self._full_file_path )
                print("\n =============================\n")
            else:
                msgBoxSave = QMessageBox(self)
                msgBoxSave.setText("Save your changes first")
                msgBoxSave.exec_()

        else:
            print("Please select a file")
        
        
        
        
        


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
