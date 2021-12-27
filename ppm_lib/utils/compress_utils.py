import os
import tarfile
from file_utils import get_files_of_type
from logging_utils import logger as lg


PROJECTS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
PROJECTS_PATH = os.path.join(PROJECTS_PATH, "projects")



def tarfile_convert(path):
    with tarfile.open(path + ".tar.gz", "w:gz") as tar:
        tar.add(path, arcname=os.path.basename(path))
    tar.close
    
    
    
def tarfile_convert_files_of_type(path, type):
    files = get_files_of_type(path, type)
    
    if files:
        with tarfile.open(path + "_{}_.tar.gz".format(type), "w:gz") as tar:
            for fil in files:
                tar.add(fil, arcname=os.path.basename(fil))
                lg.Logger.info("File {} added to the tarfile".format(fil))
        tar.close
    
    
    
    
    
if __name__ == "__main__":
    TEST_PATH = PROJECTS_PATH + "/test"
    #tarfile_convert(TEST_PATH)
    tarfile_convert_files_of_type(TEST_PATH, "txt")