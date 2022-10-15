import hou

def att_warning(node):    
    geo = node.geometry()    
   
    pt_atts = list(geo.stringListAttribValue("_1_pointattribs"))
    prim_atts = list(geo.stringListAttribValue("_1_primitiveattribs"))
    vert_atts = list(geo.stringListAttribValue("_1_vertexattribs"))
   
    not_v = ""
    not_N = ""
    not_uv = ""
    not_path = ""
   
    if "v" not in pt_atts:
        not_v = "v"
       
    if "N" not in vert_atts:
        not_N = "N"
       
    if "uv" not in vert_atts:
        not_uv = "uv"
       
    if "path" not in prim_atts:
        not_path = "path"      
       
       
    warning_text = "{}   {}   {}  {}".format(not_v, not_N, not_uv, not_path)
   
    node.parm("lbl_warning").set(warning_text)
   
   


def return_list_as_string(att_list):
    """
    Returns a list as a long string where the elements of the list
    are separated by ',  '
   
    """
    output = " ".join(att_list)
    if len(att_list) > 0:
        return output
    else:
        return "No different attributes to the other input"
       
   
def all_atts_list(list1, list2):
    """
    returns a string that will be used to populate the 'All Attributes'
    parm of the OTL
   
    """
   
    in_list1 = sorted(list1)
    in_list2 = sorted(list2)
   
    input1 = "Input 1: {}".format(" ".join(in_list1))
   
    input2 = "Input 2: {}".format(" ".join(in_list2))
   
    return (input1 + "\n" + input2)        
   
   
def fill_parms(node):      
    """
    Updates the parameters of the OTL
    """
    geo = hou.node(node.path() + '/POINT').geometry()
   
   
    in_pt_list_1 = list(geo.stringListAttribValue("diff_pt_att_1"))
    in_pt_list_2 = list(geo.stringListAttribValue("diff_pt_att_2"))    
    in_pt_all_atts_1 = list(geo.stringListAttribValue("_1_pointattribs"))
    in_pt_all_atts_2 = list(geo.stringListAttribValue("_2_pointattribs"))
   
    in_prim_list_1 = list(geo.stringListAttribValue("diff_prim_att_1"))
    in_prim_list_2 = list(geo.stringListAttribValue("diff_prim_att_2"))
    in_prim_all_atts_1 = list(geo.stringListAttribValue("_1_primitiveattribs"))
    in_prim_all_atts_2 = list(geo.stringListAttribValue("_2_primitiveattribs"))
     
 
    in_vert_list_1 = list(geo.stringListAttribValue("diff_vert_att_1"))
    in_vert_list_2 = list(geo.stringListAttribValue("diff_vert_att_2"))  
    in_vert_all_atts_1 = list(geo.stringListAttribValue("_1_vertexattribs"))
    in_vert_all_atts_2 = list(geo.stringListAttribValue("_2_vertexattribs"))    
   

    node.parm('in1_1').set(return_list_as_string(in_pt_list_1))    
    node.parm('in2_1').set(return_list_as_string(in_pt_list_2))
    node.parm('all_atts_points').set(all_atts_list( in_pt_all_atts_1, in_pt_all_atts_2 ))
   
   
    node.parm('in1_2').set(return_list_as_string(in_prim_list_1))
    node.parm('in2_2').set(return_list_as_string(in_prim_list_2))
    node.parm('all_atts_prims').set(all_atts_list( in_prim_all_atts_1, in_prim_all_atts_2 ))  
   
   
    node.parm('in1_3').set(return_list_as_string(in_vert_list_1))    
    node.parm('in2_3').set(return_list_as_string(in_vert_list_2))
    node.parm('all_atts_verts').set(all_atts_list( in_vert_all_atts_1, in_vert_all_atts_2 ))
   
    att_warning(node)
   
   
def create_att_delete(node):
    """
    Creates an attribute delete node that will delete the attributes from Input1
    that are not present on Input2
   
    """

    default_text = 'No different attributes to the other input'
   
    point_atts = node.parm('in1_1').eval()
    prim_atts = node.parm('in1_2').eval()
    vert_atts = node.parm('in1_3').eval()
   
    if len(point_atts)==0 or len(prim_atts)==0 or len(vert_atts)==0:
        fill_parms(node)
       
    point_atts = node.parm('in1_1').eval()
    prim_atts = node.parm('in1_2').eval()
    vert_atts = node.parm('in1_3').eval()
   
    point_atts.replace("v", "")
    prim_atts.replace("path", "")
    vert_atts.replace("uv", "")
    vert_atts.replace("N", "")
   
    parent_node = node.parent()
    pos = node.position()
    input1 = node.input(0)
           
    attdelete = hou.node(parent_node.path()).createNode("attribdelete", "Cleanup_additional_attribs")
    attdelete.setPosition(pos)
    attdelete.move(hou.Vector2(-2, 0))
    attdelete.setNextInput(input1)
   
    if point_atts != default_text:
        attdelete.parm("ptdel").set(point_atts)
     
    if prim_atts != default_text:
        attdelete.parm("primdel").set(prim_atts)
       
    if vert_atts != default_text:
        attdelete.parm("vtxdel").set(vert_atts)