import sqlite3
from logging_utils import logger as lg






def connect(connection):
    return sqlite3.connect(connection)



def create_table(connection, cmd): 
    with connection:      
        return connection.execute(cmd).fetchall()
        
        
        
def add(connection, name, fps, resolution, path, cmd):
    with connection:
        return connection.execute(cmd, (name, fps, resolution, path)).fetchall()
        


def get_all(connection, cmd):    
    with connection:        
        return connection.execute(cmd).fetchall()
        
    
    
def get_by_name(connection, name, cmd):
    with connection:        
        return connection.execute(cmd, (name,)).fetchall()
    

def delete_by_name(connection, name, cmd):
    with connection:
        return connection.execute(cmd, (name,)).fetchall()
    
    

if __name__ == "__main__":
    lg.Logger.info("test")