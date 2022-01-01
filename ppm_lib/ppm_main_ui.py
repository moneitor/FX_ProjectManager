from PySide2 import QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QTabWidget, QVBoxLayout, QWidget
import ppm_main_logic as logic
import sys
import ppm_logger.logger as lg
from PySide2.QtCore import Qt
from entity import project as pr
from entity import sequence as sq
from ui.palette import Palette


import ppm_new_project_ui as new_ui
import ppm_new_seq_ui as new_ui_seq

import os


class PPM_Main_UI(QDialog):
    def __init__(self):
        super(PPM_Main_UI, self).__init__()
        self.setWindowTitle("PROJECT MANAGER")
        self.setMaximumWidth(700)
        self.setMinimumHeight(400)
        
        self._project = None
        self._project_name = ""
        self._project_fps = ""
        self._project_resolution = ""
        
        self._sequence_name = ""
        self._sequence = None
        self._sequence_path = ""
        
        self._shot_name = ""
        self._shot = None               
        self._shot_path = ""
        
        self._project_path = "" 
        
        self.widgets()
        self.layouts()
        self.connections()
        
        self.initialize_projects_list()
        
    
    def widgets(self):
        # Projects widgets        
        # - Projects
        self.lst_projects = QListWidget()        
        self.btn_add_project = QPushButton("Add Project")
        self.btn_rm_project = QPushButton("Remove Project")
        # - Sequences
        self.lst_sequences = QListWidget()
        self.btn_add_seq = QPushButton("Add Sequence")
        self.btn_rm_seq = QPushButton("Remove Seq")
        # - Shots
        self.lst_shots = QListWidget()
        self.btn_add_shot = QPushButton("Add Shot")
        self.btn_rm_shot = QPushButton("Remove Shot")
        self.btn_edit_shot = QPushButton("Edit Shot")
        # - DCC
        self.btn_houdini = QPushButton("Houdini")
        self.btn_nuke = QPushButton("Nuke")
        # - General stuff
        self.lbl_project_path = QLabel("Project Path")
        self.lbl_project_path.setText("..")
        self.lbl_project_fps = QLabel()
        self.lbl_project_fps.setText("..")
        self.lbl_project_resolution = QLabel()
        self.lbl_project_resolution.setText("..")
        
        # Files Widgets
        self.btn_rename_files = QPushButton("Rename")
        self.btn_renumber_files = QPushButton("Renumber")
        self.btn_fix_padding = QPushButton("Fix Padding")
        
        
        # Template Widgets
        self.cmb_dcc = QComboBox()
        self.cmb_dcc.addItems(["Houdini", "Nuke"])
        self.lst_template = QListWidget()  
        self.ln_run = QLineEdit()          
        
        # Final tab widget
        self.tab_main = QTabWidget()
        
    
    def layouts(self):
        self.wdg_projects = QWidget()
        self.wdg_files = QWidget()
        self.wdg_templates = QWidget()
        
        ###### STUFF RELATED TO THE PROJECTS TAB ###############################
        self.lyt_projects = QVBoxLayout()
        self.lyt_sequences = QVBoxLayout()
        self.lyt_shots = QVBoxLayout()
        self.lyt_dcc = QVBoxLayout()        
        
        self.lyt_main_projects_h = QHBoxLayout()
        self.lyt_main_projects_h.addLayout(self.lyt_projects)
        self.lyt_main_projects_h.addLayout(self.lyt_sequences)
        self.lyt_main_projects_h.addLayout(self.lyt_shots)
        self.lyt_main_projects_h.addLayout(self.lyt_dcc)
        
        self.lbl_path = QFormLayout()
        self.lbl_path.addRow("Path: ", self.lbl_project_path)  
        self.lbl_path.addRow("FPS: ", self.lbl_project_fps)      
        self.lbl_path.addRow("Resolution: ", self.lbl_project_resolution) 
        self.lbl_path.setLabelAlignment(Qt.AlignRight)
        
        self.lyt_projects.addWidget(self.lst_projects)
        self.lyt_projects.addWidget(self.btn_add_project)
        self.lyt_projects.addWidget(self.btn_rm_project)
        
        self.lyt_sequences.addWidget(self.lst_sequences)
        self.lyt_sequences.addWidget(self.btn_add_seq)
        self.lyt_sequences.addWidget(self.btn_rm_seq)
        
        self.lyt_shots.addWidget(self.lst_shots)
        self.lyt_shots.addWidget(self.btn_add_shot)
        self.lyt_shots.addWidget(self.btn_rm_shot)
        self.lyt_shots.addWidget(self.btn_edit_shot)
        
        self.lyt_dcc.addWidget(self.btn_houdini)
        self.lyt_dcc.addWidget(self.btn_nuke)
        self.lyt_dcc.addStretch()
        
        self.lyt_main_projects_v = QVBoxLayout()
        self.lyt_main_projects_v.addLayout(self.lyt_main_projects_h)
        self.lyt_main_projects_v.addLayout(self.lbl_path)        
                                
        
        ###### STUFF RELATED TO THE FILES #########################
        self.lyt_files = QHBoxLayout()
        self.lyt_files.addWidget(self.btn_rename_files)
        self.lyt_files.addWidget(self.btn_renumber_files)
        self.lyt_files.addWidget(self.btn_fix_padding)        
        
        
        ###### STUFF RELATED TO THE TEMPLATES
        self.lyt_templates_h = QHBoxLayout()
        self.lyt_templates_v = QVBoxLayout()     
        self.form_dcc = QFormLayout()        
                       
        self.form_dcc.addRow("Output houdini", self.ln_run)        
        
        self.lyt_templates_v.addWidget(self.cmb_dcc)
        self.lyt_templates_v.addWidget(self.lst_template)
        self.lyt_templates_v.addLayout(self.form_dcc)      
                
        self.lyt_templates_h.addLayout(self.lyt_templates_v)        
        
        
        ##### PUTTING IT ALL TOGETHER   
        self.wdg_projects.setLayout(self.lyt_main_projects_v)
        self.wdg_files.setLayout(self.lyt_files)
        self.wdg_templates.setLayout(self.lyt_templates_h)
        
        self.tab_main.addTab(self.wdg_projects, "Projects")
        self.tab_main.addTab(self.wdg_files, "File Utils")
        self.tab_main.addTab(self.wdg_templates, "Templates")
        
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.tab_main)     
        self.setLayout(self.main_layout)
        
        
        
    def connections(self):
        self.btn_add_project.clicked.connect(self.add_project)
        self.lst_projects.itemClicked.connect(self.get_project)        
        self.btn_rm_project.clicked.connect(self.delete_project)
        
        
        self.lst_sequences.itemClicked.connect(self.get_sequence)
        self.btn_add_seq.clicked.connect(self.add_sequence)
        self.btn_rm_seq.clicked.connect(self.delete_sequence)
    
    
    def initialize_projects_list(self):
        all_projects =  pr.Projects().get_all_project_names() 
        self.lst_projects.clear()
        self.lst_projects.addItems(all_projects)     
        self.lst_projects.setCurrentRow(0)            

    
    def update_sequences_list(self):
        all_sequences = sq.Sequences(self._project).get_sequences_names()
        self.lst_sequences.clear()
        self.lst_sequences.addItems(all_sequences)        
    
    
    def update_shots_list(self):
        pass
        
    
    def add_project(self):
        lg.Logger.info("Adding project")
        new_project_window = new_ui.PPM_NewProject()
        result = new_project_window.exec_()
        
        if result == QtWidgets.QDialog.Accepted:
            self._project_name = new_project_window.return_name()
            self._project_fps = new_project_window.return_fps()
            self._project_resolution = new_project_window.return_resolution()
            
            self.lbl_project_path.setText(self._project_name)            
            self.lbl_project_fps.setText(self._project_fps)            
            self.lbl_project_resolution.setText(self._project_resolution)
            
            logic.create_new_project(self._project_name, int(self._project_fps), self._project_resolution)
            self.initialize_projects_list()
            
            
    def get_project(self, t):
        project_name = t.text()
        project = logic.get_project(project_name)      
        
        self._project_name = str(project.get_name())
        self._project_path = project.get_path()
        self._project_fps = str(project.get_fps()) 
        self._project_resolution = str(project.get_resolution())
        
        self.lbl_project_path.setText(str(project.get_path()) )
        self.lbl_project_fps.setText(str(project.get_fps()) )
        self.lbl_project_resolution.setText(str(project.get_resolution()))
        
        self._project = project
        
        self.update_sequences_list()
        self.lst_sequences.setCurrentRow(0)
        
        return project
            
        
    def delete_project(self):    
        name = self._project_name               
        
        if not self._project_name:
            QMessageBox.warning(self, "Warning", "Select a project.")    
            return
        res = QMessageBox.question(self, "Warning", "Are you sure that you want to delete this project? ")
        if res == QMessageBox.Yes:
            print(self._project_name)
            logic.delete_project(name)           
            
        self.initialize_projects_list()
        
        
        
    def add_sequence(self):
        lg.Logger.info("Adding Sequence")
        new_sequence_window = new_ui_seq.PPM_New_Sequence()
        result = new_sequence_window.exec_()
        
        if result == QtWidgets.QDialog.Accepted:
            self._sequence_name = new_sequence_window.return_name()     
            self._sequence_path = os.path.join(self._project_name, self._sequence_name)
            self.lbl_project_path.setText(self._sequence_path)        

            logic.create_new_sequence(self._project, self._sequence_name)
            self.update_sequences_list()
        
        print(self._sequence_name) 
        
        
    def get_sequence(self, t):
        sequence_name = t.text()
        
        sequence = logic.get_sequence(self._project, sequence_name)      
        
        self._sequence_name = str(sequence.get_name())
        self._sequence_path = os.path.join(self._project_path, self._sequence_name)
        self.lbl_project_path.setText(self._sequence_path)

        
        self._sequence = sequence      

        return sequence
    
    
    def delete_sequence(self):
        sequence_name = self._sequence_name               
        
        if not self._sequence_name:
            QMessageBox.warning(self, "Warning", "Select a sequence.")    
            return
        res = QMessageBox.question(self, "Warning", "Are you sure that you want to delete this sequence? ")
        if res == QMessageBox.Yes:            
            logic.delete_sequence(self._project, sequence_name)           
            
        self.update_sequences_list()
              


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    #app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    dark_palette = QtGui.QPalette()
    Palette(dark_palette)
    app.setPalette(dark_palette)
    
    w = PPM_Main_UI()
    w.show()
    
    sys.exit(app.exec_())

