import os
import sys
import json
import subprocess as sb


def houdini_set_and_run(project_path = "", FPS=24):
	"""
	Set the environment variables for the current session and opens Houdini
	"""
	with open('config.json') as config_file:
		data = json.load(config_file)

	full_version = data.get('houdini_full_version', None)
	if full_version != None:
		short_version = '.'.join([full_version.split(".")[0], full_version.split(".")[1]])
	else:
		print ("No houdini version specified on config file")

	apps_folder = os.path.dirname( os.path.dirname(os.path.abspath(__file__)) )
	hou_folder = os.path.join(apps_folder, "houdini")

	env = os.environ

	hfs = r'C:\Program Files\Side Effects Software\Houdini {}'.format(full_version)
	env['HH'] = os.pathsep.join([os.path.expanduser(r'~\Documents\houdini{}'.format(short_version)), os.path.join(hfs, "houdini")])
	env['HOUDINI_PATH'] = ';'.join([hou_folder, env['HH'], os.getenv('HOUDINI_PATH', '')])

	env["JOB"] = project_path
	env["HIP"] = project_path
	env["FPS"] = str(FPS)

	cmd = (r'{}\bin\houdini.exe'.format(hfs)).replace('\\', '/')

	sb.Popen(cmd)




