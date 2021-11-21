from PySide2 import QtWidgets, QtCore, QtGui


def Palette(palette):
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(60,60,60))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(208,208,208))
    palette.setColor(QtGui.QPalette.Base , QtGui.QColor(25,25,25))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(208,208,208))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(208,208,208))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(208,208,208))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(45,45,45))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(208,208,208))
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42,130,218))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42,130,218))
    palette.setColor(QtGui.QPalette.Highlight, QtCore.Qt.black)

