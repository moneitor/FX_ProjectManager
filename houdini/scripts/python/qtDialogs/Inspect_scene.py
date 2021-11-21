import hou
import os

from file_scripts import palette
from PySide2 import QtCore, QtWidgets, QtGui

parentHou = hou.ui.mainQtWindow()

class InspectScene(QtWidgets.QWidget):
    def __init__(self, parent=parentHou):
        super(InspectScene, self).__init__()

        self.setWindowTitle("Inspect houdini scene")
        self.setMinimumSize(300,80)

        self.file_path = ""

        self.widgets()
        self.layout()
        self.connections()

    def widgets(self):
        self.ln_file_path = QtWidgets.QLineEdit()
        self.btn_find_file = QtWidgets.QPushButton("Search")

        self.rbn_obj = QtWidgets.QRadioButton("/obj")
        self.rbn_obj.setChecked(True)
        self.rbn_out = QtWidgets.QRadioButton("/out")
        self.rbn_mat = QtWidgets.QRadioButton("/mat")

        self.btn_update = QtWidgets.QPushButton("Update")
        self.btn_merge = QtWidgets.QPushButton("Merge")
        self.btn_close = QtWidgets.QPushButton("Close")

        self.tree_nodes = QtWidgets.QTreeWidget()
        self.tree_nodes.setColumnCount(1)
        self.tree_nodes.setHeaderLabels(["Nodes"])

    def layout(self):
        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self.ln_file_path)
        path_layout.addWidget(self.btn_find_file)

        rbn_layout = QtWidgets.QHBoxLayout()
        rbn_layout.addWidget(self.rbn_obj)
        rbn_layout.addWidget(self.rbn_out)
        rbn_layout.addWidget(self.rbn_mat)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_merge)
        btn_layout.addWidget(self.btn_close)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("File:", path_layout)
        form_layout.addRow(rbn_layout)
        form_layout.addRow(btn_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.tree_nodes)

    def connections(self):
        self.btn_update.clicked.connect(self.update_tree_widget)

        self.btn_find_file.clicked.connect(self.search_file)
        self.btn_merge.clicked.connect(self.merge_nodes)

        self.rbn_obj.clicked.connect(self.return_nodes_in_context)

        self.btn_close.clicked.connect(self.close)

    def search_file(self):
        """Return the path to the file that we want to merge the files from"""

        new_directory = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", os.chdir(r"C:/_fxProjects/_projects"))
        if new_directory[0]:
            if(new_directory[0].endswith(".hip")):
                self.file_path = str(new_directory[0])
                self.ln_file_path.setText(new_directory[0])   
            else:
                print("\n*************************\n")
                print("Please select a houdini file.")  
                print("\n*************************\n")        

    def return_nodes_in_context(self):
        """Returns a list with all the nodes in the current
            context selected"""
        file_path = self.file_path
        if file_path:
            root = hou.node("/obj")
            test = hou.hipFile.collisionNodesIfMerged(file_path, node_pattern="/obj/*")
            print(test)

            
        else:
            print("\n*************************\n")
            print("Please select a houdini file.")  
            print("\n*************************\n")


    def update_tree_widget(self):
        """Updates the tree widget with the nodes in the current 
            context selected"""
        self.tree_nodes.clear()

    def merge_nodes(self):
        """Merge the selected nodes in the tree widget into the file
            in the same context selected"""
        pass


def run_app():
    # check if the dialog already exist and delete it
    # so it opens a new one
    try:
        app.close()
        app.deleteLater()
    except:
        pass

    app = InspectScene()
    app.setParent(parentHou, QtCore.Qt.Window)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    dark_palette = QtGui.QPalette()
    palette.Palette(dark_palette)

    app.setPalette(dark_palette)
    app.show()