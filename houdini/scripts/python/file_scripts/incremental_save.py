from .files_handling import Houdini_Files
import hou



def houdini_version_up(file_name):
    file_handler = Houdini_Files()   
    new_version_path = file_handler.return_next_version(file_name)
    hou.hipFile.save(new_version_path, True)
    