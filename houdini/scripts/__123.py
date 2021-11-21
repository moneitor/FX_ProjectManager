import hou
import os
import json

project_path = os.environ.get("PROJECT_PATH")
json_project_path = project_path + "/project_Info.json"
obj = hou.node("/obj")

# read the information of the project info json file
def read_shot_info(path):
    info = ""
    with open(path, "r") as file:
        info = json.load(file) 
    
    fps = info["FPS"]       

    return fps

fps = int(read_shot_info(json_project_path))

#creates a Null
null = obj.createNode("null" , "Cam_control")

#create camera
def createCam(_null):
    cam = obj.createNode("cam", "shot_cam")
    res = {'resx': 1920 , 'resy': 1080}
    #set the camera parms
    cam.setParms(res)
    cam.setInput(0 , _null)
    cam.moveToGoodPosition()
    return cam


#Create the mantra node
out = hou.node("/out")

def createMantra(_cam):
    mantra = out.createNode("ifd", "mantra_shot")
    camParm = mantra.parm("camera")
    camParm.set(_cam.path())
    mantra.parm("vobject").set("")
    mantra.parm("alights").set("")
    mantra.setParms({"vm_renderengine": "pbrraytrace" , "trange": "normal"})





def main():    
    hou.setFps(fps)
    cam = createCam(null)
    createMantra(cam)




main()