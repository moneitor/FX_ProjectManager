import os
import sys
from files import file_utils


class Houdini_Files():
    def __init__(self):
        self._shot_path = os.getenv("SHOTPATH")  
        self._work_path = os.path.join(self._shot_path, "work", "fx")    
        self._file_paths = []  
        self._files = []   
        self._max_version_path = ""             
        
        
    def return_files(self):
        """
        Return all the existing paths to a houdini file in the working folder
        """
        self._file_paths = [file for file in file_utils.get_files_of_type(self._work_path, "hipnc") if "backup" not in file]
        return self._file_paths
        
        
    def return_file_names(self):
        """
        Return all the existing file names in the working folder
        """
        self.return_files()
        self._files = [os.path.basename(file) for file in self._file_paths]
        return self._files
    
    
    def return_last_version(self):
        """
        Return the path to the file with the last version
        """
        self.return_file_names()
        current_version = 0
        max_version_file = ""
        
        for file in self._files:
            version = os.path.splitext(file)[0].split("_v")[-1]
            version = version.lstrip("0")
            version_as_int = int(version)
            if version_as_int > current_version:
                current_version = version_as_int
                max_version_file = file
                self._max_version_path = os.path.join(self._work_path, max_version_file)
                
        if os.path.isfile(self._max_version_path):            
            return self._max_version_path
        
        
    def return_full_path(self, file_name):
        full_path = os.path.join(self._work_path, file_name)
        
        return full_path
            
        
        
        