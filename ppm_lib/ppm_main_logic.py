from typing import Sequence
from ppm_logger import logger as lg
from entity import project as pr
from entity import sequence as seq
from entity import shot as s
import db.database_utils as db_u


import os


######################### COMANDS ###################################
CREATE_PROJECTS = 'CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, fps INTEGER, resolution TEXT, path TEXT);'
GET_ALL_PROJECTS = 'SELECT * FROM projects'
#######################################################################


PROJECTS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_PATH = os.path.join(PROJECTS_PATH, "projects/")


# Connection to the database        
connection_project = db_u.connect(os.path.join(PROJECTS_PATH, "projects.db")) 
        
# Creation of the database table
db_u.create_table(connection_project, CREATE_PROJECTS)

    

####### PROJECTS ###########################################
        
def get_project(name):
    project = pr.Project(name)
    return project   
  

def create_new_project(name, fps, resolution):
    if name and fps and resolution:
        pr.Projects().add_project(name, fps, resolution)


def delete_project(name):            
    if name:        
        lg.Logger.critical("{}  Trying to remove project {}".format(__name__, name))
        projects = pr.Projects()
        projects.delete_project(name)   
        
        
######## SEQUENCES  ######################################

def get_sequence(project, sequence_name):
    pass


def create_new_sequence(sequence_name):
    pass


def delete_sequence(sequence_name):
    pass





######## SHOTS  ##########################################    




if __name__ == "__main__":


    projects = pr.Projects()
    projects.delete_project("romola")
    #projects.add_project("PROJECT_C", 24, "1920")
    #project = pr.Project("FULL")

    #sequences = seq.Sequences(project)
    #sequences.add_sequence("AAA")
    #sequence = seq.Sequence(project, "AAA")

    #shots = s.Shots(sequence)
    #shots.add_shot("shotA")
    #shot = s.Shot(sequence, "shotA")
    lg.Logger.info(projects.get_all_project_names())