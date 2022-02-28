import hou
import importlib

from PySide2.QtWidgets import QMessageBox
from PySide2 import QtWidgets

from ppm_hdas import create_hda_ui as c
importlib.reload(c)

from ppm_hdas import create_hda_logic as l
importlib.reload(c)



node = None
if hou.selectedNodes():
    
    node = hou.selectedNodes()[0]
    if node.canCreateDigitalAsset():
        node_ptg = node.parmTemplateGroup()
        
        for i in range(4):
            lbl_parm = "label" + str(i + 1)
            
            if node.parm(lbl_parm) is not None:
                node_ptg.remove(lbl_parm)
                
    
        new_hda = c.HDA_Save()
        result = new_hda.exec_()
        
        if result == QtWidgets.QDialog.Accepted:
            _name = new_hda.return_name()     
            _path = new_hda.return_path() 
            _version = new_hda.return_version()     
            _inputs = new_hda.return_inputs()   
            _description = new_hda.return_description()
    
            otl_new_node = node.createDigitalAsset(name = _name,
                                    hda_file_name=_path,
                                    description=_name, 
                                    comment=_description, 
                                    min_num_inputs=_inputs, 
                                    version=_version)  
                                    
            otl_new_node.type().definition().setParmTemplateGroup(node_ptg)
                                    
                                    
else:
    msgBoxSave = QMessageBox()
    msgBoxSave.setText('Select a node that can be converted into an HDA')
    msgBoxSave.exec_()
    