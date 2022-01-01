from PySide2.QtWidgets import QApplication, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout
import sys


class PPM_New_Sequence(QDialog):
    def __init__(self):
        super(PPM_New_Sequence, self).__init__()
        self.setWindowTitle("ADD NEW SEQUENCE")         
        self.setMaximumSize(300,500)
        
        self.widgets()
        self.layouts()
        self.connections()    
    
        
    def widgets(self):
        self.ln_seq_name = QLineEdit()
        self.btn_create_seq = QPushButton("Create")
        self.btn_create_seq.setEnabled(False)
        self.btn_cancel = QPushButton("cancel")
    
    
    def layouts(self):
        self.seq_main_layout = QVBoxLayout()
        self.seq_form_layout = QFormLayout()
        self.lyt_button = QHBoxLayout()
        self.lyt_button.addStretch()
        self.lyt_button.addWidget(self.btn_create_seq)
        self.lyt_button.addWidget(self.btn_cancel)
        self.seq_form_layout.addRow("Sequence Name: ", self.ln_seq_name)
        self.seq_main_layout.addLayout(self.seq_form_layout)
        self.seq_main_layout.addLayout(self.lyt_button)
        self.seq_main_layout.addStretch()
        
        self.setLayout(self.seq_main_layout)
    
    
    def connections(self):
        self.ln_seq_name.textChanged.connect(self.check_name)
        self.btn_cancel.clicked.connect(self.close)
        self.btn_create_seq.clicked.connect(self.accept)
        
        
    def check_name(self):
        if self.ln_seq_name.text():
            if not self.ln_seq_name.text()[0].isdigit():
                self.btn_create_seq.setEnabled(True)
        else:
            self.btn_create_seq.setEnabled(False)
            
        
    def return_name(self):
        return self.ln_seq_name.text()
    
    
    
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PPM_New_Sequence()
    w.show()
    sys.exit(app.exec_())