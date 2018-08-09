from PyQt5.QtWidgets import (
	QLabel, QCheckBox, QHBoxLayout, QVBoxLayout, QGridLayout,
	QWidget, QGroupBox
	# ,QStyleFactory, QActionGroup, QComboBox
)
from PyQt5.QtCore import (Qt, QSettings, QObject)  # QObject not currently used

import sys
from Common import *
from Common import correctBoolean

# from settings.SettingsControl import settingEntry, settingsList

enableTrivials = True

class flagTab(QWidget):
	def __init__(self, settings, parent = None):  # Parent will always be SettingsControl.settingsManager UNLESS this file is run standalone
		super(flagTab, self).__init__()
		self.setParent(parent)
		self.settingsFile = settings
		print("flagTab's parent is: " + str(parent.__class__.__name__))

		'''	Create checkboxes for window flag controls	'''
		self.windowStaysOnTopCheckBox = self.flagCheckBox("WindowFlags/cfgKeepOnTop", "Keep the window on top?")
		self.framelessWindowCheckBox = self.flagCheckBox("WindowFlags/cfgIsFrameless", "Frameless window mode")
		self.windowTitleCheckBox = self.flagCheckBox("WindowFlags/cfgShowTitle", "Show title bar?")

		''' Create settingEntry for each checkbox'''
		flag1 = settingEntry(self.windowStaysOnTopCheckBox, "WindowFlags/cfgKeepOnTop")
		flag2 = settingEntry(self.framelessWindowCheckBox, "WindowFlags/cfgIsFrameless")
		flag3 = settingEntry(self.windowTitleCheckBox, "WindowFlags/cfgShowTitle")

		self.generalFlagBox = self.makeWindowFlagBox()

	def updateFlags(self, parent = None):
		config = self.settingsFile
		self.windowFlags()
		flags = Qt.WindowFlags()
		flags = Qt.Dialog  # Without this line, when MainWindow.window is set as parent, anything that would be displayed in its own dialog
		# by appPreferences is instead confined to the geometry of window

		# TODO: None of this part should apply to the settings window
		# TODO: Figure out how to get this to apply to the main window

		# probably going to need to pass this function the parent window or something
		if ((config.value("WindowFlags/cfgKeepOnTop", type = bool)) == True) or (self.windowStaysOnTopCheckBox.isChecked()):
			flags |= Qt.WindowStaysOnTopHint
		if ((config.value("WindowFlags/cfgIsFrameless", type = bool)) == True) or (self.framelessWindowCheckBox.isChecked()):
			flags |= Qt.FramelessWindowHint
		if ((config.value("WindowFlags/cfgShowTitle", type = bool)) == True) or (self.windowTitleCheckBox.isChecked()):
			flags |= Qt.WindowTitleHint
		if ((config.value("WindowFlags/cfgDropShadow", type = bool)) == True):  # or (self.windowNoDropShadowCheckBox.isChecked()):
			flags |= Qt.NoDropShadowWindowHint
		if ((config.value("WindowFlags/cfgSysMenu", type = bool)) == True):  # or (self.windowSystemMenuCheckBox.isChecked()):
			flags |= Qt.WindowSystemMenuHint
		if ((config.value("WindowFlags/cfgShadeButton", type = bool)) == True):  # or (self.windowShadeButtonCheckBox.isChecked()):
			flags |= Qt.WindowShadeButtonHint
		# if ((config.value("WindowFlags/cfgKeepOnBottom")) == True):# or (self.windowStaysOnBottomCheckBox.isChecked()):
		# 	flags |= Qt.WindowStaysOnBottomHint
		if ((config.value("WindowFlags/cfgCustomizeWindow", type = bool)) == True):  # or (self.customizeWindowHintCheckBox.isChecked()):
			flags |= Qt.CustomizeWindowHint
		if parent is not None:
			parent.setWindowFlags(flags)
		else:
			self.setWindowFlags(flags)

	def retrieveFlags(self):  # WIP
		config = self.settingsFile
		flags = Qt.WindowFlags()
		flags = Qt.Window
		if ((config.value("WindowFlags/cfgKeepOnTop", type = bool)) == True) or (self.windowStaysOnTopCheckBox.isChecked()):
			flags |= Qt.WindowStaysOnTopHint
		if ((config.value("WindowFlags/cfgIsFrameless", type = bool)) == True) or (self.framelessWindowCheckBox.isChecked()):
			flags |= Qt.FramelessWindowHint
		if ((config.value("WindowFlags/cfgShowTitle", type = bool)) == True) or (self.windowTitleCheckBox.isChecked()):
			flags |= Qt.WindowTitleHint
		if ((config.value("WindowFlags/cfgDropShadow", type = bool)) == True):  # or (self.windowNoDropShadowCheckBox.isChecked()):
			flags |= Qt.NoDropShadowWindowHint
		if ((config.value("WindowFlags/cfgSysMenu", type = bool)) == True):  # or (self.windowSystemMenuCheckBox.isChecked()):
			flags |= Qt.WindowSystemMenuHint
		if ((config.value("WindowFlags/cfgShadeButton", type = bool)) == True):  # or (self.windowShadeButtonCheckBox.isChecked()):
			flags |= Qt.WindowShadeButtonHint
		# if ((config.value("WindowFlags/cfgKeepOnBottom", type = bool)) == True):# or (self.windowStaysOnBottomCheckBox.isChecked()):
		# 	flags |= Qt.WindowStaysOnBottomHint
		if ((config.value("WindowFlags/cfgCustomizeWindow", type = bool)) == True):  # or (self.customizeWindowHintCheckBox.isChecked()):
			flags |= Qt.CustomizeWindowHint
		return flags

	'''	Create check boxes for group boxes	'''

	# Suppress warnings about unresolved references to connect() using noinspection PyUnresolvedReferences
	# noinspection PyShadowingNames, PyUnresolvedReferences
	def flagCheckBox(self, cfgName, text = "<placeholder>"):
		# Would have prevented a weak warning if it worked, but parameters and nonlocal variables can't have the same name. Using noinspection instead...
		# nonlocal self
		box = QCheckBox(text)
		initialState = correctBoolean(self.settingsFile.value(cfgName))
		box.setChecked(initialState)

		def Link():
			print("Flag \"" + cfgName + "\" toggled")
			previous = correctBoolean(self.settingsFile.value(cfgName))

		# self.settingsFile.setValue(cfgName, negate(previous))
		# print("was:"+str(previous))
		# print("is: " +self.settingsFile.value(cfgName))

		# print(box.__class__.__name__)

		box.stateChanged.connect(Link)
		return box

	def makeWindowFlagBox(self):  # consider having all the flag-checkboxes automatically added to a list
		windowFlagBox = QGroupBox("Window Flags",
								  self)  # Need to remember to pass self so that windowFlagBox becomes a descendant of settingsManager

		# sync checked states
		# self.syncWindowFlagCheckStates()  #FIXME
		# Add checkbox widgets to layout
		flagBoxLayout = QGridLayout()
		flagBoxLayout.addWidget(self.windowStaysOnTopCheckBox)
		flagBoxLayout.addWidget(self.framelessWindowCheckBox)
		flagBoxLayout.addWidget(self.windowTitleCheckBox)
		windowFlagBox.setLayout(flagBoxLayout)
		return windowFlagBox

