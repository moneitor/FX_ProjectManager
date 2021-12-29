from .project import Project
from ppm_logger import logger as lg
from directory.directory_utils import ppm_mkdir, ppm_rmdir
from db import database_interface as db
from db import database_utils as db_u
import os

######################### COMANDS ###################################
CREATE_SEQUENCES = 'CREATE TABLE IF NOT EXISTS sequences (id INTEGER PRIMARY KEY, name TEXT, fps INTEGER, resolution TEXT, path TEXT);'
INSERT_SEQUENCE = 'INSERT INTO sequences (name, fps, resolution, path) VALUES (?, ?, ?, ?);'
GET_ALL_SEQUENCES = 'SELECT * FROM sequences'
GET_SEQUENCE_BY_NAME = 'SELECT * FROM sequences WHERE name = ?;'
DELETE_BY_NAME = 'DELETE FROM sequences WHERE name = ?;'


#######################################################################
PROJECTS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
PROJECTS_PATH = os.path.join(PROJECTS_PATH, "projects/")




class Sequences:
    
    def __init__(self, project):
        if isinstance(project, Project):
            self.prj = project
        self.project_name = self.prj.get_name()    
        self.project_path = self.prj.get_path()    
        
        # Connection to the databases 
        self.connection_seq = db_u.connect(os.path.join(PROJECTS_PATH, self.project_name, "sequences.db")) 
        
        # Creation of the database table
        db_u.create_table(self.connection_seq, CREATE_SEQUENCES)    
    
    
    def add_sequence(self, sequence_name):
        
        """Creates the sequence folder"""      
        sequence_path = os.path.join(self.project_path,  sequence_name)   
        lg.Logger.warning(sequence_path)
        
        if not db.find_by_name(self.connection_seq, sequence_name, GET_SEQUENCE_BY_NAME):
            db.add_new(self.connection_seq, sequence_name, -1, "NA", sequence_path, INSERT_SEQUENCE)      
        
            if os.path.exists(self.project_path):                
                ppm_mkdir(sequence_path)         
                
        else:
            lg.Logger.warning("Sequence [{}] already exists".format(sequence_name))   
            
            
    def get_sequences_info(self):
        
        seqs = []
        sequences = db.get_all(self.connection_seq, GET_ALL_SEQUENCES)        
        
        for sequence in sequences:
            seqs.append(sequence)           
        
        return seqs  
    
    
    def get_sequences_names(self):
        names = []
        seqs = self.get_sequences_info()
        for seq in seqs:    
            names.append(seq[1])
        lg.Logger.info(names)        
        
    
    def get_sequences_path(self):
        paths = []
        seqs = self.get_sequences_info()
        for seq in seqs:    
            paths.append(seq[-1])
        lg.Logger.info(paths)     
    
        
    def delete_sequence(self, sequence_name):
        db.delete(self.connection_seq, sequence_name, DELETE_BY_NAME)
        sequence_path = os.path.join(self.project_path,  sequence_name) 
        ppm_rmdir(sequence_path)
        
        
            
        
    
    
    
class Sequence:
    def __init__(self, project, seq_name):
        if isinstance(project, Project):
            self.prj = project
        self.project_name = self.prj.get_name()
        self.seq_name = seq_name        
        # Connection to the database        
        self.connection_seq = db_u.connect(os.path.join(PROJECTS_PATH, self.project_name, "sequences.db")) 
        
        
        # Creation of the database table
        db_u.create_table(self.connection_seq, CREATE_SEQUENCES)    
    

    def get_shots(self):
        pass
    
    
    def get_path(self):
        path = db.find_by_name(self.connection_seq, self.seq_name, GET_SEQUENCE_BY_NAME)
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
    
    
    
    