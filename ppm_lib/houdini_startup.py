import os
import subprocess as sb
import sys


HOU_NAME = "hfs19.0.383"

def hou_run(fps=24, resx=1920, resy=1280):
    
    _env = os.environ
    abs_path = os.path.abspath(__file__)
    pwd = os.path.dirname(os.path.dirname(abs_path))
    ppm_lib = os.path.dirname(abs_path)

    hou_pipe_path = os.path.join(pwd, "houdini")
    hou_bash_path = os.path.join(ppm_lib, "bash_scripts/hmaster")    
    

    hfs = r"/opt/{}".format(HOU_NAME)
    user_expand = "~/{}".format(".".join([  HOU_NAME.split(".")[0],  HOU_NAME.split(".")[1]]  ) )

    _env["HH"] = os.pathsep.join([os.path.join(hfs, "houdini"), os.path.expanduser(user_expand)])
    _env["HOUDINI_PATH"] = ":".join([hou_pipe_path, _env["HH"],_env.get("HOUDINI_PATH", "")])
    
    # Set custom environment variables
    _env["FPS"] =  str(fps)
    _env["RESX"], _env["RESY"] = str(resx), str(resy)
    #_env["PYTHONPATH"] = ":".join([ppm_lib, _env.get("PYTHONPATH", "")])
    
    # RUN HOUDINI
    result = sb.run(hou_bash_path, shell=True)
    
        


if __name__ == "__main__":
    hou_run()
