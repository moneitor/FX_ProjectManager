import hou
import toolutils

#node_to_run  = hou.node(hou.ui.selectNode())
node_to_run = hou.node("/obj/geo1")

out = hou.node("/out")

childs= node_to_run.allSubChildren()

fx_cache_version = 71
str_match = "cglibrary::fx_cache::{}".format(str(fx_cache_version))

cmd = '''from sys import exit
fetch = kwargs["node"]
sourcePath = fetch.parm("source").eval()
foo = 1 if hou.node(sourcePath) != None else exit(0)
foo = 1 if "fx_cache" in hou.node(sourcePath).parent().parent().type().name() else exit(0)
node = hou.node(sourcePath).parent().parent()
networkEditor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
networkEditor.setCurrentNode(node)
size = 2
pos = node.position()
bounds = hou.BoundingRect(pos-hou.Vector2(size,size), pos+hou.Vector2(size,size))
networkEditor.setVisibleBounds(bounds)'''


    
def create_rop(node):
    """Creates a fetch node pointing to the internal rop net for chaining

    New fetch rop will be named by grabbing the fxCache name plus all the asset tags
    """
    # Make fetch node with path to fxCache grouping
    ropnet = hou.node("/out")
    
    #make sure to not have duplicate fetches
    ropNodes = ropnet.children()
    for child in ropNodes:
        if(child.type().name() == "fetch"):
            if(child.node(child.parm("source").evalAsString()) == None):
                continue
            if(child.node(child.parm("source").evalAsString()).parent().parent() == node):
                return 0
    # Tokens to use in fetch node name
    toks = [
        node.name(),        
        node.parm("definition").evalAsString()        
        ]
        
    fetch = ropnet.createNode("fetch", "_".join(toks))
    fetch.moveToGoodPosition()
    fetch.parm("source").set("%s/ropnet1/OUT" % node.path())
    
    fetch_path = fetch.path()
    
    #jump button command
    cmd = '''from sys import exit
    fetch = kwargs["node"]
    sourcePath = fetch.parm("source").eval()
    foo = 1 if hou.node(sourcePath) != None else exit(0)
    foo = 1 if "fx_cache" in hou.node(sourcePath).parent().paren
    [pasted text truncated for security]
