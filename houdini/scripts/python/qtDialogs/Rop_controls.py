import hou
import os

from file_scripts import palette
from PySide2 import QtCore, QtWidgets, QtGui


parentHou = hou.ui.mainQtWindow()

list_headers = ["Rop Node", "Active", "Rend Engine", "Pixel Samples", "M Blur", "Min ray samples",
"Max ray samples"]
list_render_engines = ["micropoly", "raytrace", "pbrmicropoly", "pbrraytrace", "photon"]


class RopControls(QtWidgets.QWidget):
    def __init__(self, parent=parentHou):
        super(RopControls, self).__init__()

        self.setWindowTitle("Rop controls")
        self.setMinimumWidth(900)
        self.setMinimumHeight(150)

        self.widgets()
        self.layout()
        self.connections() 

        self.current_render_engine = ""       

        self.rop_names = []
        self.rop_paths = []
        self.actives = []
        self.rend_engine = []
        self.pixel_samples = []
        self.motion_blur = []
        self.min_ray_samp = []
        self.max_ray_samp = []

        self.clean_table()
        self.return_mantra_nodes()
        self.fill_table()


    def widgets(self):
        self.table_rops = QtWidgets.QTableWidget()
        self.table_rops.setColumnCount(7)
        self.table_rops.setHorizontalHeaderLabels(list_headers)
        self.table_rops.setColumnWidth(0, 140)
        self.table_rops.setColumnWidth(1, 90)
        self.table_rops.setColumnWidth(2, 140)
        self.table_rops.setColumnWidth(3, 90)
        self.table_rops.setColumnWidth(4, 70)
        self.table_rops.setColumnWidth(5, 140)
        self.table_rops.setColumnWidth(6, 140)
        header_size = self.table_rops.horizontalHeader()
        header_size.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.btn_update = QtWidgets.QPushButton("Update")
        self.btn_close = QtWidgets.QPushButton("Close")

    def layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_update)
        button_layout.addWidget(self.btn_close)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(0.1)

        main_layout.addWidget(self.table_rops)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def connections(self):
        self.table_rops.cellChanged.connect(self.change_display_flag)
        self.table_rops.cellChanged.connect(self.update_motion_blur)
        self.table_rops.cellChanged.connect(self.update_pixel_samples)
        self.table_rops.cellChanged.connect(self.get_value_from_table)
        self.table_rops.cellChanged.connect(self.set_value_from_table)
        
        self.btn_update.clicked.connect(self.clean_table)
        self.btn_update.clicked.connect(self.return_mantra_nodes)
        self.btn_update.clicked.connect(self.fill_table)

        self.btn_close.clicked.connect(self.close)

    def keyPressEvent(self, event):
        super(RopControls, self).keyPressEvent(event)
        event.accept()

    def return_mantra_nodes(self):
        """
        Return all the mantra nodes contained inside
        hou.node("/out"), it only work for mantra nodes for now
        """

        root = hou.node("/out")
        rop_paths = []
        rop_names = []
        actives = []
        r_engine = []
        p_samples = []
        m_blur = []
        min_r_samples = []
        max_r_samples = []

        for rop in root.children():
            if rop.type().name() == "ifd":
                rop_paths.append(rop.path())
                rop_names.append(rop.name())
                actives.append(rop.isBypassed())
                r_engine.append(rop.parm("vm_renderengine").eval())
                p_samples.append([rop.parm("vm_samplesx").eval() , rop.parm("vm_samplesy").eval()])
                m_blur.append(rop.parm("allowmotionblur").eval())
                min_r_samples.append(rop.parm("vm_minraysamples").eval())
                max_r_samples.append(rop.parm("vm_maxraysamples").eval())


        self.rop_names = rop_names
        self.rop_paths = rop_paths    
        self.actives = actives
        self.rend_engine = r_engine
        self.pixel_samples = p_samples  
        self.motion_blur = m_blur   
        self.min_ray_samp = min_r_samples   
        self.max_ray_samp = max_r_samples


    def clean_table(self):
        """
        Clean the rop table widget
        """
        self.table_rops.setRowCount(0)


    def fill_table(self):
        """
        Fills the rop table with the information contained in the nodes
        """
        
        for node in range(len(self.rop_names)):
            self.table_rops.insertRow(node)
            self.insert_item(node, 0, self.rop_names[node], False)
            self.insert_item(node, 1, (self.actives[node]), True)
            self.insert_item(node, 2, self.rend_engine[node] , False)
            self.insert_item(node, 3, str(self.pixel_samples[node]), False)
            self.insert_item(node, 4, str(self.motion_blur[node]), True)
            self.insert_item(node, 5, str(self.min_ray_samp[node]), False)
            self.insert_item(node, 6, str(self.max_ray_samp[node]), False)


    def insert_item(self, row, column, text, is_boolean):
        """
        Inserts items in the rop table widget, if the information is
        a boolean it will add a checkbox to the table
        """
        combobox_engine = QtWidgets.QComboBox()
        combobox_engine.addItems(list_render_engines)            
        current_rend_engine = hou.node("/out/" + self.rop_names[row]).parm("vm_renderengine").eval()
        combobox_engine.setCurrentText(current_rend_engine)  
        combobox_engine.currentTextChanged.connect(self.change_render_engine)   
        combobox_engine.currentTextChanged.connect(lambda: self.update_render_engine(row, self.current_render_engine))

        item = QtWidgets.QTableWidgetItem(text)
        
        if is_boolean and column == 1:
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)            
            if text != 1 :
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

        if is_boolean and column == 4:
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)            
            if text == 1 or text == "1":
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
                
        if column != 2:
            self.table_rops.setItem(row, column, item)
        else:
            self.table_rops.setCellWidget(row, column, combobox_engine)


    def change_display_flag(self, row, column):
        """
        Change the display flag of the nodes
        """
        if column == 1:
            item = self.table_rops.item(row,column)
            rop_node = hou.node("/out/{}".format(self.rop_names[row]))
            rop_path = rop_node.path()              
            
            if item.checkState() == QtCore.Qt.CheckState.Checked:                
                hou.node(rop_path).bypass(0)
                
            else:
                hou.node(rop_path).bypass(1)


    def change_render_engine(self, engine):   
        """
        return the curren render engine as a string and store it in the
        class attribute self.current_render_engine to be used by other methods
        """     
        rop_engine = engine  
        self.current_render_engine = str(rop_engine)

        
    def update_render_engine(self, row, engine):   
        """
        Updates the render engine in the mantra node selected in the 
        TableWidget
        """     
        hou.node("/out/" + self.rop_names[row]).parm("vm_renderengine").set(self.current_render_engine)
       
    def update_motion_blur(self, row, column):
        """
        Updates the Allow Motion Blur parm in the mantra node
        """
        if column == 4:
            item = self.table_rops.item(row, column)
            rop_node = hou.node("/out/{}".format(self.rop_names[row]))
            rop_path = rop_node.path() 

            if item.checkState() == QtCore.Qt.CheckState.Checked:
                hou.node(rop_path).parm("allowmotionblur").set(1)
            else:
                hou.node(rop_path).parm("allowmotionblur").set(0)

    def update_pixel_samples(self, row, column):
        """
        Updates the pixel sample values in the mantra node
        """
        if column == 3:
            item = self.table_rops.item(row, column)
            pixel_samples = eval(item.text())

            rop_node = hou.node("/out/{}".format(self.rop_names[row]))
            rop_node.parm("vm_samplesx").set(pixel_samples[0])
            rop_node.parm("vm_samplesy").set(pixel_samples[1])


    def get_value_from_table(self, row, column):
        if column == 5:
            item = self.table_rops.item(row, column)
            out_value = eval(item.text())

            rop_node = hou.node("/out/{}".format(self.rop_names[row]))
            rop_node.parm("vm_minraysamples").set(item.text())
            
    def set_value_from_table(self, row, column):
        if column == 6:
            item = self.table_rops.item(row, column)
            out_value = eval(item.text())

            rop_node = hou.node("/out/{}".format(self.rop_names[row]))
            rop_node.parm("vm_maxraysamples").set(item.text())



    """
    def set_value_from_table(self, row, column):
        if column == 6:
            item = self.table_rops.item(row, column)
            out_value = eval(item.text())

            rop_node = hou.node("/out/{}".format(self.rop_names[row]))
            rop_node.parm("vm_maxraysamples").set(item.text())
    """
             
        


def run_app():
    # check if the dialog already exist and delete it
    # so it opens a new one
    try:
        app.close()
        app.deleteLater()
    except:
        pass

    app = RopControls()
    app.setParent(parentHou, QtCore.Qt.Window)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    dark_palette = QtGui.QPalette()
    palette.Palette(dark_palette)

    app.setPalette(dark_palette)
    app.show()