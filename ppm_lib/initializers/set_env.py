import os
from sys import platform
from ppm_logger import logger as lg
from dotenv import load_dotenv


dotenv_path = "../.env"


def set_env(fps, resx, resy, job, first_frame, last_frame, shot_path, project, common):
    
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)    
        
        lg.Logger.info(os.getenv("HOU_INSTALLATION"))
        lg.Logger.info(os.getenv("HOU_VERSION"))

        HOU_VERSION = os.getenv("HOU_VERSION")
        HOU_INSTALLATION = os.getenv("HOU_INSTALLATION")

    else:
        lg.Logger.warning("Please make sure '.env' file exist on the root directory of FX_ProjectManager. ")
    
    
    _env = os.environ
    
    abs_path = os.path.abspath(__file__)
    pwd = os.path.dirname(os.path.dirname(os.path.dirname(abs_path))    )
    hou_pipe_path = os.path.join(pwd, "houdini")
    ppm_lib = os.path.join(pwd, "ppm_lib")
    
    hfs = HOU_INSTALLATION
   
    if platform == "linux" or platform == "linux2":
        user_expand_hou = os.path.join("~", HOU_VERSION)    
        
    
    if platform == "win32":
        user_expand_hou = os.path.join("~", "Documents", HOU_VERSION)          

    
    hh = os.pathsep.join([os.path.join(hfs, "houdini"), os.path.expanduser(user_expand_hou)])
    _env["HH"] = hh
    
    
    ##### Setting HOUDINI_PATH
    #if platform == "linux" or platform == "linux2":
    #    hpath = ":".join([hou_pipe_path, common, _env["HH"],_env.get("HOUDINI_PATH", "")])
        #_env["HOUDINI_PATH"] = hpath   
    _env["HOUDINI_PATH"]  = hou_pipe_path
    _env["HOUDINI_PATH"]  += os.pathsep + common + os.pathsep + _env["HH"] + os.pathsep + _env.get("HOUDINI_PATH", "")
        
    
    #if platform == "win32":
    #    hpath = ";".join([hou_pipe_path, common, _env["HH"],_env.get("HOUDINI_PATH", "")])
    #    _env["HOUDINI_PATH"] = hpath
        
    
    ##### Setting HOUDINI_OTLSCAN_PATH
    #if platform == "linux" or platform == "linux2":  
    
 
        
        
    base_folder = os.path.dirname(HOU_INSTALLATION) # Base folder where houdini is installed
    if platform == "linux" or platform == "linux2":    
    
        fxlabs_version = HOU_VERSION.replace("hfs", "SideFXLabs") # path to folder where SideFXLabs tools are installed
        
        
    if platform == "win32":
        fxlabs_version = HOU_VERSION.replace("houdini", "SideFXLabs") # path to folder where SideFXLabs tools are installed
        
        
        
    _env['HOUDINI_OTLSCAN_PATH'] = os.path.join(common, "houdini", "otls")
    _env['HOUDINI_OTLSCAN_PATH'] += os.pathsep + os.path.join(base_folder, "sidefx_packages", fxlabs_version, "otls")
    _env['HOUDINI_OTLSCAN_PATH'] += os.pathsep + os.path.join(HOU_INSTALLATION, "houdini", "otls")
    _env['HOUDINI_OTLSCAN_PATH'] += os.pathsep + os.path.join(HOU_INSTALLATION, "packages", "kinefx", "otls")
        
        
        
    """
    if platform == "win32":        
        houdini_otlscan_path = ";".join( [_env.get("HOUDINI_PATH", ""), os.path.join(common, "houdini", "otls")])
        _env["HOUDINI_OTLSCAN_PATH"] = houdini_otlscan_path
    """
        

    
    pythonpath = os.getenv("PYTHONPATH")
    if pythonpath:
        _env["PYTHONPATH"] = ":".join([ppm_lib, _env.get("PYTHONPATH", "")])
    else:
        _env["PYTHONPATH"] = ppm_lib
        
        
    _env["FPS"] =  str(fps)
    _env["RESX"], _env["RESY"] = str(resx), str(resy)
    _env["JOB"] = job   
    _env["DFSTART"], _env["DFEND"] = str(first_frame), str(last_frame)
    _env["SHOT"] = shot_path
    _env["PROJECT"] = project
    _env["PPM_COMMON"] = common
    _env["PPM_COMMON_HOU"] = os.path.join(common, "houdini")
    _env["PPM_OTLSCAN_PATH"] = os.path.join(common, "houdini", "otls")
    _env["H_INSTALL"] = hfs
    
    
    lg.Logger.info("HH set to [{}]".format(hh))   
    lg.Logger.info("HOUDINI_PATH set to [{}]".format(_env["HOUDINI_PATH"])) 
    lg.Logger.info("FPS set to [{}]".format(str(fps))) 
    lg.Logger.info("RESX, RESX set to [{}, {}]".format(str(resx), str(resy)) )
    lg.Logger.info("JOB set to [{}]".format(job)) 
    lg.Logger.info("DFSTART, DFEND set to [{}, {}]".format(str(first_frame), str(last_frame)))
    
  

    
if __name__ == "__main__":
    set_env()