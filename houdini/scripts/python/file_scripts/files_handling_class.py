import os
import sys
from increment_save import check_equal_name, return_list_files, return_version

root = r'C:\_fxProjects\_projects'


class Files_Handling():
    def __init__(self, name="", path=""):
        self.basename = name
        self.path = path

    def return_file_path(self):
        """
        Return the path to the file without the extension
        or the name of the file
        """        
        file_path = self.path.replace(self.basename , "")

        return file_path

    def return_full_path(self):
        """
        Return the path of the file with the basename and
        extension included
        """
        print("this is the full path")


    def return_file_version(self):
        """
        Return the version of the file as a string
        """
        print("this is the file version")   


    def return_path_shots_folders(self):
        print("shotsssss")


    def return_files_on_dir(self):
        """
        Return the list of Houdini files in the current folder
        """
        correct_name_list = []
        file_path = self.return_file_path()
        dir_list = os.listdir(file_path)
        for file_element in dir_list:
            if file_element.endswith(".hip") or file_element.endswith(".hipnc"):
                correct_name_list.append(file_element)

        return correct_name_list

    def return_project_folders(self):
        """Return the list of the projects that are currently in the _fxProjectsFolder"""
        projects = []
        for project in os.listdir(root):
            if not project.endswith(".json"):
                projects.append(project)
                print(project)
                
        return projects

 
    def return_shots_in_projects(self):
        pass



