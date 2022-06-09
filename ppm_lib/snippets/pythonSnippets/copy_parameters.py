import hou

if len(hou.selectedNodes()) == 2:
    node_source = hou.selectedNodes()[0]
    node_target = hou.selectedNodes()[1]
    
    print(node_source.name(), node_target.name())
    
    nptg_source = node_source.parmTemplateGroup()
    nptg_target = node_target.parmTemplateGroup()
    
    for i in range(4):
        lbl_parm = "label" + str(i + 1)
        print(lbl_parm)
        
        if node_target.parm(lbl_parm) is not None:
            nptg_target.remove(lbl_parm)
            print("removing: {}".format(lbl_parm))
    
    node_target.setParmTemplateGroup(nptg_source)
    
else:
    hou.ui.displayMessage("""Please select two nodes, the first node is the one that contains
    the parameters, and the second one is the one where you want to copy the parameters""")
