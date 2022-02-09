"""
Main hub from where most of the PPM applications are run, it is divided in three
main segments.
    
Project creation, File Utils and Templates.
    
moduleauthor::Hernan Llano <hernan@3d.gmail.com>   
"""



from PySide2 import QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QTabWidget, QVBoxLayout, QWidget
import ppm_main_logic as logic
import sys
import ppm_logger.logger as lg
from PySide2.QtCore import Qt
from entity import project as pr
from entity import sequence as sq
from entity import shot as s
from ui.palette import Palette


import ppm_new_project_ui as new_ui
import ppm_new_seq_ui as new_ui_seq
import ppm_new_shot_ui as new_ui_shot

from houdini_startup import hou_run

from files import renamer

import os


class PPM_Main_UI(QDialog):
    def __init__(self):
        super(PPM_Main_UI, self).__init__()       

        self.setWindowTitle("PROJECT MANAGER")
        self.setMinimumWidth(1060)
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
        self._shot_first_frame = ""
        self._shot_last_frame = ""
        self._common = ""
        
        self._project_path = "" 
        
        self.widgets()
        self.layouts()
        self.connections()
        
        self.initialize_projects_list()
        
    
    def widgets(self):
        # Projects widgets        
        # - Projects
        self.lbl_projects = QLabel("Projects:")
        self.lst_projects = QListWidget()        
        self.btn_add_project = QPushButton("Add Project")
        self.btn_rm_project = QPushButton("Remove Project")
        
        # - Sequences
        self.lbl_sequences = QLabel("Sequences:")
        self.lst_sequences = QListWidget()
        self.btn_add_seq = QPushButton("Add Sequence")
        self.btn_add_seq.setEnabled(False)
        #self.btn_add_seq.setStyleSheet("background-color: rgb(100,100,100)")
        self.btn_rm_seq = QPushButton("Remove Seq")
        self.btn_rm_seq.setEnabled(False)
        #self.btn_rm_seq.setStyleSheet("background-color: rgb(100,100,100)")
        
        # - Shots
        self.lbl_shots = QLabel("Shots:")
        self.lst_shots = QListWidget()
        self.btn_add_shot = QPushButton("Add Shot")
        self.btn_add_shot.setEnabled(False)
        #self.btn_add_shot.setStyleSheet("background-color: rgb(100,100,100)")
        self.btn_rm_shot = QPushButton("Remove Shot")
        self.btn_rm_shot.setEnabled(False)
        #self.btn_rm_shot.setStyleSheet("background-color: rgb(100,100,100)")
        self.btn_edit_shot = QPushButton("Edit Shot")
        self.btn_edit_shot.setEnabled(False)
        #self.btn_edit_shot.setStyleSheet("background-color: rgb(100,100,100)")
        
        # - DCC        
        self.btn_houdini = QPushButton("Houdini")
        self.btn_houdini.setEnabled(False)
        #self.btn_houdini.setStyleSheet("background-color: rgb(100,100,100)")
        self.btn_nuke = QPushButton("Nuke")
        self.btn_nuke.setEnabled(False)
        #self.btn_nuke.setStyleSheet("background-color: rgb(100,100,100)")       
        
        # Assets widgets
        self.btn_search_file = QPushButton("Search for file")
        self.ln_file_path = QLineEdit()
        self.btn_cg_add_abc = QPushButton("Add Alembic")  
        self.btn_cg_add_obj = QPushButton("Add OBJ")  
        self.btn_cg_add_fbx = QPushButton("Add FBX") 
        self.ln_asset_name = QLineEdit()
        self.ln_asset_name.setPlaceholderText("Write asset name")
        
        # - General stuff
        self.lbl_project_path = QLabel("Project Path")
        self.lbl_project_path.setText("..")
        #self.lbl_project_path.setStyleSheet("background-color: black: border: 1px solid black;")
        
        self.lbl_project_fps = QLabel()
        self.lbl_project_fps.setText("..")
        #self.lbl_project_fps.setStyleSheet("background-color: black: border: 1px solid black;")
        
        self.lbl_project_resolution = QLabel()
        self.lbl_project_resolution.setText("..")
        
        self.lbl_shot_first_frame = QLabel()
        self.lbl_shot_first_frame.setText("..")
        
        self.lbl_shot_last_frame = QLabel()
        self.lbl_shot_last_frame.setText("..")       
                           
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
        self.wdg_assets = QWidget()
        
        ###### STUFF RELATED TO THE PROJECTS TAB ###############################
        self.lyt_projects = QVBoxLayout()
        self.lyt_sequences = QVBoxLayout()
        self.lyt_shots = QVBoxLayout()
        self.lyt_dcc = QVBoxLayout()  
        self.lyt_assets = QVBoxLayout()
        
        self.dcc_grp = QGroupBox("Software")        
        self.dcc_v_layout = QVBoxLayout()
        self.dcc_v_layout.addWidget(self.btn_houdini)
        self.dcc_v_layout.addWidget(self.btn_nuke)
        self.dcc_grp.setLayout(self.dcc_v_layout)              
        
        self.lyt_main_projects_h = QHBoxLayout()
        self.lyt_main_projects_h.addLayout(self.lyt_projects)
        self.lyt_main_projects_h.addLayout(self.lyt_sequences)
        self.lyt_main_projects_h.addLayout(self.lyt_shots)
        self.lyt_main_projects_h.addLayout(self.lyt_dcc)
        
        self.grp_info = QGroupBox("General Information")
        self.lbl_path = QFormLayout()
        self.lbl_path.addRow("Path -> ", self.lbl_project_path)  
        self.lbl_path.addRow("FPS -> ", self.lbl_project_fps)      
        self.lbl_path.addRow("Resolution -> ", self.lbl_project_resolution) 
        self.lbl_path.addRow("Shot First Frame -> ", self.lbl_shot_first_frame)
        self.lbl_path.addRow("Shot Last Frame -> ", self.lbl_shot_last_frame)        
        self.lbl_path.setLabelAlignment(Qt.AlignRight)
        self.grp_info.setLayout(self.lbl_path)
        
        self.lyt_projects.addWidget(self.lbl_projects)
        self.lyt_projects.addWidget(self.lst_projects)
        self.lyt_projects.addWidget(self.btn_add_project)
        self.lyt_projects.addWidget(self.btn_rm_project)
        
        self.lyt_sequences.addWidget(self.lbl_sequences)
        self.lyt_sequences.addWidget(self.lst_sequences)
        self.lyt_sequences.addWidget(self.btn_add_seq)
        self.lyt_sequences.addWidget(self.btn_rm_seq)
        
        self.lyt_shots.addWidget(self.lbl_shots)
        self.lyt_shots.addWidget(self.lst_shots)
        self.lyt_shots.addWidget(self.btn_add_shot)
        self.lyt_shots.addWidget(self.btn_rm_shot)
        self.lyt_shots.addWidget(self.btn_edit_shot)        
        
        self.lyt_dcc.addWidget(self.dcc_grp)
        self.lyt_dcc.addStretch()
        
        self.lyt_main_projects_v = QVBoxLayout()
        self.lyt_main_projects_v.addLayout(self.lyt_main_projects_h)
        self.lyt_main_projects_v.addWidget(self.grp_info)   
           
        
        ##### STUFF RELATED TO ASSETS
        self.lyt_h_asset_file = QHBoxLayout()
        self.lyt_h_cg_buttons = QHBoxLayout()
        self.grp_cg_buttons = QGroupBox("CG Assets")
        self.lyt_h_asset_file.addWidget(self.btn_search_file)
        self.lyt_h_asset_file.addWidget(self.ln_file_path) 
        self.lyt_assets.addLayout(self.lyt_h_asset_file)
        
        self.lyt_h_cg_buttons.addWidget(self.btn_cg_add_abc)
        self.lyt_h_cg_buttons.addWidget(self.btn_cg_add_obj)
        self.lyt_h_cg_buttons.addWidget(self.btn_cg_add_fbx)
        
        self.grp_cg_buttons.setLayout(self.lyt_h_cg_buttons)
        
        self.lyt_assets.addWidget(self.grp_cg_buttons)    
        self.lyt_assets.addWidget(self.ln_asset_name)
        self.lyt_assets.addStretch()      
                                        
        
        ###### STUFF RELATED TO THE FILES #########################
        self.lyt_files = QVBoxLayout()
        self.lyt_files.addWidget(self.btn_rename_files)
        self.lyt_files.addWidget(self.btn_renumber_files)
        self.lyt_files.addWidget(self.btn_fix_padding)       
        self.lyt_files.addStretch() 
        
        
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
        self.wdg_assets.setLayout(self.lyt_assets)
        self.wdg_files.setLayout(self.lyt_files)
        self.wdg_templates.setLayout(self.lyt_templates_h)        
        
        self.tab_main.addTab(self.wdg_projects, "Projects")
        self.tab_main.addTab(self.wdg_assets, "Assets")
        self.tab_main.addTab(self.wdg_files, "File Utils")
        self.tab_main.addTab(self.wdg_templates, "Templates")        
        
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.tab_main)     
        self.setLayout(self.main_layout)
        
        
        
    def connections(self):
        self.btn_add_project.clicked.connect(self.add_project)
        self.lst_projects.itemClicked.connect(self.get_project)   
        self.lst_projects.itemClicked.connect(self.get_common_folder)     
        self.btn_rm_project.clicked.connect(self.delete_project)
        
        self.btn_add_seq.clicked.connect(self.add_sequence)
        self.lst_sequences.itemClicked.connect(self.get_sequence)        
        self.btn_rm_seq.clicked.connect(self.delete_sequence)
        
        self.btn_add_shot.clicked.connect(self.add_shot)
        self.lst_shots.itemClicked.connect(self.get_shot)        
        self.btn_rm_shot.clicked.connect(self.delete_shot)
        
        self.btn_houdini.clicked.connect(self.hou_run)
        
        self.btn_rename_files.clicked.connect(self.run_renamer)
    
    
    def initialize_projects_list(self):
        all_projects =  pr.Projects().get_all_project_names() 
        self.lst_projects.clear()
        self.lst_projects.addItems(all_projects)    
        self.lst_projects.sortItems()
                   

    
    def update_sequences_list(self):
        all_sequences = sq.Sequences(self._project).get_sequences_names()
        self.lst_sequences.clear()
        self.lst_sequences.addItems(all_sequences)        
        self.lst_sequences.sortItems()
    
    
    
    def update_shots_list(self):
        all_shots = s.Shots(self._sequence).get_shot_names()
        self.lst_shots.clear()
        self.lst_shots.addItems(all_shots)
        self.lst_shots.sortItems()
        
        
    
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
            self.lst_sequences.clear()
            self.lst_shots.clear()
            
            
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
        
        self.btn_add_seq.setEnabled(True)
        #self.btn_add_seq.setStyleSheet("background-color: rgb(45,45,45)")        
        self.btn_rm_seq.setEnabled(True)
        #self.btn_rm_seq.setStyleSheet("background-color: rgb(45,45,45)")     
        
        self._project = project
        
        try:
            self.update_sequences_list()   
            self.update_shots_list()   
            self.lst_shots.clear()  
        except:
            lg.Logger.info("No sequences or shots created yet")
        
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
        self.lst_sequences.clear()
        self.lst_shots.clear()
        
        
        
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
        
        self.btn_add_shot.setEnabled(True)
        #self.btn_add_shot.setStyleSheet("background-color: rgb(45,45,45)")        
        self.btn_rm_shot.setEnabled(True)
        #self.btn_rm_shot.setStyleSheet("background-color: rgb(45,45,45)")        
        self.btn_edit_shot.setEnabled(True)
        #self.btn_edit_shot.setStyleSheet("background-color: rgb(45,45,45)")
        
        self.update_shots_list()        

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
        self.lst_shots.clear()
        
        
    def add_shot(self):
        lg.Logger.info("Adding Shot")
        new_shot_window = new_ui_shot.PPM_NewProject()
        result = new_shot_window.exec_()
        
        if result == QtWidgets.QDialog.Accepted:
            self._shot_name = self._sequence_name + "_" + new_shot_window.return_name()     
            self._shot_path = os.path.join(self._sequence_name, self._shot_name)
            self.lbl_project_path.setText(self._shot_path)     
            self._shot_first_frame = new_shot_window.return_first_frame()  
            self._shot_last_frame = new_shot_window.return_last_frame()  

            create_new_shot = logic.create_new_shot(self._sequence, self._shot_name, self._shot_first_frame, self._shot_last_frame)
            if create_new_shot == False:
                QMessageBox.warning(self, "Warning", "Shot Already Exists.")
            self.update_shots_list()
        
        print(self._sequence_name)
    
    
    def get_shot(self, t):
        shot_name = t.text()
        shot_name = shot_name.split("_")[-1]
        
        shot = logic.get_shot(self._sequence, shot_name)      
        
        self._shot_name = self._sequence_name + "_" + str(shot.get_name())
        self._shot_path = os.path.join(self._sequence_path, self._shot_name)        
        self._shot_first_frame = str(logic.get_shot_first_frame(self._sequence, self._shot_name))
        self._shot_last_frame = str(logic.get_shot_last_frame(self._sequence, self._shot_name))
        
        self.lbl_project_path.setText(self._shot_path)
        self.lbl_shot_first_frame.setText(self._shot_first_frame)
        self.lbl_shot_last_frame.setText(self._shot_last_frame)
        
        self.btn_houdini.setEnabled(True)
        #self.btn_houdini.setStyleSheet("background-color: rgb(45,45,45)")        
        self.btn_nuke.setEnabled(True)
        #self.btn_nuke.setStyleSheet("background-color: rgb(45,45,45)")
        
            
                  
        self._shot = shot       
               
        return shot
    
    
    def delete_shot(self):
        shot_name = self._shot_name               
        
        if not self._shot_name:
            QMessageBox.warning(self, "Warning", "Select a shot.")    
            return
        res = QMessageBox.question(self, "Warning", "Are you sure that you want to delete this shot? ")
        if res == QMessageBox.Yes:            
            logic.delete_shot(self._sequence, shot_name)           
            
        self.update_shots_list()
        
        
    def get_common_folder(self):
        """ 
        This saves the path to the common folder, where houdini and nuke can look for scripts within the project.
        """
        self._common = os.path.join(self._project_path, "common")
        
        
        
    def hou_run(self):
        lg.Logger.info("Running houdini")
        hou_run(fps=int(self._project_fps),
                resx=int(self._project_resolution.split("x")[0].strip()), 
                resy= int(self._project_resolution.split("x")[-1].strip()), 
                job=self._shot_path, 
                first_frame=int(self._shot_first_frame),
                last_frame=int(self._shot_last_frame),
                shot_path = self._shot_path,
                project_path = self._project_path,
                common=self._common)
        
        
        
    ######################### FILE UTILITIES ############################################################
    
    def run_renamer(self):
        renamer_window = renamer.Renamer()
        renamer_window.exec_()
              


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    #dark_palette = QtGui.QPalette()
    #Palette(dark_palette)
    #app.setPalette(dark_palette)
    
    w = PPM_Main_UI()
    w.show()
    
    sys.exit(app.exec_())

