import files.file_utils as fu
import os
import OpenEXR as exr


PROJECTS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
PROJECTS_PATH = os.path.join(PROJECTS_PATH, "projects/test2")


exr_files = fu.get_files_of_type(PROJECTS_PATH, "exr")

exr_obj = exr.InputFile(exr_files[1])

for k,v in exr_obj.header().items():
    print(k, v)