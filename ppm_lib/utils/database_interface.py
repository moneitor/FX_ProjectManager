import database_utils
from logging_utils import logger as lg
import os

PROJECTS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
PROJECTS_PATH = os.path.join(PROJECTS_PATH, "projects/")

projects_db = os.path.join(PROJECTS_PATH, "projects.db")



def add_new(connection, name, fps, resolution, path, cmd):
    _name = name
    _fps = int(str(fps))
    _resolution = resolution
    _path = path
            
    database_utils.add(connection, _name, _fps, _resolution, _path, cmd)
    
    
    
def get_all(connection, cmd):
    projects = database_utils.get_all(connection, cmd)            
           
    return projects
        
        
        
def find_by_name(connection, name, cmd):
    _name = name
    
    datas = database_utils.get_by_name(connection, name, cmd)   
    
    for data in datas:
        info = "{}, {}, {}, {}, {}".format(data[0], data[1], data[2], data[3], data[4])
        return(info)
        
        

def delete(connection, name, cmd):
    
    database_utils.delete_by_name(connection, name, cmd)    
   
    
    
    
    
def add_new_sequence(connection):
    pass
    





if __name__ == "__main__":
    pass
