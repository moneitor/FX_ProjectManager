import sqlite3
import sqlite3
import os



projects = os.path.dirname(os.path.abspath(__file__)) + "/databases/projects.db"


CREATE_PROJECTS = 'CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, fps INTEGER, path TEXT);'
INSERT_PROJECT = 'INSERT INTO projects (name, fps, path) VALUES (?, ?, ?);'
GET_ALL_PROJECTS = 'SELECT * FROM projects'
GET_PROJECT_BY_NAME = 'SELECT * FROM projects WHERE name = ?;'
DELETE_BY_NAME = 'DELETE FROM projects WHERE name = ?;'



def connect():
    return sqlite3.connect("./databases/projects.db")



def create_tables(connection): 
    with connection:      
        return connection.execute(CREATE_PROJECTS).fetchall()
        
        
        
def add_project(connection, name, fps, path):
    with connection:
        return connection.execute(INSERT_PROJECT, (name, fps, path)).fetchall()
        


def get_all_projects(connection):
    with connection:
        return connection.execute(GET_ALL_PROJECTS).fetchall()
        
    
    
def get_project_by_name(connection, name):
    with connection:
        return connection.execute(GET_PROJECT_BY_NAME, (name,)).fetchall()
    

def delete_project_by_name(connection, name):
    with connection:
        return connection.execute(DELETE_BY_NAME, (name,)).fetchall()
    