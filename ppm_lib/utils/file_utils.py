import os
import glob
from logging_utils import logger as lg




def get_files_of_type(dir, fileType):
	"""
	Return files of the given filetype in a location (dir)
	"""
	fils = []
	for x in os.walk(dir):		
		for y in glob.glob(os.path.join(x[0], "*.{}".format(fileType))):
			fils.append(os.path.normpath(y))

	if fils:
		return fils
	else:
		return "No files of type: {}".format(fileType)



def rename_files(dir_name, mode, old_text="", new_text=""):
	"""
	Rename files using a prefix or a postfix, or fully replace a part of the original Lctext
	"""
	for fil in os.listdir(dir_name):
		fil = os.path.join(dir_name, fil)
		file_name = os.path.basename(fil)

		if mode == "prefix":
			new_name = os.path.join(dir_name, file_name.replace(file_name, new_text + file_name))
		if mode == "replace":
			new_name = os.path.join(dir_name, file_name.replace(old_text, new_text))
		if mode == "append":
			new_name = os.path.join(dir_name, file_name.replace(file_name, file_name + new_text))

		os.rename(fil, new_name)



def _frame_range_from_file_seq(dir_name):
	"""
	Returns a tuple with the first and last frame of an image sequence inside the dir_name folder
	"""
	frames = []

	for fil in os.listdir(dir_name):
		fil = os.path.join(dir_name, fil)
		folder = os.path.dirname(fil)
		file_full_name = os.path.basename(fil)
		file_name = file_full_name.split(".")[0]
		file_frame = file_full_name.split(".")[1]
		file_ext = file_full_name.split(".")[-1]

		frames.append(int(file_frame.lstrip("0")))
	
	return (min(frames), max(frames))



def renumber_files(dir_name, new_start_frame=1001, leading_zeroes=4):
	"""
	Renames the files so they start from the new_start_frame
	"""
	if not isinstance(new_start_frame, int):
		new_start_frame = int(new_start_frame)

	frame_range = _frame_range_from_file_seq(dir_name)
	ran = int(frame_range[1]) - int(frame_range[0])
	print(ran)
	
	initial_frame = frame_range[0]
	new_initial_frame = int(new_start_frame) 

	for i in range(ran + 1):
		start_frame_old = str(i + frame_range[0]).zfill(leading_zeroes) 
		start_frame_new = str(new_initial_frame + i).zfill(leading_zeroes)
		

		rename_files(dir_name, "replace", start_frame_old, start_frame_new)









		

	









