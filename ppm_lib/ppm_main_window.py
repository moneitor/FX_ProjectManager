import sys
from PySide2 import QtUiTools, QtWidgets
import utils.OsUtils
import os
import houdini_start
import utils.json_utils
import utils.folder_utils as folder_utils


projects_dir =  os.path.normpath( os.path.join( os.path.dirname(os.path.dirname(__file__)) , "projects") )


class Main_PPM(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(Main_PPM, self).__init__(parent)

		file_path = os.path.abspath(os.path.dirname(__file__))
		file_path = os.path.join(file_path, "ui", "ppm_main.ui")
		self.ui = QtUiTools.QUiLoader().load(file_path, parentWidget=self)

		self.project_path = projects_dir
		self.project_name = ""
		self.full_project_path = ""
		self.full_path_to_sequence = ""
		self.sequence_name = ""


		self.update_list(self.ui.list_projects)
		self.connections()

	def connections(self):
		self.ui.btn_new_project.clicked.connect(self.add_new_project)	
		self.ui.btn_houdini.clicked.connect(self.open_houdini)

		self.ui.list_projects.itemClicked.connect(self.get_project_name)
		self.ui.list_projects.itemClicked.connect(self.update_list_sequences)

		self.ui.btn_new_seq.clicked.connect(self.add_new_seq)

		self.ui.list_sequence.itemClicked.connect(self.get_sequence_name)


	def add_new_project(self):
		"""
		Adds new project to the list widget and also to the projects_info
		json file
		"""	

		new_project = NewProject()
		result = new_project.exec_()

		if result == QtWidgets.QDialog.Accepted:
			project_name = new_project.project_path
			project_resolution = new_project.resolution
			project_fps = new_project.fps
			if (len(project_name) > 0):
				json_utils.write_into_json_project(project_name=project_name, fps=project_fps, resolution=project_resolution)
				self.update_list(self.ui.list_projects)	


	def add_new_seq(self):
		"""
		Adds a new Sequence folder inside the selected project
		"""
		if self.full_project_path:
			print(self.full_project_path)
			new_seq = NewSeq()
			result = new_seq.exec_()

			if result == QtWidgets.QDialog.Accepted:				
				sequence_name = new_seq.sequence_name
				self.full_path_to_sequence = os.path.join(self.full_project_path, sequence_name)

				if not os.path.exists(self.full_path_to_sequence):	
					folder_utils.create_sequence_folder(sequence_name, self.full_project_path)				
					json_utils.write_into_json_sequence(self.full_project_path, sequence_name)
					self.update_list_sequences()
				else:
					print("Sequence name already exists")
				

		else:
			print("Please select a project")



	def add_new_shot(self):
		"""
		Adds a new Shot folder inside the selected sequence
		"""
		pass



	def get_project_name(self, click):
		"""
		Get the string on the selected item on the list and save it on the class attribute self.project_name
		"""
		self.project_name = click.text()
		self.full_project_path = os.path.join(self.project_path, self.project_name)
		self.ui.lb_project_path.setText(self.full_project_path)
		


	def update_list(self, list_widget):
		"""
		Cleans and update the project list
		"""
		list_widget.clear()
		list_projects = json_utils.read_from_json()
		for project in list_projects:			
			list_widget.addItem(project['project_name'])


	def update_list_sequences(self):
		"""
		Cleans and update the project list
		"""		
		self.ui.list_sequence.clear()
		sequences = json_utils.read_from_json(os.path.join(self.full_project_path, "sequences_info.json"))
		
		for seq in sequences:
			print (seq)
			self.ui.list_sequence.addItem(seq['sequence_name'])


	def get_sequence_name(self, click):
		"""
		Updates the self.full_path_to_sequence class attribute and also the lable lb_project_path
		"""
		self.sequence_name = click.text()
		self.full_path_to_sequence = os.path.join(self.full_project_path, self.sequence_name)
		self.ui.lb_project_path.setText(self.full_path_to_sequence)



	def update_list_shots(self):
		pass



	def open_houdini(self):
		if self.full_path_to_sequence:
			if len(self.project_name) > 0:		
				if os.path.exists(self.full_project_path):				
					resolution, fps = json_utils.return_project_info(self.project_name)				
					houdini_start.houdini_set_and_run(self.full_path_to_sequence, fps)
					
			else:
				print ("Project Folder don't exist")



class NewProject(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setWindowTitle("Create New Project")

		self._fps = ('24', '25', '30', '60')
		self._res = ("1280 x 720", "960 x 540", "1600 x 900", "1920 x 1080", "2048 x 1152", "3048 x 2160")
		self.project_path = ""
		self.fps = ""
		self.resolution = ""
		self.widgets()
		self.layout()
		self.connections()


	def widgets(self):
		self.title = QtWidgets.QLabel("New Project")
		self.ln_project_name = QtWidgets.QLineEdit()
		self.cb_fps = QtWidgets.QComboBox()
		self.cb_fps.addItems(self._fps)
		self.cb_resolutions = QtWidgets.QComboBox()
		self.cb_resolutions.addItems(self._res)
		self.btn_ok = QtWidgets.QPushButton("OK")		
		self.btn_cancel = QtWidgets.QPushButton("Cancel")



	def layout(self):
		form_layout = QtWidgets.QFormLayout()
		form_layout.addRow("Project Name: ", self.ln_project_name)
		form_layout.addRow("FPS: ", self.cb_fps)
		form_layout.addRow("Resolutions: ", self.cb_resolutions)
		
		button_layout = QtWidgets.QHBoxLayout()
		button_layout.addWidget(self.btn_cancel)
		button_layout.addWidget(self.btn_ok)

		main_layout = QtWidgets.QVBoxLayout(self)
		main_layout.addLayout(form_layout)
		main_layout.addLayout(button_layout)
		#main_layout.addWidget(self.btn_ok)


	def connections(self):
		self.ln_project_name.textChanged.connect(self.set_project_name)

		self.btn_ok.clicked.connect(self.create)		
		self.btn_ok.clicked.connect(self.accept)
		self.btn_cancel.clicked.connect(self.reject)



	def create_folders(self):
		project_path = os.path.join(projects_dir, self.project_path)
		if os.path.exists(project_path):
			print("Please select a different name, folder named '{}'' already exists".format(self.project_path))
			return


		os.makedirs(project_path)
		folder_utils.create_folders_project(project_path)	



	def create(self):		
		if len(self.project_path) > 1:			
			self.fps = self.cb_fps.currentText()
			self.resolution = self.cb_resolutions.currentText()		
			self.create_folders()	
		else:
			self.warning_message()
			return self.reject


	def set_project_name(self):
		self.project_path = self.ln_project_name.text()


	def warning_message(self):
		msg = QtWidgets.QMessageBox()
		msg.setText("Please fill the name of the Project.")
		msg.exec_()
		return msg	




class NewSeq(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setWindowTitle("Create New Sequence")

		self.sequence_name = ""

		self.widgets()
		self.layout()
		self.connections()


	def widgets(self):	
		self.ln_sequence_name = QtWidgets.QLineEdit()

		self.btn_ok = QtWidgets.QPushButton("OK")		
		self.btn_cancel = QtWidgets.QPushButton("Cancel")


	def layout(self):
		form_layout = QtWidgets.QFormLayout()
		form_layout.addRow("Sequence Name: ", self.ln_sequence_name)
		
		button_layout = QtWidgets.QHBoxLayout()
		button_layout.addWidget(self.btn_cancel)
		button_layout.addWidget(self.btn_ok)

		main_layout = QtWidgets.QVBoxLayout(self)

		main_layout.addLayout(form_layout)
		main_layout.addLayout(button_layout)


	def connections(self):
		self.ln_sequence_name.textChanged.connect(self.set_sequence_name)

		self.btn_ok.clicked.connect(self.create)		
		self.btn_ok.clicked.connect(self.accept)
		self.btn_cancel.clicked.connect(self.reject)


	def create_folders(self):
		project_path = os.path.join(projects_dir, self.project_path)
		if os.path.exists(project_path):
			print("Please select a different name, folder named '{}'' already exists".format(self.project_path))
			return


		os.makedirs(project_path)
		folder_utils.create_folders_project(project_path)


	def set_sequence_name(self):
		self.sequence_name = self.ln_sequence_name.text()


	def warning_message(self):
		msg = QtWidgets.QMessageBox()
		msg.setText("Please fill the name of the Project.")
		msg.exec_()
		return msg	




class NewShot(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setWindowTitle("Create New Shot")





def main():

	try:
		app.close()
		app.deleteLater()
	except:
		pass

	app = QtWidgets.QApplication(sys.argv)
	win = Main_PPM()	
	win.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
	

	#houdini_start.houdini_set_and_run(temp_project_path, temp_fps)
