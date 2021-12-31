import sys
from PySide2 import QtUiTools, QtWidgets
import files.file_utils as file_utils
import os


class Rename_files(QtWidgets.QWidget):
	def __init__(self):
		super(Rename_files, self).__init__()

		ui_file = "./ui/renamer.ui"
		self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)

		self.folder = ""
		self.old_text = ""
		self.new_text = ""
		self.new_start = 1001

		self.connections()

	def connections(self):
		self.ui.btn_folder.clicked.connect(self.lookup_dir)
		self.ui.ln_dir.textEdited.connect(self.update_folder_text)
		self.ui.ln_oldtext.textEdited.connect(self.update_old_text)
		self.ui.ln_newtext.textEdited.connect(self.update_new_text)
		self.ui.spn_newstart.valueChanged.connect(self.update_new_start_frame)
		self.ui.btn_rename.clicked.connect(self.rename)
		self.ui.btn_renumber.clicked.connect(self.renumber)

	def lookup_dir(self):
		asset_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
		self.ui.ln_dir.setText(asset_dir)
		self.folder = asset_dir

	def update_folder_text(self):
		self.folder = self.ui.ln_dir.text()

	def update_old_text(self):
		self.old_text = self.ui.ln_oldtext.text()

	def update_new_text(self):
		self.new_text = self.ui.ln_newtext.text()

	def update_new_start_frame(self):
		self.new_start = int(self.ui.spn_newstart.text())

	def rename(self):
		if self.ui.rd_prefix.isChecked():
			mode = "prefix"
		if self.ui.rd_append.isChecked():
			mode = "append"
		if self.ui.rd_replace.isChecked():
			mode = "replace"

		if os.path.isdir(self.folder) and len(self.new_text) > 0:
			print (self.old_text, self.new_text)			
			file_utils.rename_files(self.folder, mode, self.old_text, self.new_text)

	def renumber(self):
		if os.path.isdir(self.folder):
			file_utils.renumber_files(self.folder, self.new_start, 4)

		

def main():
	app = QtWidgets.QApplication(sys.argv)
	win = Rename_files()
	win.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()