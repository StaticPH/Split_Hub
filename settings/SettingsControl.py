from PyQt5.QtCore import (Qt, QSettings, QObject, QByteArray)  # QObject not currently used
from PyQt5.QtWidgets import (
	QPushButton, QLineEdit, QDialog, QDialogButtonBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox
)

from Common import *
from QTabWidgetExtras import extendedTabWidget

import warnings, sys
warnings.warn("Interpreting SettingsControl")
enableTrivials = False

# Section####################################### Start Settings Handling ###############################################
# noinspection PyGlobalUndefined
class settingsManager(QDialog):
	# def __init__ (self, parent = None):
	def __init__(self):
		# noinspection PyArgumentList
		super(settingsManager, self).__init__()
		# self.setParent(parent)

		# This line being AFTER setParent should ensure that the settingsManager dialog doesnt get stuck inside the main window
		self.setWindowFlags(Qt.Dialog)
		# print("settingsMangager's parent is: " + str(parent.__class__.__name__))


		self.settingsFile = QSettings(
				"MySwitchboard.cfg",
				QSettings.IniFormat
		)

		self.settingsFile.setPath(
				QSettings.IniFormat,
				QSettings.UserScope,
				"MySwitchboard.cfg"
		)

		self.resize(500, 500)  # TEMPORARY

	# use @staticmethod???
	def getSettingsFile (self):
		return self.settingsFile

	def initSettings (self):
		# NOTE:Is toolbar moveable or locked in place. Is it floatable. Maybe if i figure out how to let the user adjust contents,
		# NOTE: add an option to disable that ability? Enable/disable certain widgets?
		# TODO: Figure out how to add descriptive text into the config file, if at all possible

		config = self.settingsFile  # test=config.setValue("test", 3);    print("test=" + str(config.value("test")))

		# Initialize all boolean type config settings to None
		cfgMainToolBarMoveable = None
		cfgMainToolBarFloatable = None
		cfgCreateSystemTrayIcon = None
		# TODO: Add print/logging statements when values need to be reset to default
		'''	Style Configs	'''
		config.beginGroup("Style_Options")
		cfgStyle = config.value("primaryStyle")
		if (cfgStyle is None) or (cfgStyle.capitalize().replace(" ", "") not in validStyles):
			if sys.platform.startswith("win32"):
				config.setValue("primaryStyle", "Windows Vista")
			else:
				config.setValue("primaryStyle", "Fusion")
			if enableTrivials: print("Resetting style to hard default")
		config.endGroup()

		'''	Main Toolbar Configs	'''
		config.beginGroup("MainToolbar")

		cfgMainToolBarPos = config.value("mainToolBarPosition",
										 Qt.LeftToolBarArea)  # Setting defaults like this while also including a case for invalid values may be redundant
		if cfgMainToolBarPos == "\n" or cfgMainToolBarPos not in ["1", "2", "4", "8"]:
			config.setValue("mainToolBarPosition", Qt.LeftToolBarArea)  # Default toolbar position is on the left side

		if correctBoolean(config.value("isMainToolBarMovable")) == -1:
			config.setValue("isMainToolBarMovable", True)  # Main toolbar is movable by default
		else:
			cfgMainToolBarMoveable = correctBoolean(config.value("isMainToolBarMovable", True, bool))
			config.setValue("isMainToolBarMovable", cfgMainToolBarMoveable)

		if correctBoolean(config.value("isMainToolBarFloatable")) == -1:
			config.setValue("isMainToolBarFloatable", True)  # Main toolbar is floatable by default
		else:
			cfgMainToolBarFloatable = correctBoolean(config.value("isMainToolBarFloatable", True, bool))
			config.setValue("isMainToolBarFloatable", cfgMainToolBarFloatable)

		config.endGroup()

		'''	Other Configs	'''
		# cfgTitle = config.value("cfgWindowTitle")
		# if (cfgTitle is None) or (cfgTitle == "\n"):
		# 	# This isn't really required, but it makes sure that the config has a value set in the config file even if the field was cleared.
		# 	config.setValue("cfgWindowTitle", "Switchboard")

		if correctBoolean(config.value("cfgShouldCreateTrayIcon")) == -1:
			config.setValue("cfgShouldCreateTrayIcon", True)
		else:
			cfgCreateSystemTrayIcon = correctBoolean(config.value("cfgShouldCreateTrayIcon", True, bool))
			config.setValue("cfgShouldCreateTrayIcon", cfgCreateSystemTrayIcon)

		# Makes sure that default window geometry value is available in case there isn't one in the config
		cfgWindowGeometry = config.value("mainWindowGeometry")
		if type(cfgWindowGeometry) is None or cfgWindowGeometry == "\n" or cfgWindowGeometry == "":
			config.setValue("mainWindowGeometry", defaultWindowGeometry)
			if enableTrivials: print("Defaulting geometry")

if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication, QAction

	app = QApplication(sys.argv)
	app.setApplicationName("SettingsControl")
	# print(str(app.effectiveWinId()))

	display = settingsManager()

	actQuit = QAction("&Quit", display)
	actQuit.setShortcut("Ctrl+q")
	# noinspection PyUnresolvedReferences
	actQuit.triggered.connect(sys.exit)
	display.addAction(actQuit)

	display.initSettings()
	display.show()
	# display.dumpObjectInfo()
	# display.dumpObjectTree()
	sys.exit(app.exec_())
