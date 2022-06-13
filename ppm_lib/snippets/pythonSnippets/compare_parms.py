import hou

if len(hou.selectedNodes()) == 2:
    node_source = hou.selectedNodes()[0]
    node_target = hou.selectedNodes()[1]
   
    source_name = node_source.name()
    target_name = node_target.name()
   
    parms_source = [parm for parm in node_source.parms()]
    node_target  = [parm for parm in node_target.parms()]
   
    all_parms = zip(parms_source, node_target)
    diff_parms = []
   
    for parm in all_parms:
        if parm[0].eval() != parm[1].eval():
            if "folder" not in parm[0].name():              
                                                   
                str_build = "Parm Name: %20s ===> Value 1:  %10s   , Value 2: %10s"% (parm[0].name() , str(parm[0].eval()), str(parm[1].eval()) )
               
                diff_parms.append(str_build)
         
    hou.ui.selectFromList(diff_parms, column_header="------------------------------------------------{}-----------------------------------------------{} ".format(source_name.upper(), target_name.upper()),
                          message="""This list displays the parameters with different values
                          between the two selected nodes""", width=800)
