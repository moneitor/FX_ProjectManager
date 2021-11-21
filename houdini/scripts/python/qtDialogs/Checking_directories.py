import hou
import os

from file_scripts import palette
from PySide2 import QtCore, QtWidgets, QtGui

parentHou = hou.ui.mainQtWindow()



class TraversingDirectories(QtWidgets.QWidget):
    def __init__(self, parent=parentHou):
        super(TraversingDirectories, self).__init__(parent)

        self.__path = os.getenv("PROJECT_PATH")

        self.setWindowTitle("Check Directories")

        self.widgets()
        self.layout()
        self.connections()
        self.refresh_list()


    def widgets(self):
        self.path_label = QtWidgets.QLabel(self.__path)

        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderHidden(True)

        self.close_btn = QtWidgets.QPushButton("Close")

    def layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addWidget(self.path_label)
        main_layout.addWidget(self.tree_widget)
        main_layout.addLayout(button_layout)

    def connections(self):
        self.close_btn.clicked.connect(self.close)

    def refresh_list(self):
        self.tree_widget.clear()

        self.add_children(None, self.__path)

    def add_children(self, parent_item, dir_path):
        directory = QtCore.QDir(dir_path)
        nodots = QtCore.QDir.NoDotAndDotDot
        AllEntries = QtCore.QDir.AllEntries
        DirsFirst = QtCore.QDir.DirsFirst
        IgnoreCase = QtCore.QDir.IgnoreCase
        files = directory.entryList(nodots | AllEntries, DirsFirst | IgnoreCase)

        for fileName in files:
            self.add_child(parent_item, dir_path, fileName)

    def add_child(self, parent_item, dir_path, file_name):
        filePath = "{}/{}".format(dir_path, file_name)
        file_info = QtCore.QFileInfo(filePath)

        item = QtWidgets.QTreeWidgetItem(parent_item, [file_name])
        item.setData(0, QtCore.Qt.UserRole, filePath)

        if file_info.isDir():
            self.add_children(item, file_info.absoluteFilePath())

        if not parent_item:
            self.tree_widget.addTopLevelItem(item)




def run_app():
    # check if the dialog already exist and delete it
    # so it opens a new one
    try:
        app.close()
        app.deleteLater()
    except:
        pass

    app = TraversingDirectories()
    app.setParent(parentHou, QtCore.Qt.Window)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    dark_palette = QtGui.QPalette()
    palette.Palette(dark_palette)

    app.setPalette(dark_palette)
    app.show()