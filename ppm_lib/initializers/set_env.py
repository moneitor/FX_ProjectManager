import os
import sys
from ppm_logger import logger as lg
from .init_values import HOU_VERSION, HOU_INSTALLATION




def set_env(fps, resx, resy, job, first_frame, last_frame):
    _env = os.environ
    
    abs_path = os.path.abspath(__file__)
    pwd = os.path.dirname(os.path.dirname(os.path.dirname(abs_path))    )
    hou_pipe_path = os.path.join(pwd, "houdini")
    ppm_lib = os.path.join(pwd, "ppm_lib")
    
    hfs = HOU_INSTALLATION
    user_expand_hou = "~/{}".format(HOU_VERSION)
    
    
    hh = os.pathsep.join([os.path.join(hfs, "houdini"), os.path.expanduser(user_expand_hou)])
    _env["HH"] = hh
    hpath = ":".join([hou_pipe_path, _env["HH"],_env.get("HOUDINI_PATH", "")])
    _env["HOUDINI_PATH"] = hpath
    
    
    pythonpath = os.getenv("PYTHONPATH")
    if pythonpath:
        _env["PYTHONPATH"] = ":".join([ppm_lib, _env.get("PYTHONPATH", "")])
    else:
        _env["PYTHONPATH"] = ppm_lib
        
        
    _env["FPS"] =  str(fps)
    _env["RESX"], _env["RESY"] = str(resx), str(resy)
    _env["JOB"] = job   
    _env["DFSTART"], _env["DFEND"] = str(first_frame), str(last_frame)
    
    
    lg.Logger.info("HH set to [{}]".format(hh))   
    lg.Logger.info("HOUDINI_PATH set to [{}]".format(hpath)) 
    lg.Logger.info("FPS set to [{}]".format(str(fps))) 
    lg.Logger.info("RESX, RESX set to [{}, {}]".format(str(resx), str(resy)) )
    lg.Logger.info("JOB set to [{}]".format(job)) 
    lg.Logger.info("DFSTART, DFEND set to [{}, {}]".format(str(first_frame), str(last_frame)))
    
  

    
if __name__ == "__main__":
    set_houdini_env()