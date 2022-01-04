from PySide2.QtWidgets import QApplication, QDialog, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QSpinBox, QVBoxLayout, QFileDialog
from .file_utils import rename_files, renumber_files, fix_padding, get_first_file_from_sequence

import sys

import os


class Renamer(QDialog):
    def __init__(self):
        super(Renamer, self).__init__()
        self.setWindowTitle("RENAME - RENUMBER")
        self.setMinimumSize(600,250)
        
        self.folder = ""
        self.old_text = ""
        self.new_text = ""
        self.new_start = 1001		
        
        self.full_sequence = []
        
        
        self.widgets()
        self.layouts()
        self.connections()
        
        
    def widgets(self):
        self.ln_folder_path = QLineEdit()
        self.ln_folder_path.setPlaceholderText("Path to the folder")
        self.btn_folder = QPushButton("Folder")
        
        self.lbl_file_sequence = QLabel()
        
        self.ln_old_text = QLineEdit()
        self.ln_new_text = QLineEdit()       
         
        self.grp_chks = QGroupBox("Usage")
        self.chk_prefix = QRadioButton("Prefix")
        self.chk_suffix = QRadioButton("Suffix")
        self.chk_replace = QRadioButton("Replace")  
        self.chk_replace.setChecked(True) 
        
        self.btn_rename = QPushButton("Rename") 
        
        self.spn_renumber = QSpinBox()
        self.spn_renumber.setMaximum(10000)
        self.spn_renumber.setValue(1001)
        self.btn_renumber = QPushButton("Re-Number")
        
        self.btn_padding = QPushButton("Fix Padding")
        

    def layouts(self):
        self.lyt_v_main = QVBoxLayout()
        self.lyt_h_folder = QHBoxLayout()
        
        self.lyt_form = QFormLayout()
        self.lyt_form.addRow("Old Text: ", self.ln_old_text)
        self.lyt_form.addRow("New Text: ", self.ln_new_text)    
        
        self.lyt_form_file_name = QFormLayout()
        self.lyt_form_file_name.addRow("File Sequence: ", self.lbl_file_sequence)
        
        self.lyt_renumber_form = QFormLayout()
        self.lyt_renumber_form.addRow("New Starting Frame: ", self.spn_renumber)
        
        self.lyt_chks = QHBoxLayout()
        self.lyt_chks.addWidget(self.chk_replace)
        self.lyt_chks.addWidget(self.chk_suffix)
        self.lyt_chks.addWidget(self.chk_prefix) 
        self.lyt_chks.addStretch()  
        self.lyt_chks.addWidget(self.btn_rename)
        self.grp_chks.setLayout(self.lyt_chks) 
        
        self.lyt_renumber = QHBoxLayout()
        self.lyt_renumber.addStretch()
        self.lyt_renumber.addLayout(self.lyt_renumber_form)     
        self.lyt_renumber.addWidget(self.btn_renumber)
        self.lyt_renumber.addWidget(self.btn_padding)
        
        self.lyt_h_folder.addWidget(self.btn_folder)
        self.lyt_h_folder.addWidget(self.ln_folder_path)        
        
        self.lyt_v_main.addLayout(self.lyt_h_folder)        
        self.lyt_v_main.addLayout(self.lyt_form_file_name)          
        self.lyt_v_main.addLayout(self.lyt_form) 
        self.lyt_v_main.addWidget(self.grp_chks)      
        self.lyt_v_main.addStretch() 
        self.lyt_v_main.addLayout(self.lyt_renumber)        
        self.lyt_v_main.addStretch()  
        

        self.setLayout(self.lyt_v_main)           


    def connections(self):
        self.btn_folder.clicked.connect(self.lookup_dir)
        self.ln_folder_path.textEdited.connect(self.update_folder_text)
        self.ln_old_text.textEdited.connect(self.update_old_text)
        self.ln_new_text.textEdited.connect(self.update_new_text)
        self.spn_renumber.valueChanged.connect(self.update_new_start_frame)
        self.btn_rename.clicked.connect(self.rename)
        self.btn_renumber.clicked.connect(self.renumber)
        self.btn_padding.clicked.connect(self.padding)
        

    def lookup_dir(self):
        asset_dir = QFileDialog.getExistingDirectory(self, "Select Folder")        
        self.ln_folder_path.setText(asset_dir)
        self.folder = asset_dir
        self.return_first_element(asset_dir)
        
    
    def update_list_from_files_in_folder(self):
        files = os.listdir(self.folder)
        self.full_sequence = files
        return files
        

    def update_folder_text(self):
        self.folder = self.ln_folder_path.text()
        

    def update_old_text(self):
        self.old_text = self.ln_old_text.text()
        

    def update_new_text(self):
        self.new_text = self.ln_new_text.text()
        

    def update_new_start_frame(self):
        self.new_start = int(self.spn_renumber.text())
        

    def rename(self):        
        if self.chk_prefix.isChecked():
            mode = "prefix"
        if self.chk_suffix.isChecked():
            mode = "suffix"
        if self.chk_replace.isChecked():
            mode = "replace"         

        if os.path.isdir(self.folder) and len(self.new_text) > 0 and len(self.old_text) > 0:
            			
            self.full_sequence = rename_files(self.folder, mode, self.old_text, self.new_text)
            self.update_list_from_files_in_folder()
            self.return_first_element(self.folder)
            

    def renumber(self):
        if os.path.isdir(self.folder):
            renumber_files(self.folder, self.new_start, 4)
            self.return_first_element(self.folder)
        
            
            
    def padding(self):
        if os.path.isdir(self.folder):
            print(self.folder)
            fix_padding(self.folder)
            self.return_first_element(self.folder)
            
        
    def return_first_element(self, dir_name):
        first_file = get_first_file_from_sequence(dir_name)
        self.lbl_file_sequence.setText(first_file)
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    w = Renamer()
    w.show()
    
    sys.exit(app.exec_())
        
        