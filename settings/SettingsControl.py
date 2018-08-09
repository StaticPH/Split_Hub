from PyQt5.QtCore import (Qt, QSettings, QObject, QByteArray)  # QObject not currently used
from PyQt5.QtWidgets import (
	QPushButton, QLineEdit, QDialog, QDialogButtonBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox
	# QTabWidget, QStyleFactory, QActionGroup, QComboBox
)

from Common import *
from QTabWidgetExtras import extendedTabWidget
from StyleHandler import styleSheets
from settings.FlagTab import flagTab

import warnings, sys
warnings.warn("Compiling SettingsControl")
enableTrivials = False

# Section####################################### Start Settings Handling ###############################################
# noinspection PyGlobalUndefined
class settingsManager(QDialog):
	def __init__ (self, parent = None):
		# noinspection PyArgumentList
		super(settingsManager, self).__init__()
		self.setParent(parent)
		self.setWindowFlags(
			Qt.Dialog)  # This line being AFTER setParent should ensure that the settingsManager dialog doesnt get stuck inside the main window
		print("settingsMangager's parent is: " + str(parent.__class__.__name__))


		self.settingsFile = QSettings(
				"MySwitchboard.cfg",
				QSettings.IniFormat
		)

		self.settingsFile.setPath(
				QSettings.IniFormat,
				QSettings.UserScope,
				"MySwitchboard.cfg"
		)
		self.flagTab = flagTab(self.settingsFile, self)
		# self.windowFlags()
		# flags = Qt.WindowFlags()
		# flags = Qt.Dialog
		# self.setWindowFlags(flags)
		# self.show=self.appPreferences()

		self.resize(500, 500)  # TEMPORARY
		# else:
		# 	print("settingsManager Name = " + __name__)
		# 	print("parent of settingsManager is: " + str(self.parent().__class__.__name__))
		# 	print("parentWidget of settingsManager is: " + str(self.parentWidget().__class__.__name__))
		# 	print("type of settingsManager is: " + str(type(self)))
		# 	print("type of settingsManager.settingsFile is :" + str(type(self.settingsFile)))
		pass
		# print(self.settingsFile.allKeys())
		pass

	# use @staticmethod???
	def getSettingsFile (self):
		return self.settingsFile

	'''	Refresh field values	'''  # TODO: TRY TO FIND A BETTER WAY THAN THIS, consider making this into an override of showEvent()
	# noinspection PyShadowingNames
	def getCurrentValues(self):  #TODO:Can probably reduce this to ignoring any changes and just pulling the values directly from the config
		config = self.settingsFile
		for settingEntry in settingsList:
			setting = settingEntry.widget
			settingName = settingEntry.cfgName
			# TODO: Handle different types, consider handling special cases
			if (type(setting) == QLineEdit):  # and (setting.isModified()):
				# print(settingName + " has been changed, but not saved. Refreshing field value.")
				setting.setText(config.value(settingName))
			# elif (type(setting) == QLineEdit):
			# 	continue  # Temp
			# elif (type(setting) == QCheckBox):	#Temp
			# 	print("State: " + str(setting.checkState()))	#Temp
			# 	print("Setting: " + str(config.value(settingName)))	#Temp
			# 	# print("Corrected setting: " + str(correctBoolean(config.value(settingName))))	#Temp
			elif (type(setting) == QCheckBox):  # and (setting.checkState() != correctBoolean(config.value(settingName))):
				# print(settingName + " has been changed, but not saved. Refreshing field value.")
				if correctBoolean(config.value(settingName)) == True:
					setting.setChecked(True)
				elif correctBoolean(config.value(settingName)) == False:
					setting.setChecked(False)
			# elif (type(setting) == QCheckBox):
			# 	continue  # Temp
			elif type(setting) == QPushButton:
				pass
			else:
				print(settingName + " has been changed, but not saved. Refreshing field value.")
				print("Setting \"" + settingName + "\" matches no handled type. Its type is " + str(type(setting)))


	'''	Update config file contents to match field values	'''  # TODO: TRY TO FIND A BETTER WAY THAN THIS
	# noinspection PyShadowingNames
	def updateModifiedValues (self):
		config = self.settingsFile
		for settingEntry in settingsList:
			setting = settingEntry.widget
			settingName = settingEntry.cfgName
			# TODO:Handle different types, consider handling special cases
			if (type(setting) == QLineEdit):
				if (setting.isModified()):
					print(settingName + " has been modified. Now saving.")
					config.setValue(settingName, setting.text())
				continue
			elif (type(setting) == QCheckBox):
				if (correctBoolean(config.value(settingName)) != correctBoolean(setting.checkState())):
					print(settingName + " has been modified. Now saving.")
					config.setValue(settingName, setting.checkState())
				continue
			elif type(setting) == QPushButton:
				pass
			else:
				print(settingName + " has been modified. Now saving.")
				print("Setting \"" + settingName + "\" matches no handled type. Its type is " + str(type(setting)))

	# noinspection PyAttributeOutsideInit, PyArgumentList
	def appPreferences (self):
		if enableTrivials: print("Preferences selected")

		config = self.settingsFile
		# global settingEntry
		flagTab = self.flagTab
		self.setWindowTitle("Settings")

		# NOTICE: createCheckBox USED TO BE HERE
		# NOTICE: getCurrentValues USED TO BE HERE
		# NOTICE: updateModifiedValues USED TO BE HERE
		# self.update()
		parentLayout = QVBoxLayout()

		# Create the 2 possible responses to the dialog
		responses = QDialogButtonBox(QDialogButtonBox.NoButton, Qt.Horizontal)
		responses.apply = responses.addButton("Accept Changes", QDialogButtonBox.AcceptRole)
		responses.discard = responses.addButton("Discard Changes", QDialogButtonBox.RejectRole)

		def accResp ():
			print("Accepting Changes...")
			# Check for and save any changed settings
			self.updateModifiedValues()
			self.accept()  # TEMPORARY? See reminder above
			# print(winTitle.text()); #text, textChanged, textEdited, setValidator, setText. setTooltip. QLineEdit,displayText
			config.sync()
			print("Leaving Settings")  # TEMPORARY? See reminder above

		def rejResp():  # Might need to have the settings gui get deleted and recreated here
			print("Discarding Changes...")
			self.getCurrentValues()
			self.reject()

		# Using this to allow an OK and an Accept button with separate resulting operations
		#TODO: get rid of this, since the OK button has been eliminated
		def onClicked ():
			sender = self.sender()

			if sender.text() == "Accept Changes":
				accResp()
			elif sender.text() == "Discard Changes":
				rejResp()

		# When either of the two responses is clicked, go to onClicked
		responses.apply.clicked.connect(onClicked)
		responses.discard.clicked.connect(onClicked)

		# Available(visible) Settings
		# DONE: probably need to use a byte array to store current settings on opening preferences window. that would be used to restore discarded changes
		# TODO: apply doesnt just need to sync, it needs to update too
		# NOTE: replaced the two lines below with a call to a class that contains the two, settingEntry
		# winTitle = QLineEdit(config.value("cfgWindowTitle"))
		# winTitle.cfgName = "cfgWindowTitle"  # CRITICAL FOR AUTOMATIC SETTING SAVE
		winTitle = settingEntry(QLineEdit(config.value("cfgWindowTitle")), "cfgWindowTitle")
		labelWinTitle = QLabel("Window Title:")
		labelWinTitle.setBuddy(winTitle.widget)

		# windowFlagBox.setLayout(self.makeWindowFlagBox())
		windowFlagBox = flagTab.generalFlagBox
		# self.windowFlagBox.setLayout(self.flagBoxLayout)
		# print(self.windowFlagBox.children())
		# if enableTrivials:
		# 	print("windowFlagBox parent: " + str(windowFlagBox.parent().__class__.__name__))
		# 	print("windowFlagBox parentWidget: " + str(windowFlagBox.parentWidget().__class__.__name__))
		# 	print("Am I the ancestor of the windowFlagBox? " + str(self.isAncestorOf(windowFlagBox)))

		# NOTE: the following line occurs automatically as part of new settingEntry class
		# settingsList.append(winTitle)  # DONT FORGET TO ADD TO THIS

		'''	Settings Group Tabs	'''
		settingGroupTabs = extendedTabWidget(self)  # Previously used QTabWidget directly
		self.generalTab = QWidget()
		# self.flagTab = QWidget()  # placeholder
		self.tab3 = QWidget()  # placeholder

		'''	Create tab layouts	'''

		# noinspection PyArgumentList
		def generalTabLayout ():
			layout = QHBoxLayout()
			layout.addWidget(labelWinTitle)
			layout.addWidget(winTitle.widget)
			return layout

		# noinspection PyArgumentList
		def flagTabLayout ():
			layout = QHBoxLayout()
			layout.addWidget(windowFlagBox)
			return layout

		def tab3Layout ():  # placeholder
			pass

		'''	Set layouts	'''
		self.generalTab.setLayout(generalTabLayout())
		self.flagTab.setLayout(flagTabLayout())  # TODO
		# self.tab3.setLayout(tab3Layout())		#TODO

		'''	Add tabs to group	'''
		settingGroupTabs.addTabExtended(self.generalTab, "General", toolTip = "General Settings")
		settingGroupTabs.addTabExtended(self.flagTab, "Window Flags", toolTip = "Manage the window flags")  # placeholder
		# self.windowFlagBox.show()
		# settingGroupTabs.addTab(self.tab3, "Tab 3")  # placeholder

		parentLayout.addWidget(settingGroupTabs)  # Add the tab group to the top level layout first; everything not in a tab should be below this
		parentLayout.addWidget(responses)  # Add the 3 dialog responses to the top level layout last; nothing should appear below this
		self.setLayout(parentLayout)  # Set the top level layout
		self.hide()
		# self.show()			<----THIS GUY HAS BEEN THE SOURCE OF ALL MY TROUBLES WITH THINGS DISAPPEARING
		print("~~~~~~~~~")

	# responses.receivers(PYQT_SIGNAL = accResp)
	# responses.clicked(responses.apply)
	# responses.isSignalConnected(responses.clicked(responses.apply))
	# if responses.clicked(QAbstractButton = apply):print("YES")
	# settingsPage.closeEvent()
	# QDialog.customEvent(),event,eventFilter, installEventFilter, leaveEvent,mask, showEvent, signalsBlocked
	# responses.finished.connect(something to save?)???     sender      senderSignalIndex       result? signals?
	##something that saves preferences when the OK button is pressed

	def initSettings (self):
		# NOTE:Is toolbar moveable or locked in place. Is it floatable. Maybe if i figure out how to let the user adjust contents,
		# NOTE: add an option to disable that ability? Enable/disable certain widgets?
		# TODO: Figure out how to add descriptive text into the config file, if at all possible

		config = self.settingsFile  # test=config.setValue("test", 3);    print("test=" + str(config.value("test")))
		flagTab = self.flagTab

		# Initialize all boolean type config settings to None
		cfgMainToolBarMoveable = None
		cfgMainToolBarFloatable = None
		cfgKeepOnTop = None
		cfgIsWindowFrameless = None
		cfgShowWindowTitle = None
		cfgDropShadow = None
		cfgShowSysMenu = None
		cfgShadeButton = None
		cfgKeepOnBottom = None
		cfgCustomizeWindow = None
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

		cfgStyleSheet = config.value("styleSheet")
		sheet = None
		if cfgStyleSheet is not None: sheet = cfgStyleSheet.lower().replace(" ", "")  # str(config.value("styleSheet")).replace(" ", "")
		if (sheet is None) or ((sheet not in styleSheets) and (sheet != "default")):
			if sheet is None or sheet == "":
				print("No stylesheet specified. Using default.")
			else:  # noinspection PyTypeChecker
				print("Stylesheet \"" + sheet + "\" could not be found.")
			config.setValue("styleSheet", "default")
		else:
			if enableTrivials: print("Using stylesheet \"" + sheet + "\".")
			config.setValue("styleSheet", sheet)
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

		''' Main Window Flag Configs'''
		# WIP: Add checkboxes for these to config manager
		config.beginGroup("WindowFlags")

		if correctBoolean(config.value("cfgKeepOnTop")) == -1:
			config.setValue("cfgKeepOnTop", False)
		else:
			cfgKeepOnTop = correctBoolean(config.value("cfgKeepOnTop", False, bool))
			config.setValue("cfgKeepOnTop", cfgKeepOnTop)
		# flagTab.windowStaysOnTopCheckBox.setChecked(cfgKeepOnTop)

		if correctBoolean(config.value("cfgIsFrameless")) == -1:
			config.setValue("cfgIsFrameless", False)
		else:
			cfgIsWindowFrameless = correctBoolean(config.value("cfgIsFrameless", False, bool))
			config.setValue("cfgIsFrameless", cfgIsWindowFrameless)
		# flagTab.framelessWindowCheckBox.setChecked(cfgIsWindowFrameless)

		if correctBoolean(config.value("cfgShowTitle")) == -1:
			config.setValue("cfgShowTitle", True)
		else:
			cfgShowWindowTitle = correctBoolean(config.value("cfgShowTitle", True, bool))
			config.setValue("cfgShowTitle", cfgShowWindowTitle)
		# flagTab.windowTitleCheckBox.setChecked(cfgShowWindowTitle)

		if correctBoolean(config.value("cfgDropShadow")) == -1:
			config.setValue("cfgDropShadow", True)
		else:
			cfgDropShadow = correctBoolean(config.value("cfgDropShadow", True, bool))
			config.setValue("cfgDropShadow", cfgDropShadow)
		# self.<CHECKBOX NAME>.setChecked(cfgDropShadow)

		if correctBoolean(config.value("cfgSysMenu")) == -1:
			config.setValue("cfgSysMenu", True)
		else:
			cfgShowSysMenu = correctBoolean(config.value("cfgSysMenu", True, bool))
			config.setValue("cfgSysMenu", cfgShowSysMenu)

		if correctBoolean(config.value("cfgShadeButton")) == -1:
			config.setValue("cfgShadeButton", True)
		else:
			cfgShadeButton = correctBoolean(config.value("cfgShadeButton", True, bool))
			config.setValue("cfgShadeButton", cfgShadeButton)

		# Considering enabling this
		# if correctBoolean(config.value("cfgKeepOnBottom")) == -1:
		# 	config.setValue("cfgKeepOnBottom", False)
		# else:
		# 	cfgKeepOnBottom = correctBoolean(config.value("cfgKeepOnBottom", False, bool))
		# 	config.setValue("cfgKeepOnBottom", cfgKeepOnBottom)

		if correctBoolean(config.value("cfgCustomizeWindow")) == -1:
			config.setValue("cfgCustomizeWindow", True)
		else:
			cfgCustomizeWindow = correctBoolean(config.value("cfgCustomizeWindow", True, bool))
			config.setValue("cfgCustomizeWindow", cfgCustomizeWindow)

		flagTab.updateFlags()  # parent.setflags(retrieveflags)
		# self.parent().setWindowFlags(self.retrieveFlags())

		config.endGroup()

		'''	Other Configs	'''
		cfgTitle = config.value("cfgWindowTitle")
		if (cfgTitle is None) or (cfgTitle == "\n"):
			# This isn't really required, but it makes sure that the config has a value set in the config file even if the field was cleared.
			config.setValue("cfgWindowTitle", "Switchboard")

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
	# print(display.settingsFile.value("WindowFlags/cfgKeepOnTop"))
	display.appPreferences()
	display.show()
	# display.dumpObjectInfo()
	# display.dumpObjectTree()
	sys.exit(app.exec_())
