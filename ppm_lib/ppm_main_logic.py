from typing import Sequence
from ppm_logger import logger as lg
from entity import project as pr, sequence
from entity import sequence as seq
from entity import shot as s
import db.database_utils as db_u


import os


######################### COMANDS ###################################
CREATE_PROJECTS = 'CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, fps INTEGER, resolution TEXT, path TEXT);'
GET_ALL_PROJECTS = 'SELECT * FROM projects'
#######################################################################


PROJECTS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\",'/')
PROJECTS_PATH = os.path.join(PROJECTS_PATH, "projects").replace("\\",'/')



# Connection to the database        
if os.path.exists(PROJECTS_PATH):
    connection_project = db_u.connect(os.path.join(PROJECTS_PATH, "projects.db")) 
else:
    os.makedirs(PROJECTS_PATH)
        
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
        projects = pr.Projects()
        projects.delete_project(name)   
        
        
        
        
######## SEQUENCES  ######################################
def get_sequence(project, sequence_name):    
    sequence = seq.Sequence(project, sequence_name)    
    return sequence


def create_new_sequence(project, sequence_name):
    if project and sequence_name:
        sequences = seq.Sequences(project)
        sequences.add_sequence(sequence_name)


def delete_sequence(project, sequence_name):
    if sequence_name:              
        sequences = seq.Sequences(project)
        sequences.delete_sequence(sequence_name)





######## SHOTS  ##########################################    
def get_shot(sequence, shot_name):
    shot = s.Shot(sequence, shot_name)    
    return shot


def get_shot_first_frame(sequence, shot_name):
    shot = s.Shot(sequence, shot_name)
    first_frame = shot.get_first_frame()
    return first_frame


def get_shot_last_frame(sequence, shot_name):
    shot = s.Shot(sequence, shot_name)
    last_frame = shot.get_last_frame()
    return last_frame


def create_new_shot(sequence, shot_name, first_frame, last_frame):
    if sequence and shot_name:
        shots = s.Shots(sequence)
        shot = shots.add_shot(shot_name, first_frame, last_frame)
        
        return shot
    
    
def edit_shot(sequence, shot_name, first_frame, last_frame):
    if sequence and shot_name:
        shots = s.Shots(sequence)
        shot = shots.edit_shot(shot_name, first_frame, last_frame)
        print("EDITING LOGIC")


def delete_shot(sequence, shot_name):
    if shot_name:              
        shots = s.Shots(sequence)        
        shots.delete_shot(shot_name)


if __name__ == "__main__":
    
    projects = pr.Projects()
    projects.delete_project("romola")
    #projects.add_project("PROJECT_C", 24, "1920")
    project = pr.Project("FULL")

    sequences = seq.Sequences(project)
    sequences.add_sequence("AAA")
    sequence = seq.Sequence(project, "AAA")

    #shots = s.Shots(sequence)
    #shots.add_shot("shotA")
    #shot = s.Shot(sequence, "shotA")
    lg.Logger.info(projects.get_all_project_names())