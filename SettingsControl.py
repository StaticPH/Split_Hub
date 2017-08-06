from PyQt5.QtWidgets import (
	QPushButton, QAction, QLabel, QCheckBox, QComboBox, QHBoxLayout,
	QVBoxLayout, QTabWidget, QWidget, QDialog, QDialogButtonBox,
	QStyleFactory, QGridLayout, QLineEdit, QActionGroup, QGroupBox
)

from PyQt5.QtCore import (Qt, QObject, QSettings)

import warnings
from Common import *
from QTabWidgetExtras import *

warnings.warn("Compiling SettingsControl")

# Section####################################### Start Settings Handling ###############################################
class settingsManager(QDialog):
	def __init__ (self):
		super(settingsManager, self).__init__()

		self.settingsFile = QSettings(
				"MySwitchboard.cfg",
				QSettings.IniFormat
		)

		self.settingsFile.setPath(
				QSettings.IniFormat,
				QSettings.UserScope,
				"MySwitchboard.cfg"
		)
		# self.windowFlags()
		# flags = Qt.WindowFlags()
		# flags = Qt.Dialog
		# self.setWindowFlags(flags)
		# self.show=self.appPreferences()
		self.resize(500, 500)  # TEMPORARY
		if __name__ == "__main__":  # TEMPORARY
			actQuit = QAction("&Quit", self)
			actQuit.setShortcut("Ctrl+q")
			actQuit.triggered.connect(sys.exit)
			self.addAction(actQuit)
		print("type of settingsManager is: " + str(type(self)))
		print("type of settingsManager.settingsFile is :" + str(type(self.settingsFile)))
		pass
		# print(self.settingsFile.allKeys())
		pass

	def getSettingsFile (self):
		return self.settingsFile

	def appPreferences (self):
		print("Preferences selected")

		settingsPage = self  # TODO: remove this, because its completely unnecessary, and just replace all settingsPage with self
		config = self.settingsFile

		self.setWindowTitle("Settings")

		# Create check boxes for group boxes
		def createCheckBox (self, text = "<placeholder>"):
			box = QCheckBox(text, self)
			box.stateChanged.connect(self.updatePreview)

			def Link ():
				wrapper(testPrint, "Flag Toggled").call()

			box.stateChanged.connect(Link)
			return box

		# Refresh field values		#TODO: FIND A BETTER WAY THAN THIS
		def getCurrentValues ():
			for setting in settingsList:
				# TODO: Handle different types, consider handling special cases
				if setting.isModified():
					print(setting.cfgName + " has been changed. Refreshing field value.")
					if type(setting) == QLineEdit:
						setting.setText(config.value(setting.cfgName))
					elif type(setting) == QCheckBox:
						if config.value(setting.cfgName) == True:
							pass
						elif config.value(setting.cfgName) == False:
							pass
					elif type(setting) == QPushButton:
						pass
					else:
						print("Setting \"" + setting.cfgName + "\" matches no handled type. Its type is " + str(type(setting)))

		# Update config file contents to match field values		#TODO: FIND A BETTER WAY THAN THIS
		def updateModifiedValues ():
			for setting in settingsList:
				# TODO:Handle different types, consider handling special cases
				if setting.isModified():
					print(setting.cfgName + " has been modified. Now saving.")

					if type(setting) == QLineEdit:
						config.setValue(setting.cfgName, setting.text())
					elif type(setting) == QCheckBox:
						# if setting.
						pass
					elif type(setting) == QPushButton:
						pass
					else:
						print("Setting \"" + setting.cfgName + "\" matches no handled type. Its type is " + str(type(setting)))

		# settingsPage.update()
		parentLayout = QVBoxLayout()

		#Create the 3 possible responses to the dialog
		responses = QDialogButtonBox(QDialogButtonBox.NoButton, Qt.Horizontal)
		responses.apply = responses.addButton("Accept Changes", QDialogButtonBox.AcceptRole)
		responses.good = responses.addButton("Okay", QDialogButtonBox.ActionRole)
		responses.discard = responses.addButton("Discard Changes", QDialogButtonBox.RejectRole)

		def accResp ():
			wrapper(testPrint, "Accepting Changes...").call()

			# Check for and save any changed settings
			updateModifiedValues()
			# print(winTitle.text()); #text, textChanged, textEdited, setValidator, setText. setTooltip. QLineEdit,displayText
			config.sync()

		def rejResp ():
			wrapper(testPrint, "Discarding Changes...").call()
			getCurrentValues()
			settingsPage.reject()

		def good ():
			# settingsPage.setResult(QDialog.accepted())
			# settingsPage.done(QDialog.accepted())
			settingsPage.accept()
			getCurrentValues()
			print("Leaving Settings")

		# responses.accepted.connect(good)
		# responses.accepted.connect(accResp)
		# responses.rejected.connect(rejResp)

		# Using this to allow an OK and an Accept button with separate resulting operations
		def onClicked ():
			sender = self.sender()

			if sender.text() == "Accept Changes":
				accResp()
			elif sender.text() == "Discard Changes":
				rejResp()
			elif sender.text() == "Okay":
				good()

		#When any of the three responses is clicked, goto onClicked
		responses.apply.clicked.connect(onClicked)
		responses.discard.clicked.connect(onClicked)
		responses.good.clicked.connect(onClicked)

		# Available(visible) Settings
		# DONE: probably need to use a byte array to store current settings on opening preferences window. that would be used to restore discarded changes
		# TODO: apply doesnt just need to sync, it needs to update too
		winTitle = QLineEdit(config.value("cfgWindowTitle"))
		winTitle.cfgName = "cfgWindowTitle"  # CRITICAL FOR AUTOMATIC SETTING SAVE
		labelWinTitle = QLabel("Window Title:")
		labelWinTitle.setBuddy(winTitle)

		settingsList = [winTitle]  # DONT FORGET TO ADD TO THIS

		# Settings Group Tabs
		settingGroupTabs = extendedTabWidget(settingsPage)  # Previously used QTabWidget directly
		self.generalTab = QWidget()
		self.tab2 = QWidget()  # placeholder
		self.tab3 = QWidget()  #placeholder

		# Create tab layouts
		def generalTabLayout ():
			horiz1 = QHBoxLayout()
			horiz1.addWidget(labelWinTitle)
			horiz1.addWidget(winTitle)
			return horiz1

		def tab2Layout ():  # placeholder
			pass

		def tab3Layout ():  # placeholder
			pass

		# Set layouts
		self.generalTab.setLayout(generalTabLayout())

		# Add tabs to group
		settingGroupTabs.addTabExtended(self.generalTab, "General", toolTip = "General Settings")
		settingGroupTabs.addTab(self.tab2, "Tab 2")  # placeholder
		settingGroupTabs.addTab(self.tab3, "Tab 3")  # placeholder

		parentLayout.addWidget(settingGroupTabs)  # Add the tab group to the top level layout first; everything not in a tab should be below this
		parentLayout.addWidget(responses)  # Add the 3 dialog responses to the top level layout last; nothing should appear below this
		settingsPage.setLayout(parentLayout)  #Set the top level layout
		settingsPage.show()

	# responses.receivers(PYQT_SIGNAL = accResp)
	# responses.clicked(responses.apply)
	# responses.isSignalConnected(responses.clicked(responses.apply))
	# if responses.clicked(QAbstractButton = apply):print("YES")
	# settingsPage.closeEvent()
	# QDialog.customEvent(),event,eventFilter, installEventFilter, leaveEvent,mask, showEvent, signalsBlocked
	# responses.finished.connect(something to save?)???     sender      senderSignalIndex       result? signals?
	##something that saves preferences when the OK button is pressed
	def updateFlags (self):
		config = self.settingsFile
		self.windowFlags()
		flags = Qt.WindowFlags()
		flags = Qt.Dialog  # Without this line, when MainWindow.window is set as parent, anything that would be displayed in its own dialog
		# by appPreferences is instead confined to the geometry of window

		# TODO: None of this part should apply to the settings window
		# TODO: Figure out how to get this to apply to the main window
		if (config.value("cfgKeepOnTop")) == True:
			flags |= Qt.WindowStaysOnTopHint
		if (config.value("cfgIsFrameless")) == True:
			flags |= Qt.FramelessWindowHint

		self.setWindowFlags(flags)

	def initSettings (self):
		# NOTE:Is toolbar moveable or locked in place. Is it floatable. Maybe if i figure out how to let the user adjust contents,
		# NOTE: add an option to disable that ability? Enable/disable certain widgets?
		# TODO: Figure out how to add descriptive text into the config file, if at all possible

		config = self.settingsFile  # test=config.setValue("test", 3);    print("test=" + str(config.value("test")))

		# Style Configs
		cfgStyle = config.value("primaryStyle")
		if str(config.value("primaryStyle")).capitalize().replace(" ", "") not in validStyles:
			config.setValue("primaryStyle", "Windows Vista")
			print("Resetting style to hard default")

		# Main Toolbar Configs
		config.beginGroup("MainToolbar")

		cfgMainToolBarPos = config.value("mainToolBarPosition")
		if cfgMainToolBarPos == "\n" or cfgMainToolBarPos not in ["1", "2", "4", "8"]:
			config.setValue("mainToolBarPosition", Qt.LeftToolBarArea)  # Default toolbar position is on the left side

		cfgMainToolBarMoveable = config.value("isMainToolBarMovable")
		if cfgMainToolBarMoveable not in extendedBools:
			config.setValue("isMainToolBarMovable", True)  # Main toolbar is movable by default
		elif cfgMainToolBarMoveable in [1, "t", "T", "true", "True"]:
			config.setValue("isMainToolBarMovable", True)
		elif cfgMainToolBarMoveable in [0, "f", "F", "false", "False"]:
			config.setValue("isMainToolBarMovable", False)

		cfgMainToolBarFloatable = config.value("isMainToolBarFloatable")
		if cfgMainToolBarFloatable not in extendedBools:
			config.setValue("isMainToolBarFloatable", True)  # Main toolbar is floatable by default
		elif cfgMainToolBarFloatable in [1, "t", "T", "true", "True"]:
			config.setValue("isMainToolBarFloatable", True)
		elif cfgMainToolBarFloatable in [0, "f", "F", "false", "False"]:
			config.setValue("isMainToolBarFloatable", False)

		config.endGroup()

		# TODO: Add checkboxes for these to config manager
		config.beginGroup("WindowFlags")

		cfgKeepOnTop = config.value("cfgKeepOnTop")
		if cfgKeepOnTop not in extendedBools:
			config.setValue("cfgKeepOnTop", False)
		elif cfgKeepOnTop in [0, "f", "F", "false", "False"]:
			config.setValue("cfgKeepOnTop", False)
		elif cfgKeepOnTop in [1, "t", "T", "true", "True"]:
			config.setValue("cfgKeepOnTop", True)

		cfgIsWindowFrameless = config.value("cfgIsFrameless")
		if cfgIsWindowFrameless not in extendedBools:
			config.setValue("cfgIsFrameless", False)
		elif cfgIsWindowFrameless in [0, "f", "F", "false", "False"]:
			config.setValue("cfgIsFrameless", False)
		elif cfgIsWindowFrameless in [1, "t", "T", "true", "True"]:
			config.setValue("cfgIsFrameless", True)

		self.updateFlags()

		config.endGroup()

		# Other Configs
		cfgTitle = config.value("cfgWindowTitle")
		if cfgTitle == "\n":
			config.setValue("cfgWindowTitle", "I am a window")

		# Makes sure that default window geometry value is available in case there isn't one in the config
		cfgWindowGeometry = config.value("mainWindowGeometry")
		if type(cfgWindowGeometry) is None or cfgWindowGeometry == "\n" or cfgWindowGeometry == "":
			config.setValue("mainWindowGeometry", defaultWindowGeometry)
			print("Defaulting geometry")

if __name__ == "__main__":
	import sys
	from PyQt5.QtWidgets import QApplication

	app = QApplication(sys.argv)
	app.setApplicationName("SettingsControl")
	# print(str(app.effectiveWinId()))

	display = settingsManager()

	display.initSettings()
	display.appPreferences()
	sys.exit(app.exec_())
