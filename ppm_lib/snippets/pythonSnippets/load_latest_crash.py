# Script written by Lewis Taylor

import os, sys
from datetime import datetime
tmp_dir = os.getenv('TEMP')
fils = [os.path.join(tmp_dir, y) for y in os.listdir(tmp_dir) if y.endswith('.hip')]

fils.sort(key = lambda item: os.path.getctime(item), reverse = True)

crash_file = fils[0].split('/')[-1]

dt = datetime.fromtimestamp(os.path.getctime(fils[0]))
date = dt.strftime('%a %d/%m/%y %H:%M:%S')
dispMessage = 'open scene\n{SCENE}\ncreated on {DATE}?'.format(SCENE = crash_file,
                                                                DATE = date)
if hou.ui.displayConfirmation(dispMessage):
    hou.hipFile.load(fils[0])
