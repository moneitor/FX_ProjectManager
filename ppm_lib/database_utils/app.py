import database
import os

PROJECTS_PATH = os.path.expanduser("~/Documents/FX_Project_Manager/projects/")
PROJECT_PROMPT = """\n\n --- Project Manager ---

Please choose one of the next options:

1) Add new project.
2) See all projects.
3) Find a project by name.
4) Delete project by name.
5) EXIT.

Your selection: """



def prompt_add_new_project(connection):
    name = input("Enter projec name: ")
    fps = int(input("Enter project FPS: "))
    path = os.path.join(PROJECTS_PATH, name)
            
    database.add_project(connection, name, fps, path)
    
    
    
def see_all_projects(connection):
    projects = database.get_all_projects(connection)
            
    for project in projects:
        to_print = "{}, {}, {}, {}".format(project[0], project[1], project[2], project[3] )
        print(to_print)
        
        
        
def find_project_by_name(connection):
    name = input("Enter project name: ")
    projects = database.get_project_by_name(connection, name)
            
    for project in projects:
        to_print = "{}, {}, {}, {}".format(project[0], project[1], project[2], project[3] )
        print(to_print)
        
        

def delete_project(connection):
    name = input("Enter project name: ")
    projects = database.delete_project_by_name(connection, name)
    
    print ("Project {} deleted".format(name))
    


def menu():
    connection = database.connect()
    database.create_tables(connection)
    
    while  (user_input := input(PROJECT_PROMPT)) != "5":
        if user_input == "1":
            prompt_add_new_project(connection)

            
        elif user_input == "2":
            see_all_projects(connection)

                
                
        elif user_input == "3":
            find_project_by_name(connection)
            
        
        elif user_input == "4":
            delete_project(connection)           

        
        else:
            print ("Invalid input, please try again.")
        
        
menu()