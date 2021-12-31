from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide2.QtCore import Qt
import sys


__all__ = ["PPM_NewProject"]

FPS_LIST = ["12", "24", "25", "30", "60", "120"]
RESOLUTION_LIST = ["7680 x 4320", "3840 x 2160", "1920 x 1080", "640 x 480"]


class PPM_NewProject(QDialog):
    def __init__(self):
        super(PPM_NewProject, self).__init__()
        self.setWindowTitle("ADD NEW PROJECT")       
        self.setMinimumSize(350, 200) 
        self.widgets()
        self.layouts()
        self.connections()
        
        
    def widgets(self):        
        self.ln_project_name = QLineEdit()
        self.ln_project_name.setPlaceholderText("Write project name here...")
        self.cmb_fps = QComboBox()
        self.cmb_fps.addItems(FPS_LIST)
        self.cmb_fps.setCurrentIndex(1)
        
        self.cmb_resolution = QComboBox()
        self.cmb_resolution.addItems(RESOLUTION_LIST)
        self.cmb_resolution.setCurrentIndex(2)
                
        self.btn_create = QPushButton("Create")   
        self.btn_cancel = QPushButton("Cancel")
        self.qwidget1 = QWidget()           

    
    def layouts(self):        
        self.lyt_v_main = QVBoxLayout()
        self.lyt_h_main = QHBoxLayout()
        self.form_main = QFormLayout()
        self.form_main.addRow("Project Name:", self.ln_project_name)
        self.form_main.addRow("FPS:", self.cmb_fps)
        self.form_main.addRow("Resolution:", self.cmb_resolution)
        self.form_main.setLabelAlignment(Qt.AlignRight)
        self.lyt_h_main.addStretch()
        self.lyt_h_main.addWidget(self.btn_create)    
        self.lyt_h_main.addWidget(self.btn_cancel)           
          
        self.qwidget1.setLayout(self.form_main)  
        self.lyt_v_main.addWidget(self.qwidget1)           
        
        self.lyt_v_main.addLayout(self.lyt_h_main)        
        self.lyt_v_main.addStretch()
        
        self.setLayout(self.lyt_v_main)
    
    
    def connections(self):        
        self.btn_create.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.close)       
        # TODO fix the accepting problem so it checks for an empty name 
        
        
    def check_valid_name(self):
        if not self.ln_project_name.text():
            QMessageBox.warning(self, "Warning", "Please add a project name.")
        else:
            self.btn_create.clicked.connect(self.accept)
        
        
    def return_name(self):        
        return self.ln_project_name.text()
    
    
    def return_fps(self):        
        return self.cmb_fps.currentText()
    
    
    def return_resolution(self):
        return self.cmb_resolution.currentText()
    
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PPM_NewProject()
    w.show()
    
    sys.exit(app.exec_())