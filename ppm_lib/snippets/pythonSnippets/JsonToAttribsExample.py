import json
import os
import hou

def unpack_vec_list(vec_list):
    return [component for vec in vec_list for component in vec]

node = hou.pwd()
geo = node.geometry()

json_file = node.parm("_json").eval()

with open(json_file) as j_file:
    json_contents = json.load(j_file)
    

road_0 = json_contents['world']['roads']['road_0']  
road_1 = json_contents['world']['roads']['road_1'] 
    
road_0_left_lane_width = road_0['left_lane_width']
road_0_right_lane_width = road_0['right_lane_width']
road_0_ids = [int(_id) for _id in road_0['points']]

road_1_left_lane_width = road_1['left_lane_width']
road_1_right_lane_width = road_1['right_lane_width']
road_1_ids = [int(_id) for _id in road_1['points']]


all_positions = []
for pos in json_contents['world']['points']:
    final_pos = [float(pos[0]), 0.0, float(pos[1])]
    all_positions.append(final_pos)
    print (final_pos)


geo.addAttrib(hou.attribType.Global, "road_0_left_lane_w", road_0_left_lane_width)
geo.addAttrib(hou.attribType.Global, "road_0_right_lane_w", road_0_right_lane_width)
geo.addAttrib(hou.attribType.Global, "road_1_left_lane_w", road_1_left_lane_width)
geo.addAttrib(hou.attribType.Global, "road_1_right_lane_w", road_1_right_lane_width)
geo.addAttrib(hou.attribType.Global, "road_width", road_0_right_lane_width + road_0_left_lane_width)

geo.addArrayAttrib(hou.attribType.Global, "ids_road_0", hou.attribData.Int, tuple_size=1)
geo.setGlobalAttribValue("ids_road_0", road_0_ids)

geo.addArrayAttrib(hou.attribType.Global, "ids_road_1", hou.attribData.Int, tuple_size=1)
geo.setGlobalAttribValue("ids_road_1", road_1_ids)

geo.addArrayAttrib(hou.attribType.Global, "positions", hou.attribData.Float, tuple_size=3)
geo.setGlobalAttribValue("positions", unpack_vec_list(all_positions))



