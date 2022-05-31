from .project import Project
from ppm_logger import logger as lg
from directory.directory_utils import ppm_mkdir, ppm_rmdir
from db import database_interface as db
from db import database_utils as db_u
import os
from sys import platform
import stat
from send2trash import send2trash # library to send stuff to the bin

######################### COMANDS ###################################
#CREATE_SEQUENCES = 'CREATE TABLE IF NOT EXISTS sequences (id INTEGER PRIMARY KEY, name TEXT, fps INTEGER, resolution TEXT, path TEXT);'
CREATE_SEQUENCES = 'CREATE TABLE IF NOT EXISTS sequences (id INTEGER PRIMARY KEY, name TEXT, path TEXT);'
#CREATE_SHOTS = 'CREATE TABLE IF NOT EXISTS shots (id INTEGER PRIMARY KEY, name TEXT, fps INTEGER, resolution TEXT, path TEXT);'
CREATE_SHOTS = 'CREATE TABLE IF NOT EXISTS shots (id INTEGER PRIMARY KEY, name TEXT, firstFrame INTEGER, lastFrame INTEGER, path TEXT);'



#INSERT_SEQUENCE = 'INSERT INTO sequences (name, fps, resolution, path) VALUES (?, ?, ?, ?);'
INSERT_SEQUENCE = 'INSERT INTO sequences (name, path) VALUES (?, ?);'

GET_ALL_SEQUENCES = 'SELECT * FROM sequences'
GET_ALL_SHOTS = 'SELECT * FROM shots'

GET_SEQUENCE_BY_NAME = 'SELECT * FROM sequences WHERE name = ?;'
DELETE_BY_NAME = 'DELETE FROM sequences WHERE name = ?;'


#######################################################################
PROJECTS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
PROJECTS_PATH = os.path.join(PROJECTS_PATH, "projects")




class Sequences:
    
    def __init__(self, project):
        if isinstance(project, Project):
            self.prj = project
        self.project_name = self.prj.get_name()    
        self.project_path = self.prj.get_path()  
        self.project_basedir = os.path.dirname(self.project_path)  
        
        # Connection to the databases 
        self.connection_seq = db_u.connect(os.path.join(self.project_path, "sequences.db")) 
        
        # Creation of the database table
        db_u.create_table(self.connection_seq, CREATE_SEQUENCES)    
    
    
    def add_sequence(self, sequence_name):
        
        """Creates the sequence folder"""      
        sequence_path = os.path.join(self.project_path,  sequence_name)   
        lg.Logger.warning(sequence_path)
        
        if not db.find_by_name(self.connection_seq, sequence_name, GET_SEQUENCE_BY_NAME):
            db.add_new_sequence(self.connection_seq, sequence_name, sequence_path, INSERT_SEQUENCE)      
        
            if os.path.exists(self.project_path):                
                ppm_mkdir(sequence_path)         
                
        else:
            lg.Logger.warning("Sequence [{}] already exists".format(sequence_name)) 
            
            
    
    def get_sequences(self):
        """
        Returns a list of Sequences() objects
        """
        sequences = []
        sequence_db = db.get_all(self.connection_seq, GET_ALL_SEQUENCES)
        for sequence in sequence_db:
            current_sequence = Sequence(self.prj, sequence[1])
            sequences.append(current_sequence)
            
        return sequences  
             
            
    
    
    def get_sequences_names(self):
        names = []
        seqs = self.get_sequences()
        for seq in seqs:    
            names.append(seq.get_name())            
        
        return names        
        
    
    def get_sequences_path(self):
        paths = []
        seqs = self.get_sequences()
        for seq in seqs:    
            paths.append(seq.get_path())
        lg.Logger.info(paths)     
        
    
        
    def delete_sequence(self, sequence_name):
        sequence_path = os.path.join(self.project_path,  sequence_name)
        
        if os.path.exists(sequence_path):
            db.delete(self.connection_seq, sequence_name, DELETE_BY_NAME)     
            
            if platform == "linux" or platform == "linux2":    
                send2trash(sequence_path) 
                #ppm_rmdir(sequence_path)
            
            if platform == "win32":
                print(sequence_path)
                #send2trash(sequence_path)
                print ("Folders can't be deleted from Windows yet, so please go ahead and remove the folder manually. ")
                """
                top = sequence_path
                for root, dirs, files in os.walk(top, topdown=False):
                    for name in files:
                        filename = os.path.join(root, name)
                        os.chmod(filename, stat.S_IWUSR)
                        os.remove(filename)
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(top)
                """
        
            
        
    
    
    
class Sequence:
    def __init__(self, project, seq_name):
        if isinstance(project, Project):
            self.prj = project
        self.project_name = self.prj.get_name()
        self.seq_name = seq_name              
        self.project_path = self.prj.get_path()  
        self.project_basedir = os.path.dirname(self.project_path)  
           
        # Connection to the database         
        if os.path.exists(self.project_path):       
            self.connection_seq = db_u.connect(os.path.join(self.project_path, "sequences.db")) 
        if os.path.exists(os.path.join(self.project_path,  self.seq_name, "shots.db")):            
            self.connection_shot = db_u.connect(os.path.join(self.project_path,  self.seq_name, "shots.db"))       
                
        # Creation of the database table
        db_u.create_table(self.connection_seq, CREATE_SEQUENCES)      


    
    def get_shots(self):
        sh = db.get_all(self.connection_shot, GET_ALL_SHOTS)
        shots = []
        for s in sh:
            shots.append(s[-1])
            
        return shots  
    
    
    def get_name(self):
        seq = db.find_by_name_sequence(self.connection_seq, self.seq_name, GET_SEQUENCE_BY_NAME)
        if seq != None:
            seq = seq.split(",")[1].strip()
            return seq
        
    
    
    def get_path(self):
        path = db.find_by_name_sequence(self.connection_seq, self.seq_name, GET_SEQUENCE_BY_NAME)
        if path != None:
            path = path.split(",")[-1].strip()
            return path
    
    
    

if __name__ == "__main__":
    sqs = Sequences("CHAMACO")
    sq = Sequence("CHAMACO", "ddd")
    #sqs.create_sequence("aaa")    
    #sqs.create_sequence("bbb")   
    #sqs.create_sequence("ccc")   
    #sqs.create_sequence("ddd")  
    #sqs.delete_sequence("aaa") 
    #sqs.get_sequences_path()
    lg.Logger.info(sq.get_path())
    
    
    
    