from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSpinBox, QVBoxLayout, QHBoxLayout, QWidget
from PySide2.QtCore import Qt
import sys


__all__ = ["PPM_NewProject"]

FPS_LIST = ["12", "24", "25", "30", "60", "120"]
RESOLUTION_LIST = ["7680 x 4320", "3840 x 2160", "1920 x 1080", "640 x 480"]


class PPM_NewProject(QDialog):
    def __init__(self):
        super(PPM_NewProject, self).__init__()
        self.setWindowTitle("ADD NEW SHOT")       
        self.setMinimumSize(350, 200) 
        self.widgets()
        self.layouts()
        self.connections()
        
        
    def widgets(self):        
        self.ln_shot_name = QLineEdit()
        self.ln_shot_name.setPlaceholderText("Write shot name here...")
        self.cmb_firstFrame = QSpinBox()   
        self.cmb_firstFrame.setMaximum(10000)
        self.cmb_firstFrame.setValue(1001)
        self.cmb_lastFrame = QSpinBox()
        self.cmb_lastFrame.setMaximum(10000)
        self.cmb_lastFrame.setValue(1100)
        self.btn_create = QPushButton("Create")   
        self.btn_create.setEnabled(False)
        self.btn_cancel = QPushButton("Cancel")
        self.qwidget1 = QWidget()           

    
    def layouts(self):        
        self.lyt_v_main = QVBoxLayout()
        self.lyt_h_main = QHBoxLayout()
        self.form_main = QFormLayout()
        self.form_main.addRow("Shot Name:", self.ln_shot_name)
        self.form_main.addRow("First Frame:", self.cmb_firstFrame)
        self.form_main.addRow("Last Frame:", self.cmb_lastFrame)
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
        self.ln_shot_name.textChanged.connect(self.check_name)       
        self.btn_create.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.close)      
        
        
        
    def check_name(self):
        if self.ln_shot_name.text():            
            self.btn_create.setEnabled(True)
        else:
            self.btn_create.setEnabled(False)      

        
        
    def return_name(self):        
        return self.ln_shot_name.text()
    
    
    def return_first_frame(self):        
        return self.cmb_firstFrame.text()
    
    
    def return_last_frame(self):
        return self.cmb_lastFrame.text()
    
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PPM_NewProject()
    w.show()
    
    sys.exit(app.exec_())