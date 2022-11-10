import hou

def create_object_merge(ctrl_click):   
    
    """If shelf is ctrl+click pressed, then the relative path of the node
        will be used
    """
        
    isCtrlClick = ctrl_click

    
    selected = hou.selectedNodes()

    if selected:    

        for node in selected:
            
            pos = node.position()   
            new_pos = pos + hou.Vector2((0, -1.5))
            parent = node.parent()
            null = parent.createNode("null", "OUT_{}".format(node.name()))
            null.setPosition(pos)
            null.move((0, -1.5))
            null.setColor(hou.Color(0.451, 0.369, 0.769))
            
            omerge = parent.createNode("object_merge", "om_{}".format(node.name()))
            omerge.setPosition(pos)
            omerge.move((0, -2.5))
            omerge.setColor(hou.Color(0.451, 0.369, 0.769))
            
            null.setInput(0, node)
            
            relpath = omerge.relativePathTo(null)
            
            if isCtrlClick:
                omerge.parm("objpath1").set(relpath)
            
            else:
                omerge.parm("objpath1").set(null.path())
                
                
                
                
            
def create_rop_fetch():  
    """
    Generates a ROP Fetch at the out context when the selected node
    is a labs::fileCache"""  
    
    nodes = hou.selectedNodes()  
    
    out = hou.node("/out")

    if nodes:
        for node in nodes:
            if "labs::filecache" in node.type().name():
                node.setColor(hou.Color(0.89,0.412,0.761))
                rop_geo = hou.node(node.path() + "/render")    
                fetch = out.createNode("fetch", "out_{}".format(node.name()) )
                fetch.parm("source").set(rop_geo.path())