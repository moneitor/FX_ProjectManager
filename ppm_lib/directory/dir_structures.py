import subprocess as sub
import os


def asset_folders():
    folders = {"01_Asset": {"Models": None,
                            "Textures": None}}

    return folders


def reference():
    folders = {"02_Reference": {"Images": None , 
                                "Video": None}}

    return folders


def sandbox():
    folders = {"03_Sandbox": {"Natalia": None, "Hernan": None}}

    return folders


def sequence(sequence_name):
    folders = {"{}".format(sequence_name): {"Sequence_info": None }}

    return folders


def shot(shot_name):
    folders =  {"publish": None,
                                               "work": {"anim": None,
                                                        "comp": None,
                                                        "fx":  {"Geo": None , "Textures": None, "Render": None, "Flipbooks": None,
                                                                "Abc": None, "Hda": None, "Simulation": None,
                                                                "Cameras": None},
                                                        "Lighting": None,
                                                        "Roto": None,
                                                        "RnD": None,
                                                        "Track": None,
                                                        "Photogrametry": None,
                                                        "Lens_info": None}}

    return folders




def go_folder(project_path, houdini=0, shot_number=1):
    '''Set the project_path as the current working directory
    if the second argument is 1, then the path will be set to the
    houdini working directory'''
    if not houdini:
        os.chdir(project_path)
    else:
        os.chdir(project_path + '\\Shot_{}\\work\\fx'.format(shot_number))

