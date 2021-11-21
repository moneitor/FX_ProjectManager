import os
import hou
from difflib import SequenceMatcher

basename = hou.hipFile.basename()
path = hou.hipFile.path()


def check_equal_name(name, nameFile):
    """
    Check if the name of the current file and the names in the list of files
    are the same so we check the version of the correct files
    """
    start_name = name.split("_")[:2]
    start_nameFile = nameFile.split("_")[:2]

    if start_name == start_nameFile:
        return True

def return_list_files():
    """
    Uses the function check_equal_name to work
    Return a list of all the files contained in the project folder
    """
    correct_name_list = []
    file_path = path.replace(basename , "")
    dir_list = os.listdir(file_path)
    for file_hip in dir_list:
        if check_equal_name(file_hip, basename):
            correct_name_list.append(file_hip)           

    return correct_name_list, file_path

def return_version():
    """
    Uses the return_list_files function to work
    Return the maximum version contained in the folder
    """
    max_version = 0
    versions = []
    for _file in return_list_files()[0]:
        if (_file.endswith(".hip") or _file.endswith(".hipnc")) and "VER" in _file:
            version = _file.split(".")[0].split("_")[-1].split("R")[-1]
            versions.append(version)
            max_version = max(versions)
            max_version = int(max_version)

    return max_version

def change_name():
    """
    Update the VER part to have the newer version number for 
    example if VER1 is the current version then the 
    next version is gonna be VER2
    """
    current_version_str = return_version()
    current_version_int = int(current_version_str) 
    new_version_int = current_version_int + 1
    new_version_str = str(new_version_int)
    current_VER = "VER{}".format(current_version_str)
    new_VER = "VER{}".format(new_version_str)

    print("\n------------------\n")
    print("current----" + current_VER)
    print("current----" + new_VER)
    print("\n------------------\n")

    current_basename = basename
    new_basename = basename.replace(current_VER, new_VER)

    print(current_basename)
    print(new_basename)

    print("\n------------------\n")

    current_basename = ""
    
    return new_basename

def save_increment():
    """
    Saves the file using the new name
    based on the increased version
    """

    file_path = return_list_files()[1]
    new_name = change_name()

    new_path = file_path + new_name

    print(file_path)
    print(new_name)
    print(new_path)

    print("\n------------------\n")

    hou.hipFile.save(new_path, True)

    print("Saved file {}".format(new_name))

    
    

