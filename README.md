## FX Personal Project Manager

Hi there.

With the goal of learning and getting better at python, and maybe along the way creating something that might help me out with the structure of my personal 
projects in the future, I decided to slowly create a set of tools that kind of work like a simple vfx pipeline for personal projects.

This is still work in progress and will remain like that for the long term.


There are VEX Snippets that you might find useful inside:
**FX_ProjectManager/ppm_lib/snippets/vexSnippets/**

####      Project manager window
Main hub that stores most of the functionalities that are not going to be run directly from the DCCs
![](images/main_window.jpeg)

####      New Project window
Allows to create new projects and adds them to the database
![](images/new_project.jpeg)

####      New Sequence window
Given the selected project, will allow the user to add a new sequence and will store it on the database
![](images/new_sequence.jpeg)

####      New Shot window
Given the selected sequence, will allow the user to create a new shot whose name will be the union of the sequence name 
and the shot number
![](images/new_shot.jpeg)

####      File Renamer window
Work in progress, allows to rename files, offset the frame range, fix padding issues, and eventually will be a work with an instance of a FileSequence() object that will allow all the functionalities needed by a sequence of files.
![](images/renamer.jpeg)
