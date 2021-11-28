"""This functions is used inside the hdaModule of the attribute splitter on TBS
It takes the string list attribute called parts, iterates through that list, and then for 
each element of the list, it will create a Blast that will keep only the geometry where an attribute
with the same name as the current element of the list exists
"""

def blasts_from_list(node):
    """
    Generates a blast from each different value of an attribute
    """
    att_parm = node.parm("att")
    run_over = node.parm("runover").eval()
    
    if att_parm:
        geo = node.geometry()
        input_path = node.inputs()[0]
        parent_path = node.parent().path()
        
        att = node.parm("att").eval()
        
        parts = geo.stringListAttribValue("parts")
        
        strings = ["@" + att + "=" + part for part in parts]
        
        for string in strings:
            name = string.split("=")[-1]
            
            if len(name):
                blast = hou.node(parent_path).createNode("blast", name, force_valid_node_name=True)
            else:
                blast = hou.node(parent_path).createNode("blast", "empty")
            blast.setNextInput(input_path)     
            blast.moveToGoodPosition()
            blast.parm("group").set(string)
            blast.parm("negate").set(1)
            
            if run_over == 0:
                blast.parm("grouptype").set(3)
            else:
                blast.parm("grouptype").set(4)
            
    else:
        pass


def main(node):
    blasts_from_list(node)
    
