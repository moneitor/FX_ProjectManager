node = hou.selectedNodes()[0]

if node:
    lst_nodes = [n.path() for n in node.dependents()]
    
    hou.ui.selectFromList(lst_nodes, column_header="Dependent Nodes")
    
