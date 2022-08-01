from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSpinBox, QVBoxLayout, QHBoxLayout, QWidget
from PySide2.QtCore import Qt
import sys


__all__ = ["PPM_NewProject"]

FPS_LIST = ["12", "24", "25", "30", "60", "120"]
RESOLUTION_LIST = ["7680 x 4320", "3840 x 2160", "1920 x 1080", "640 x 480"]


class PPM_EditShot(QDialog):
    def __init__(self, old_first_frame, old_last_frame):
        super(PPM_EditShot, self).__init__()
        self.setWindowTitle("EDIT SHOT")       
        self.setMinimumSize(350, 200) 
        self.widgets()
        self.layouts()
        self.connections()
        self._old_first_frame = old_first_frame
        self._old_last_frame = old_last_frame
        
        self.set_labels()
        
        
    def widgets(self):        
        self.lb_shot_name = QLabel("Shot name: ")
        self.cmb_firstFrame = QSpinBox()   
        self.cmb_firstFrame.setMaximum(10000)
        self.cmb_firstFrame.setValue(1001)
        self.cmb_lastFrame = QSpinBox()
        self.cmb_lastFrame.setMaximum(10000)
        self.cmb_lastFrame.setValue(1100)
        self.btn_create = QPushButton("Accept")         
        self.btn_cancel = QPushButton("Cancel")
        self.spinners = QWidget()     
        
        self.old_info = QWidget()    
        self.lb_old_start = QLabel("test")  
        self.lb_old_end = QLabel("test") 


    
    def layouts(self):        
        self.form_old = QFormLayout()
        self.form_old.addRow("Old Start", self.lb_old_start)
        self.form_old.addRow("Old End", self.lb_old_end)
        
        self.lyt_v_main = QVBoxLayout()
        self.lyt_h_main = QHBoxLayout()
        self.form_main = QFormLayout()       
        self.form_main.addRow("First Frame:", self.cmb_firstFrame)
        self.form_main.addRow("Last Frame:", self.cmb_lastFrame)
        self.form_main.setLabelAlignment(Qt.AlignRight)
        self.lyt_h_main.addStretch()
        self.lyt_h_main.addWidget(self.btn_create)    
        self.lyt_h_main.addWidget(self.btn_cancel)  
        
        self.lyt_v_main.addWidget(self.lb_shot_name)   
        self.lyt_v_main.addStretch()      
        
        self.old_info.setLayout(self.form_old)  
        self.lyt_v_main.addWidget(self.old_info)  
          
        self.spinners.setLayout(self.form_main)  
        self.lyt_v_main.addWidget(self.spinners)          
      
        
        self.lyt_v_main.addLayout(self.lyt_h_main)        
        self.lyt_v_main.addStretch()
        
        self.setLayout(self.lyt_v_main)
    
    
    def connections(self):               
        self.btn_create.clicked.connect(self.accept)        
        self.btn_cancel.clicked.connect(self.close)             

        
    def get_name(self):
        value = str(self.ln_shot_name.text())
        fixed_value = value.zfill(4)
        return fixed_value
    
    
    def return_first_frame(self):        
        return self.cmb_firstFrame.text()
    
    
    def return_last_frame(self):
        return self.cmb_lastFrame.text()
    
    
    def set_labels(self):
        self.lb_old_start.setText(self._old_first_frame)
        self.lb_old_end.setText(self._old_last_frame)
    
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PPM_EditShot("800", "900")
    w.show()
    
    sys.exit(app.exec_())