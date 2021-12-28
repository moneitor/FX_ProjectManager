from logging_utils import logger as lg
import database_interface as db
import database_utils as db_u
from directory_utils import ppm_mkdir, ppm_rmdir

import os


######################### COMANDS ###################################
CREATE_PROJECTS = 'CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, fps INTEGER, resolution TEXT, path TEXT);'
CREATE_SEQUENCES = 'CREATE TABLE IF NOT EXISTS sequences (id INTEGER PRIMARY KEY, name TEXT, fps INTEGER, resolution TEXT, path TEXT);'

INSERT_PROJECT = 'INSERT INTO projects (name, fps, resolution, path) VALUES (?, ?, ?, ?);'

GET_ALL_PROJECTS = 'SELECT * FROM projects'
GET_ALL_SEQUENCES = 'SELECT * FROM sequences'

GET_PROJECT_BY_NAME = 'SELECT * FROM projects WHERE name = ?;'
DELETE_BY_NAME = 'DELETE FROM projects WHERE name = ?;'

#######################################################################


PROJECTS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
PROJECTS_PATH = os.path.join(PROJECTS_PATH, "projects/")


class Projects:    
    
    def __init__(self):
        # Connection to the database        
        self.connection_project = db_u.connect(os.path.join(PROJECTS_PATH, "projects.db")) 
        
        # Creation of the database table
        db_u.create_table(self.connection_project, CREATE_PROJECTS)
        
    
    def get_all_projects_info(self):
        """
        Displays all the projects
        """
        projects = db.get_all(self.connection_project, GET_ALL_PROJECTS)        
        return projects
        
        
    def get_all_project_names(self):
        """
        Displays all the project names
        """
        names = []
        projects = self.get_all_projects_info()
        
                
        for project in projects:
            names.append(project[1])
        
        return names    
    
    
    def get_all_projects_path(self):
        """
        Displays all the project names
        """
        path = []
        projects = self.get_all_projects_info()
        
        for project in projects:
            if os.path.exists(project[-1]):
                path.append(project[-1])
                
            else:
                lg.Logger.warning("Project {} does not exist".format(project[1]))
        
        return path
    
    
    def create_project(self, name, fps, resolution):
        """Creates the project folder 
        and stores the information on the database
        """
        path = os.path.join(PROJECTS_PATH, name)        
        db.add_new(self.connection_project, name, fps, resolution, path, INSERT_PROJECT)
        
        
        #Creation of the project folder
        if os.path.exists(PROJECTS_PATH):
            ppm_mkdir(path)              
        
        
        
    def delete_project(self, name):
        """Deletes the project with the given name"""
        path = os.path.join(PROJECTS_PATH, name)
        db.delete(self.connection_project, path, DELETE_BY_NAME)
    
    

class Project:
    def __init__(self, project_name):
        self.project_name = project_name    
        
        # Connection to the database
        self.connection_project = db_u.connect(os.path.join(PROJECTS_PATH, "projects.db"))         
        self.connection_seq = db_u.connect(os.path.join(PROJECTS_PATH, self.project_name, "sequences.db"))
                
        # Creation of the database table
        db_u.create_table(self.connection_project, CREATE_PROJECTS)    
        db_u.create_table(self.connection_seq, CREATE_SEQUENCES)   

    
    def get_sequences(self):
        seqs = db.get_all(self.connection_seq, GET_ALL_SEQUENCES) 
        sequences = []
        for seq in seqs:
            sequences.append(seq[-1])
        return sequences
    
       
    def get_shots(self):
        pass
    
    
    def get_path(self):
        path = db.find_by_name(self.connection_project, self.project_name, GET_PROJECT_BY_NAME)
        if path != None:
            path = path.split(",")[-1].strip()
        return path
    
    
    def get_fps(self):
        fps = db.find_by_name(self.connection_project, self.project_name, GET_PROJECT_BY_NAME)
        if fps != None:
            fps = fps.split(",")[2].strip()
        return fps
    
    
    def get_resolution(self):
        resolution = db.find_by_name(self.connection_project, self.project_name, GET_PROJECT_BY_NAME)
        if resolution != None:
            resolution = resolution.split(",")[3].strip()        
        return resolution        
    
    
    def get_project_info(self):
        info = db.find_by_name(self.connection_project, self.project_name, GET_PROJECT_BY_NAME)
        return info
        
    
    
    
    

if __name__ == "__main__":

    
    #prs = Projects()
    pr = Project("CHAMACO")
    #lg.Logger.info(pr.get_project_info())
    lg.Logger.info(pr.get_sequences())
    #prs.create_project("CHORIZO", 30, "1920x1080")
    #prs.delete_project("ROMOLA")
    
    #lg.Logger.info(prs.get_all_projects_path())
    #lg.Logger.info(prs.get_all_projects_info())

    
    