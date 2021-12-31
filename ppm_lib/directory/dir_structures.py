import subprocess as sub
import os


def asset_folders():
    folders = {"01_asset": {"characters": {"model":None, "lookDev": None, "rig": None},
                            "environments": {"layout": None, "lookDev": None, "model": None},
                            "props": {"lookDev": None, "model": None},
                            "vehicles": {"lookDev": None, "model": None}}}

    return folders


def reference():
    folders = {"02_reference": {"Images": None , 
                                "Video": None}}

    return folders


def edit():
    folders = {"04_edit": {"exrs": None , 
                           "proxies": None}}

    return folders


def sandbox():
    folders = {"03_sandbox": {"natalia": None, "hernan": None}}

    return folders


def sequence(sequence_name):
    folders = {"{}".format(sequence_name): {"sequence_info": None }}

    return folders


def shot(shot_name):
    folders =  {"publish": None,
                                               "work": {"anim": None,
                                                        "comp": None,
                                                        "fx":  {"geo": None , "textures": None, "render": None, "flipbooks": None,
                                                                "abc": None, "hda": None, "simulation": None,
                                                                "cameras": None},
                                                        "lighting": None,
                                                        "roto": None,
                                                        "rnd": None,
                                                        "track": None,
                                                        "photogrametry": None,
                                                        "lens_info": None,
                                                        "plate": None,
                                                        "camera": None,
                                                        "previs": None}}

    return folders




def go_folder(project_path, houdini=0, shot_number=1):
    '''Set the project_path as the current working directory
    if the second argument is 1, then the path will be set to the
    houdini working directory'''
    if not houdini:
        os.chdir(project_path)
    else:
        os.chdir(project_path + '\\Shot_{}\\work\\fx'.format(shot_number))

