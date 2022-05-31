from ppm_logger import logger as lg
from db import database_interface as db
import db.database_utils as db_u
from directory.directory_utils import ppm_mkdir, ppm_rmdir, make_dirs_from_dict
from directory import dir_structures as ds
from sys import platform
import stat
from send2trash import send2trash # library to send stuff to the bin

import os

__all__= ["Projects", "project"]

######################### COMANDS ###################################
CREATE_PROJECTS = 'CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, fps INTEGER, resolution TEXT, path TEXT);'
#CREATE_SEQUENCES = 'CREATE TABLE IF NOT EXISTS sequences (id INTEGER PRIMARY KEY, name TEXT, fps INTEGER, resolution TEXT, path TEXT);'
CREATE_SEQUENCES = 'CREATE TABLE IF NOT EXISTS sequences (id INTEGER PRIMARY KEY, name TEXT, path TEXT);'
# TODO UPDATE THE CREATE SEQUENCES DATABASE TO 

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
        
        
    def get_projects(self):
        """Returns a list of Project() objects
        """
        projects = []
        projects_db = db.get_all(self.connection_project, GET_ALL_PROJECTS)
        for project in projects_db:
            current_project = Project(project[1])
            projects.append(current_project)
            
        return projects       
    

        
        
    def get_all_project_names(self):
        '''
        Displays all the project names
        '''
        names = []
        projects = self.get_projects()
        
                
        for project in projects:
            names.append(project.get_name())
        
        return names    
    
    
    def get_all_projects_path(self):
        '''
        Displays all the project names
        '''
        path = []
        projects = self.get_projects()
        
        for project in projects:
            if os.path.exists(project.get_path()):
                path.append(project.get_path())
                
            else:
                lg.Logger.warning("Project {} does not exist".format(project[1]))
        
        return path
    
    
    def add_project(self, name, fps, resolution):
        '''Creates the project folder 
        and stores the information on the database
        '''
        if not db.find_by_name(self.connection_project, name, GET_PROJECT_BY_NAME):        
            path = os.path.join(PROJECTS_PATH, name)        
            db.add_new(self.connection_project, name, fps, resolution, path, INSERT_PROJECT)
            
            #Creation of the project folder
            if os.path.exists(PROJECTS_PATH): 
                asset_dict = ds.asset_folders()                  
                sandbox_dict = ds.sandbox()         
                reference_dict = ds.reference() 
                edit_dict = ds.edit()
                common_dict = ds.common()
                ppm_mkdir(path)
                make_dirs_from_dict(path, asset_dict)
                make_dirs_from_dict(path, sandbox_dict)
                make_dirs_from_dict(path, reference_dict)
                make_dirs_from_dict(path, edit_dict)
                make_dirs_from_dict(path, common_dict)
                  
            
        else:
            lg.Logger.warning("Project [{}] already exists".format(name))       
        

        
    def delete_project(self, name):
        '''Deletes the project with the given name'''
        lg.Logger.critical("{}  Trying to remove project {}".format(__name__, name)) 
        if name:                        
            db.delete(self.connection_project, name, DELETE_BY_NAME)
            
            if platform == "linux" or platform == "linux2":    
                send2trash(os.path.join(PROJECTS_PATH, name) )           
                #ppm_rmdir(os.path.join(PROJECTS_PATH, name) )

            if platform == "win32":                
                top = os.path.join(PROJECTS_PATH, name)
                send2trash(top)
                """
                for root, dirs, files in os.walk(top, topdown=False):
                    for name in files:
                        filename = os.path.join(root, name)
                        os.chmod(filename, stat.S_IWUSR)
                        os.remove(filename)
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(top)
                """

            
    
    

class Project:
    def __init__(self, project_name):
        self.project_name = project_name    
        
        # Connection to the database
        self.connection_project = db_u.connect(os.path.join(PROJECTS_PATH, "projects.db"))         
        self.connection_seq = db_u.connect(os.path.join(PROJECTS_PATH, self.project_name, "sequences.db"))
                
        # Creation of the database table
        db_u.create_table(self.connection_project, CREATE_PROJECTS)    
        db_u.create_table(self.connection_seq, CREATE_SEQUENCES) 
        
        
    def get_name(self):
        return self.project_name  

    
    def get_sequences(self):
        seqs = db.get_all(self.connection_seq, GET_ALL_SEQUENCES) 
        sequences = []
        for seq in seqs:
            sequences.append(seq[-1])
        return sequences    

    
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
        
    
    
#def pprint_dict(module_name, dict):
#    for key in dict.keys():
#        print (key)

    
#print ("********************** {} *************************".format(__name__))
#pprint_dict(__name__, globals())


if __name__ == "__main__":

    pass
    #prs = Projects()
    #pr = Project("CHAMACO")
    #lg.Logger.info(pr.get_project_info())
    #lg.Logger.info(pr.get_sequences())
    #prs.create_project("CHORIZO", 30, "1920x1080")
    #prs.delete_project("ROMOLA")
    
    #lg.Logger.info(prs.get_all_projects_path())
    #lg.Logger.info(prs.get_all_projects_info())

    