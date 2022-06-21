from db import database_utils
from ppm_logger import logger as lg
import os

PROJECTS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
PROJECTS_PATH = os.path.join(PROJECTS_PATH, "projects/")

projects_db = os.path.join(PROJECTS_PATH, "projects.db")


# PROJECTS #########################################
def add_new(connection, name, fps, resolution, path, cmd):
    """Adds a new PROJECT
    """
    _name = name
    _fps = int(str(fps))
    _resolution = resolution
    _path = path
            
    database_utils.add(connection, _name, _fps, _resolution, _path, cmd)
    
  
def get_all(connection, cmd):
    """Gets all Projects
    """
    projects = database_utils.get_all(connection, cmd)            
           
    return projects
        

def find_by_name(connection, name, cmd):
    """Finds a PROJECT by name
    """
    _name = name
    
    datas = database_utils.get_by_name(connection, name, cmd)   
    
    for data in datas:
        info = "{}, {}, {}, {}, {}".format(data[0], data[1], data[2], data[3], data[4])
        return(info)
    



# SEQUENCES  ##############################################
def add_new_sequence(connection, name, path, cmd):
    _name = name
    _path = path            
    database_utils.add_sequence(connection, _name, _path, cmd)


def find_by_name_sequence(connection, name, cmd):
    _name = name
    
    datas = database_utils.get_by_name(connection, name, cmd)   
    
    for data in datas:
        info = "{}, {}, {}".format(data[0], data[1], data[2])
        return(info)    


    



# SHOTS #############################################
def add_new_shot(connection, name, firstFrame, lastFrame, path, cmd):
    _name = name
    _first_frame = firstFrame
    _last_frame = lastFrame
    _path = path            
    database_utils.add_shot(connection, _name, _first_frame, _last_frame, _path, cmd)


def find_by_name_shot(connection, name, cmd):
    _name = name
    
    datas = database_utils.get_by_name(connection, name, cmd)   
    
    for data in datas:
        info = "{}, {}, {}, {}, {}".format(data[0], data[1], data[2], data[3], data[4])
        return(info)
                




# GENERIC FUNCTIONS ######################################
def delete(connection, name, cmd):    
    database_utils.delete_by_name(connection, name, cmd)  
    





if __name__ == "__main__":
    pass
