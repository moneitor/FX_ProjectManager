from Qt.QtWidgets import QMainWindow, QApplication
import sys



class myWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Config")
        
app = QApplication(sys.argv)
window = myWindow()
window.show()

app.exec_()
        