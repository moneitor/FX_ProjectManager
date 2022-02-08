## FX Personal Project Manager
#### Using Python 3.8.10

Hi there.

I am a Senior Houdini FXTD and CG Supervisor at Framestore.

With the goal of learning and getting better at python, and maybe along the way creating something that might help me out with the structure of my personal 
projects in the future, I decided to slowly create a set of tools that kind of work like a simple vfx pipeline for personal projects.

This is still work in progress and will remain like that for the long term.


There are VEX Snippets that you might find useful inside:
**FX_ProjectManager/ppm_lib/snippets/vexSnippets/**


### Installation steps

 * Create a virtualenvironment inside the FX_ProjectManager folder and install the python dependecies defined on the **requirements.txt**.
 * Run ```pip install -r requirements.txt```. This will install the python libraries required. On Windows you might need a different version of the same libraries
 * rename the ```./.env_example``` to ```./env``` and update it's contents to point to the installation folders on your system

The **first part** of the manager is in charge of creation and modification of projects, sequences and shots, Modification of file sequences, ingesting of plates, conversion from DNG to EXR.

The **second part** of the manager is software based and works from inside each DCC "Nuke, and Houdini", which will let you open and save files, version up, manage versioning of caches, publishing of setups etc.

## First part

####      Project manager window
![](images/main_window.jpeg)

Main hub that stores most of the functionalities that are not going to be run directly from the DCCs

####      New Project window
![](images/new_project.jpeg)

Allows to create new projects and adds them to the database

####      New Sequence window
![](images/new_sequence.jpeg)

Given the selected project, will allow the user to add a new sequence and will store it on the database

####      New Shot window
![](images/new_shot.jpeg)

Given the selected sequence, will allow the user to create a new shot whose name will be the union of the sequence name 
and the shot number

####      File Renamer window
![](images/renamer.jpg)

Work in progress, allows to rename files, offset the frame range, fix padding issues, and eventually will be a work with an instance of a FileSequence() object that will allow all the functionalities needed by a sequence of files.


## Houdini

#### PPM Shelf
![](images/PPM_Shelf.png)
The main Houdini functionalities are part of the PPM_Lib shelf tool


#### Open file
![](images/openFile.png)

Displays the files saved in the current shot.

#### Save new file
![](images/savingFile.png)

Displays the files saved in the current shot.

