import hou


def return_null_children():
    """RETURN A LIST WITH ALL MERGEABLE NODES"""
    nodesList = []
    for node in hou.selectedNodes():  
        childrens = node.allSubChildren()
        if len(childrens) > 0:
            for child in childrens:
                if child.type().name() == "geo":
                    for newChild in child.allSubChildren():
                        if not len(newChild.outputs()):
                            if newChild.type().name() != "subnet":    
                                nodesList.append(newChild)
                              
    return nodesList

    
def create_merge(objects_to_merge):
    """CREATE A MERGE NODE WITH ALL THE OUPUT FROM FBX"""
    num = len(objects_to_merge)
    name = hou.selectedNodes()[0]
    name = name.name()
    merge_node = hou.node("/obj").createNode("geo" , name + "_merge")
    
    merge = merge_node.createNode("object_merge" , name + "_merge")
    merge.parm("numobj").set(num)
    
    for i in range(1 , num+1):
        path = objects_to_merge[i-1].path()
        merge.parm('objpath%d' %i).set(path)
                              

    
create_merge(return_null_children())


