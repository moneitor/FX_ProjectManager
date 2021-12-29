import sys
sys.path.append("..")

import os
from ppm_logger import logger as lg

PROJECTS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
PROJECTS_PATH = os.path.join(PROJECTS_PATH, "projects")

def shot(shot_number):
    folders = {"Shot_{}".format(str(shot_number)): {"publish": None,
                                               "work": {"anim": None,
                                                        "comp": None,
                                                        "fx":  {"Geo": None , "Textures": None, "Render": None, "Flipbooks": None,
                                                                "Abc": None, "Hda": None, "Simulation": None,
                                                                "Cameras": None},
                                                        "Lighting": None,
                                                        "Roto": None,
                                                        "RnD": None,
                                                        "Track": None,
                                                        "Photogrametry": None,
                                                        "Lens_info": None}}}

    return folders


def ppm_mkdir(path):
    lg.Logger.info("Creating folder {}".format(path))
    if not os.path.exists(path):        
        os.makedirs(path)
    else:
        lg.Logger.warning("Folder {} already exists.".format(path))
        
        
        
def ppm_rmdir(path):
    """
    Removes the directory on the given path
    """
    lg.Logger.info("Removing folder {}".format(path))
    if os.path.exists(path):
        os.removedirs(path)
    
        

def make_dirs_from_dict(dir, folder_dict):    
    """Creates a folder structure using a dictionary structure passed
    as the second argument
    
    dir:: is the path to the folder where the new folders are going to be created
    foder_dict:: is the dictionary with the folder structure
    
    """
    
    for key, values in folder_dict.items():
        pathFolder = os.path.join(dir, key)
        if not os.path.exists(pathFolder):
            ppm_mkdir(pathFolder)
            if type(values) == dict:                
                inner_folder = os.path.join(dir, key)                
                make_dirs_from_dict(inner_folder, values)      

                       
        
def list_of_dirs(path):
    dirs = []
    for dir in os.listdir(path):
        full_path = os.path.join(path, dir)
        dirs.append(full_path)    
        lg.Logger.info(full_path)    
        
    return dirs

        

if __name__ == "__main__":
    #make_dirs_from_dict(PROJECTS_PATH, shot(10))
    #make_dirs_from_dict(PROJECTS_PATH, shot(20))
    #make_dirs_from_dict(PROJECTS_PATH, shot(30))
    #make_dirs_from_dict(PROJECTS_PATH, shot(40))
    list_of_dirs(PROJECTS_PATH)
    
                
                

 