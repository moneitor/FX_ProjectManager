node = hou.selectedNodes()[0]

n_ptg = node.parmTemplateGroup()

if node.parm("standardfolder1") is not None:
    n_ptg.remove("standardfolder1")
    
node.type().definition().setParmTemplateGroup(n_ptg)   
   
print("\n\n\n")
