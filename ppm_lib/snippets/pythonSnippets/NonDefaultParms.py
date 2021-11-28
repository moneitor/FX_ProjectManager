node = hou.pwd()
geo = node.geometry()

read_parm = node.parm("nodeToEval").eval()

parms = hou.node(read_parm).parms()
modified_parms = {}

for parm in parms:
    if not parm.isAtDefault():
        modified_parms[parm.name()] = parm.eval()

string_dict = str(modified_parms)
        
geo.setGlobalAttribValue( "storedParms", string_dict)

print (str(modified_parms))
