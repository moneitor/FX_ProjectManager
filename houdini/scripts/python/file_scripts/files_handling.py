from hashlib import new
import os
import sys
from files import file_utils
from datetime import datetime


class Houdini_Files():
    def __init__(self):
        self._shot_path = os.getenv("SHOT")  
        self._work_path = os.path.join(self._shot_path, "work", "fx")    
        self._file_paths = []  
        self._files = []   
        self._max_version_path = ""             
        
        
    def return_files(self):
        """
        Return all the existing paths to a houdini file in the working folder
        """
        _hiplc = file_utils.get_files_of_type(self._work_path, "hiplc")
        _hipnc = file_utils.get_files_of_type(self._work_path, "hipnc")
        _hip = file_utils.get_files_of_type(self._work_path, "hip")
        
        _file_paths_hiplc = None
        _file_paths_hipnc = None
        _file_paths_hip =  None
        
        
        if _hiplc:
            _file_paths_hiplc = [file for file in _hiplc if "backup" not in file]
        if _hipnc:
            _file_paths_hipnc = [file for file in _hipnc if "backup" not in file]
        if _hip:
            _file_paths_hip = [file for file in _hip if "backup" not in file]
        
        if _file_paths_hiplc:
            self._file_paths = _file_paths_hiplc 
        if _file_paths_hipnc:
            self._file_paths += _file_paths_hipnc 
        if _file_paths_hip:
            self._file_paths += _file_paths_hip 
        
        
        return self._file_paths

 
        
    def return_file_names(self):
        """
        Return all the existing file names in the working folder
        """
        self.return_files()
        print(self.return_files())
        self._files = [os.path.basename(file) for file in self._file_paths]
        return self._files
    
    
    def return_last_version(self, file_name):
        """
        Return the path to the file with the last version
        """
        file_name = os.path.basename(file_name)        
        
        file_name_fixed = file_name.split("_")[2]
        
        all_files = self.return_file_names()
        
        specific_files = [file for file in all_files if file_name_fixed in file]        
        
        current_version = 0
        max_version_file = ""
        
        for file in specific_files:
            version = os.path.splitext(file)[0].split("_v")[-1]
            version = version.lstrip("0")
            version_as_int = int(version)
            if version_as_int > current_version:
                current_version = version_as_int
                max_version_file = file
                self._max_version_path = os.path.join(self._work_path, max_version_file)
                
        if os.path.isfile(self._max_version_path):   
            
            return self._max_version_path
        
        
    def return_next_version(self, file_name):       
          
        last_version_path = self.return_last_version(file_name)     
        last_version_name = os.path.basename(last_version_path)          
        get_version_string = last_version_name.split("_v")[-1].split(".")[0] 
        stripped_version = get_version_string.lstrip("0")
        new_version = str(int(stripped_version) + 1)
        new_version = new_version.zfill(3)  
        
        current_version_path = file_name
        current_version_name = os.path.basename(current_version_path)
        current_version_string = current_version_name.split("_v")[-1].split(".")[0] 
        current_stripped_version = current_version_string.lstrip("0")
        current_version = str(current_stripped_version)
        current_version = current_version.zfill(3)       
                 
        
        new_version_full_path = file_name.replace("_v" + current_version, "_v" + new_version)
        print("NEW   ", "_v" + current_version, "_v" + new_version)    
        print(new_version_full_path)    
        
        return new_version_full_path       
        

    def return_full_path(self, file_name):
        full_path = os.path.join(self._work_path, file_name)
        
        return full_path
    
    
    def return_file_info(self, file_name):
        
        full_file_path = os.path.join(os.getenv("SHOT"), "work", "fx", file_name)
        
        time_last_modified = datetime.fromtimestamp(  os.path.getmtime(full_file_path)  ).strftime('%Y-%m-%d %H:%M:%S')
        time_created = datetime.fromtimestamp(  os.path.getctime(full_file_path)  ).strftime('%Y-%m-%d %H:%M:%S')
        size = str(  round(  float(os.path.getsize(full_file_path)) / ( 1024 * 1024 ),  3))
        
        
        return time_last_modified, size
        
            
        
        
        