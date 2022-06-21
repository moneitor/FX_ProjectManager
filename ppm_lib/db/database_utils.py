import sqlite3
from db import DB_ContextManager as DB



def connect(connection):
    return sqlite3.connect(connection)



def create_table(connection, cmd): 
    with connection:      
        return connection.execute(cmd).fetchall()
        
        

## PROJECTS #####################################################################
def add(connection, name, fps, resolution, path, cmd):
    with connection:
        return connection.execute(cmd, (name, fps, resolution, path)).fetchall()
        

       
    
## SEQUENCES #####################################################################
def add_sequence(connection, name, path, cmd):
    with connection:
        return connection.execute(cmd, (name, path)).fetchall()



## SHOTS #########################################################################
def add_shot(connection, name, firstFrame, lastFrame, path, cmd):
    with connection:
        return connection.execute(cmd, (name, firstFrame, lastFrame, path)).fetchall()




## GENERIC DATABASE FUNCTIONS
def get_all(connection, cmd):    
    with connection:        
        return connection.execute(cmd).fetchall()        
    
    
def get_by_name(connection, name, cmd):
    with connection:        
        return connection.execute(cmd, (name,)).fetchall()
    

def delete_by_name(connection, name, cmd):
    with connection:
        return connection.execute(cmd, (name,)).fetchall()


def edit_by_name(connection, name, cmd):
    with connection:
        return connection.execute(cmd, (name,)).fetchall()
    
    

