import hou
import time

num_tasks = 100
files = []
for i in range(0,num_tasks):
    files.append("filename_" + str(i))
    
with hou.InterruptableOperation("Performing Tasks", long_operation_name = "Filenames", open_interrupt_dialog=True) as op:
    for fi, filename in enumerate(files):
      op.updateLongProgress(fi / float(len(files)-1), "Processing Files {}/{}".format(fi+1, len(files)) )
      with hou.InterruptableOperation(filename) as subop:
          for i in range(10):
            time.sleep(0.01)
            percent = float(i) / 9.0
            subop.updateProgress(percent) 