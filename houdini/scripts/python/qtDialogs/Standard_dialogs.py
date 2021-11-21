import hou
import os

from file_scripts import palette
from PySide2 import QtCore, QtWidgets, QtGui

parentHou = hou.ui.mainQtWindow()



class StandardDialogs(QtWidgets.QWidget):
    def __init__(self, parent=parentHou):
        super(StandardDialogs, self).__init__()
        
        self.setWindowTitle("Standard Qt Dialogs")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)    

        self.prefs_directory = os.environ.get("PROJECT_PATH")    

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        

    def create_widgets(self):
        self.get_color_btn = QtWidgets.QPushButton("getColor")
        self.get_existing_dir_btn = QtWidgets.QPushButton("getExistingDirectory")
        self.get_open_file_name_btn = QtWidgets.QPushButton("getOpenFileName")
        self.get_open_file_names_btn = QtWidgets.QPushButton("getOpenFileNames")
        self.get_save_file_name_btn = QtWidgets.QPushButton("getSaveFileName")
        self.get_font_btn = QtWidgets.QPushButton("getFont")
        self.get_double_btn = QtWidgets.QPushButton("getDouble")
        self.get_int_btn = QtWidgets.QPushButton("getInt")
        self.get_text_btn = QtWidgets.QPushButton("getText")
        self.get_multi_line_text_btn = QtWidgets.QPushButton("getMultiLineText")
        self.critical_btn = QtWidgets.QPushButton("critical")
        self.warning_btn = QtWidgets.QPushButton("warning")
        self.information_btn = QtWidgets.QPushButton("information")
        self.question_btn = QtWidgets.QPushButton("question")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        grp_layout = QtWidgets.QHBoxLayout()
        grp_layout.addWidget(self.get_existing_dir_btn)
        grp_layout.addWidget(self.get_open_file_name_btn)
        grp_layout.addWidget(self.get_open_file_names_btn)
        grp_layout.addWidget(self.get_save_file_name_btn)
        grp_layout.addStretch()
        grp = QtWidgets.QGroupBox("QFileDialog")
        grp.setLayout(grp_layout)
        main_layout.addWidget(grp)

        grp_layout = QtWidgets.QHBoxLayout()
        grp_layout.addWidget(self.critical_btn)
        grp_layout.addWidget(self.warning_btn)
        grp_layout.addWidget(self.information_btn)
        grp_layout.addWidget(self.question_btn)
        grp_layout.addStretch()
        grp = QtWidgets.QGroupBox("QMessageBox")
        grp.setLayout(grp_layout)
        main_layout.addWidget(grp)

        grp_layout = QtWidgets.QHBoxLayout()
        grp_layout.addWidget(self.get_double_btn)
        grp_layout.addWidget(self.get_int_btn)
        grp_layout.addWidget(self.get_text_btn)
        grp_layout.addWidget(self.get_multi_line_text_btn)
        grp_layout.addStretch()
        grp = QtWidgets.QGroupBox("QInputDialog")
        grp.setLayout(grp_layout)
        main_layout.addWidget(grp)

        grp_layout = QtWidgets.QHBoxLayout()
        grp_layout.addWidget(self.get_color_btn)
        grp_layout.addStretch()
        grp = QtWidgets.QGroupBox("QColorDialog")
        grp.setLayout(grp_layout)
        main_layout.addWidget(grp)

        grp_layout = QtWidgets.QHBoxLayout()
        grp_layout.addWidget(self.get_font_btn)
        grp_layout.addStretch()
        grp = QtWidgets.QGroupBox("QFontDialog")
        grp.setLayout(grp_layout)
        main_layout.addWidget(grp)

        main_layout.addStretch()

    def create_connections(self):
        self.get_existing_dir_btn.clicked.connect(self.get_existing_directory)
        self.get_open_file_name_btn.clicked.connect(self.get_open_file_name)
        self.get_open_file_names_btn.clicked.connect(self.get_open_file_names)
        self.get_save_file_name_btn.clicked.connect(self.get_save_file_name)

        self.critical_btn.clicked.connect(self.critical)
        self.warning_btn.clicked.connect(self.warning_)
        self.information_btn.clicked.connect(self.information)
        self.question_btn.clicked.connect(self.question)

        self.get_double_btn.clicked.connect(self.get_double)
        self.get_int_btn.clicked.connect(self.get_int)
        self.get_text_btn.clicked.connect(self.get_text)
        self.get_multi_line_text_btn.clicked.connect(self.get_multi_line_text)

        self.get_color_btn.clicked.connect(self.get_color)
        self.get_font_btn.clicked.connect(self.get_font)

    def get_existing_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", self.prefs_directory)
        if directory:
            print("Selected Directory: {0}".format(directory))

    def get_open_file_name(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", os.chdir(r"C:/_fxProjects/_projects"))
        if file_path:   
            print("File path: {0}".format(file_path))

    def get_open_file_names(self):
        file_paths, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", os.chdir(r"C:/_fxProjects/_projects"))
        for path in file_paths:
            print("File path: {0}".format(path))

    def get_save_file_name(self):
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", os.chdir(r"C:/_fxProjects/_projects"))
        if file_path:
            print("File path: {0}".format(file_path))

    def critical(self):
        QtWidgets.QMessageBox.critical(self, "Error", "There was an error somewhere.")

    def warning_(self):
        QtWidgets.QMessageBox.warning(self, "Warning", "Something odd just happened.")

    def information(self):
        QtWidgets.QMessageBox.information(self, "Info", "Task completed successfully.")

    def question(self):
        button_pressed = QtWidgets.QMessageBox.question(self, "Question", "Would you like to continue?")
        if button_pressed == QtWidgets.QMessageBox.Yes:
            print("Continuing...")
        else:
            print("Cancelled")

    def get_double(self):
        value, ok = QtWidgets.QInputDialog.getDouble(self, "Enter a Value", "Value:")
        if ok:
            print(value)

    def get_int(self):
        value, ok = QtWidgets.QInputDialog.getInt(self, "Enter a Value", "Value:")
        if ok:
            print(value)

    def get_text(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Enter Text", "Text:")
        if ok:
            print(text)

    def get_multi_line_text(self):
        text, ok = QtWidgets.QInputDialog.getMultiLineText(self, "Enter Text", "Text:")
        if ok:
            print(text)

    def get_color(self):
        color = QtWidgets.QColorDialog.getColor(parent=self)
        if color:
            print("Red:{0} Green:{1} Blue:{2}".format(color.red(), color.green(), color.blue()))

    def get_font(self):
        font, ok  = QtWidgets.QFontDialog.getFont(parent=self)
        if ok:
            print("Family: {0}  Point Size: {1}".format(font.family(), font.pointSize()))





def run_app():
    # check if the dialog already exist and delete it
    # so it opens a new one
    try:
        app.close()
        app.deleteLater()
    except:
        pass

    app = StandardDialogs()
    app.setParent(parentHou, QtCore.Qt.Window)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    dark_palette = QtGui.QPalette()
    palette.Palette(dark_palette)

    app.setPalette(dark_palette)
    app.show()