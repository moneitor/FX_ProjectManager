import os
import subprocess as sb
import sys
from ppm_logger import logger as lg
from initializers import set_env as set
from sys import platform


HOU_NAME = "hfs19.0.383"

def hou_run(fps=24, resx=1920, resy=1280, job="", first_frame=1001, last_frame=1100, shot_path="", project_path="", common=""):
    # set all environment variables needed for houdini    
    set.set_env(fps, resx, resy, job, first_frame, last_frame, shot_path, project_path, common)     
   
       
    # RUN HOUDINI
    if platform == "linux" or platform == "linux2":
        hou_bash_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bash_scripts/hmaster") 
        lg.Logger.info("Running LINUX")
        result = sb.run(hou_bash_path, shell=True)    
    if platform == "win32":
        hou_bash_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bash_scripts/hmaster_windows") 
        lg.Logger.info("Running WINDOWS")
        result = sb.run(hou_bash_path, shell=True)   
    
        
if __name__ == "__main__":
    hou_run(fps=60, resx=960, resy= 540, job="paquita/galleto/reyes", first_frame=1001, last_frame=1100)
