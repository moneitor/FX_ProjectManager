from .sequence import Sequence
from ppm_logger import logger as lg
from directory.directory_utils import ppm_rmdir, make_dirs_from_dict
from db import database_interface as db
from db import database_utils as db_u
from directory import dir_structures as ds
import os
from PySide2.QtWidgets import QMessageBox
from sys import platform

######################### COMANDS ###################################

CREATE_SHOTS = 'CREATE TABLE IF NOT EXISTS shots (id INTEGER PRIMARY KEY, name TEXT, firstFrame INTEGER, lastFrame INTEGER, path TEXT);'

INSERT_SHOT = 'INSERT INTO shots (name, firstFrame, lastFrame, path) VALUES (?, ?, ?, ?);'
GET_ALL_SHOTS = 'SELECT * FROM shots'
GET_SHOT_BY_NAME = 'SELECT * FROM shots WHERE name = ?;'
DELETE_BY_NAME = 'DELETE FROM shots WHERE name = ?;'






class Shots:
    def __init__(self, sequence):
        if sequence:      
            if sequence.get_name() == None:
                lg.Logger.critical("The given sequence is not initialized correctly")
                return  
            
            if isinstance(sequence, Sequence):
                self.sequence = sequence           
            
        else:
            return
        self.sequence_name = self.sequence.get_name()
        self.sequence_path = self.sequence.get_path()
        self.sequence_basedir = os.path.dirname(self.sequence_path)
        
        # Connection to the database       
        self.connection_shot = db_u.connect(os.path.join(self.sequence_path, "shots.db"))
        
        # Creation of the database table
        db_u.create_table(self.connection_shot, CREATE_SHOTS)
    
    
    def add_shot(self, shot_name, first_frame, last_frame):
        shot_path = os.path.join(self.sequence_path, shot_name)
        
        if not db.find_by_name(self.connection_shot, shot_name, GET_SHOT_BY_NAME):
            db.add_new_shot(self.connection_shot, shot_name, first_frame, last_frame, shot_path, INSERT_SHOT)
            
            if os.path.exists(self.sequence_path):    
                          
                shot_dict = ds.shot(shot_name)                
                make_dirs_from_dict(shot_path, shot_dict)
                
        else:
            lg.Logger.warning("Shot [{}] already exists".format(shot_name))            
            return False
            
            
    def get_shots(self):
        """
        Returns a list of Sequences() objects
        """
        shots = []
        shots_db = db.get_all(self.connection_shot, GET_ALL_SHOTS)
        for shot in shots_db:
            current_shot = Shot(self.sequence, shot[1])
            shots.append(current_shot)
            
        return shots    
    

    
    
    def get_shot_names(self):
        names = []
        shots = self.get_shots()
        for shot in shots:
            names.append(shot.get_name())
            lg.Logger.info(shot.get_name())
        return names
        
    
    
    def get_shots_path(self):
        paths = []
        shots = self.get_shots
        for shot in shots:
            paths.append(shot.get_path())
            lg.Logger.info(shot.get_path())
        return paths     
    
    
        
    def delete_shot(self, shot_name):
        shot_path = os.path.join(self.sequence_path, shot_name)
        
        if os.path.exists(shot_path):
            db.delete(self.connection_shot, shot_name, DELETE_BY_NAME)
            
            if platform == "linux" or platform == "linux2":
                ppm_rmdir(shot_path)
                
            if platform == "win32":
                top = shot_path
                for root, dirs, files in os.walk(top, topdown=False):
                    for name in files:
                        filename = os.path.join(root, name)
                        os.chmod(filename, stat.S_IWUSR)
                        os.remove(filename)
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
        else:
            lg.Logger.warning("Shot [{}] does not exist.".format(shot_name))
    
    

class Shot:
    def __init__(self, sequence, shot_name):
        if isinstance(sequence, Sequence):
            self.sequence = sequence
        if sequence.get_name() == None:
            lg.Logger.critical("The given sequence is not initialized correctly")
            return
        self.sequence_name = self.sequence.get_name()
        self.shot_name = shot_name
        self.sequence_path = self.sequence.get_path()
        
        # Connection to the database       
        self.connection_shot = db_u.connect(os.path.join(self.sequence_path, "shots.db"))
        
        # Creation of the database table
        db_u.create_table(self.connection_shot, CREATE_SHOTS)
        
        
    def get_name(self):
        return self.shot_name
    
    
    def get_first_frame(self):
        path = db.find_by_name_shot(self.connection_shot, self.shot_name, GET_SHOT_BY_NAME)   
        if path != None:
            first_frame = path.split(",")[2].strip()            
            return int(first_frame)
    
    
    def get_last_frame(self):
        path = db.find_by_name_shot(self.connection_shot, self.shot_name, GET_SHOT_BY_NAME)   
        if path != None:
            last_frame = path.split(",")[3].strip()            
            return int(last_frame)
    
    
    def get_path(self):                   
        path = db.find_by_name_shot(self.connection_shot, self.shot_name, GET_SHOT_BY_NAME)   
        if path != None:
            path = path.split(",")[-1].strip()            
            return path 
                
        
   
    

        
        