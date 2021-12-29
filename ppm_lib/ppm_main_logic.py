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

all_projects =  pr.Projects().get_all_project_names() 
    
lg.Logger.info(all_projects)











#projects = pr.Projects()
#projects.add_project("PROJECT_C", 24, "1920")
#project = pr.Project("FULL")

#sequences = seq.Sequences(project)
#sequences.add_sequence("AAA")
#sequence = seq.Sequence(project, "AAA")

#shots = s.Shots(sequence)
#shots.add_shot("shotA")
#shot = s.Shot(sequence, "shotA")
#lg.Logger.info(shot.get_path())