import sqlite3



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
    
    
    
def add_sequence(connection, name, path, cmd):
    with connection:
        return connection.execute(cmd, (name, path)).fetchall()
    
    
    
def add_shot(connection, name, firstFrame, lastFrame, path, cmd):
    with connection:
        return connection.execute(cmd, (name, firstFrame, lastFrame, path)).fetchall()
    
    