# '''	Refresh field values ONLY for checkboxes associated with a window flag	'''
# def syncWindowFlagCheckStates (self):
# 	config = self.settingsFile
# 	for settingEntry in settingsList:
# 		setting = settingEntry.widget
# 		settingName = settingEntry.cfgName
# 		if settingName.startswith("WindowFlags/"):
# 			print("fixing check states")
# 			setting.setChecked(correctBoolean(config.value(settingName)))
# def acceptFlagChanges(self):
# 	config = self.settingsFile
# 	for settingEntry in settingsList:
# 		setting = settingEntry.widget
# 		settingName = settingEntry.cfgName
# 		if settingName.startswith("WindowFlags/"):
# 			if setting.checkState() != correctBoolean(config.value(settingName)):
# 				config.setValue(setting.checkState())

if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication, QAction
	from PyQt5.QtCore import QSettings

	app = QApplication(sys.argv)
	app.setApplicationName("flagTab")
	# print(str(app.effectiveWinId()))
	settingsFile = QSettings(
			"MySwitchboard.cfg",
			QSettings.IniFormat
	)

	settingsFile.setPath(
			QSettings.IniFormat,
			QSettings.UserScope,
			"MySwitchboard.cfg"
	)

	display = flagTab(settingsFile)

	actQuit = QAction("&Quit", display)
	actQuit.setShortcut("Ctrl+q")
	# noinspection PyUnresolvedReferences
	actQuit.triggered.connect(sys.exit)
	display.addAction(actQuit)

	display.show()
	# display.dumpObjectInfo()
	# display.dumpObjectTree()
	sys.exit(app.exec_())
