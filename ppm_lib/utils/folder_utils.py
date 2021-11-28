import subprocess as sub
import os


def asset_folders():
    folders = {"01_Asset": {"Models": None,
                            "Textures": None}}

    return folders


def design_folders():
    folders = {"02_Textures": {"HDRI":None,
                             "JPGs": None,
                             "EXR": None}}
    return folders

def reference():
    folders = {"03_Reference": {"Images": None , "Video": None}}

    return folders


def sequence(sequence_name):
    folders = {"{}".format(sequence_name): {"Sequence_info": None }}

    return folders

def sandbox():
    folders = {"04_Sandbox": {"Natalia": None, "Hernan": None}}

    return folders


def shot(sequence, shot_number):
    folders = {"Shot_{}".format(shot_number): {"publish": None,
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
                                                        "Lens_info": None}}}

    return folders



def make_dirs_from_dict(direct, current_dir='./'):

    for key, values in direct.items():
        pathFolder = os.path.join(current_dir, key)
        if not os.path.exists(pathFolder):
            os.mkdir(pathFolder)
            if type(values) == dict:
                make_dirs_from_dict(values, os.path.join(current_dir, key))



def create_folders_project(path):
    make_dirs_from_dict(asset_folders(), path)
    make_dirs_from_dict(design_folders(), path)
    make_dirs_from_dict(reference(), path)
    make_dirs_from_dict(sandbox(), path)


def create_sequence_folder(sequence_name, path):
    make_dirs_from_dict(sequence(sequence_name), path)
    


def go_folder(project_path, houdini=0, shot_number=1):
    '''Set the project_path as the current working directory
    if the second argument is 1, then the path will be set to the
    houdini working directory'''
    if not houdini:
        os.chdir(project_path)
    else:
        os.chdir(project_path + '\\Shot_{}\\work\\fx'.format(shot_number))

