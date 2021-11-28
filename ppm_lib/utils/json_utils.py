import json
import os
from datetime import datetime

json_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
json_path = os.path.join(json_path, "projects", "projects_info.json")

print ("PAAAATH")
print (json_path)

def read_from_json(json_path=json_path):
	"""
	Reads the information contained inside the projects_info.json
	"""
	info = ""
	if os.path.exists(json_path):
		if os.stat(json_path).st_size != 0:
		
			with open (json_path) as file:
				info = json.load(file)

	else:
		with open(json_path, "w") as file:
			file.write("[]")

	return info


def write_into_json_project(project_name, fps, resolution):
	"""
	Updates the information inside the projects_info.json
	"""
	info_list = []

	date = str(datetime.now())
	info = {
	"project_name" : project_name,
	"resolution" : resolution,
	"fps" : fps
	}

	
	if os.stat(json_path).st_size != 0:
		if os.path.exists(json_path):
			with open(json_path, "r") as file:
				
				info_list = json.load(file)
				info_list.append(info)	

	else:
		info_list.append(info)

	with open(json_path, "w") as file:
		json.dump(info_list, file, indent=4)



def write_into_json_sequence(project_path, sequence_name):
	seq_json_path = os.path.join(project_path, "sequences_info.json")
	seq_list = []

	sequence_info = {
		"sequence_name": sequence_name
	}

	if os.path.exists(seq_json_path):
		if os.stat(seq_json_path).st_size != 0:
			with open(seq_json_path, "r") as file:
				seq_list = json.load(file)
				seq_list.append(sequence_info)

	else:
		seq_list.append(sequence_info)

	with open(seq_json_path, "w") as file:
		json.dump(seq_list, file, indent=4)


		
def write_into_json_shot(sequence_name, shot_name):
	pass



def return_project_info(project_name):
	projects = read_from_json()
	for project in projects:
		if project["project_name"] == project_name:
			resolution = project["resolution"]
			fps = project["fps"]
			return resolution, fps



	






