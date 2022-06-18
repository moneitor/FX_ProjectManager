import hou
import os
import sys

# Initialization of the framerange to the proper range
#hou.playbar.setFrameRange(int(os.getenv("DFSTART")), int(os.getenv("DFEND")))
#hou.playbar.setPlaybackRange(int(os.getenv("DFSTART")), int(os.getenv("DFEND")))
#hou.playbar.jumpToNextKeyframe()

hou.playbar.setRealTime(True)

# Set the desktop to ppm
desktops_dict = dict((d.name(), d) for d in hou.ui.desktops())
desktops_dict['ppm'].setAsCurrent()

#sys.path.append("../../../../FX_ProjectManager")