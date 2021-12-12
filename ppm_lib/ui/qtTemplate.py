import sys
import os

from PySide2 import QtUiTools, QtWidgets
from PySide2 import QtCore

class YourWindow(QtWidgets.QWidget):
    def __init__(self):
        super(YourWindow, self).__init__()
        
        file_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(file_path, "ui", "ppm_main.ui")
        ui_file = "./ui/ppm_main.ui"
        if os.path.exists(ui_file):
            print("yeaaaah")
        else:
            print("noooooo")
            
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        
        self.ui.btn_new_project.clicked.connect(self.test)
        
    def test(self):
        print("pacooooooo")
        


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication([])
    win = YourWindow()
    win.show()    
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    file_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(file_path, "ui", "ppm_main.ui")
    #main()
    
    print(file_path)