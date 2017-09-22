from PyQt5.QtWidgets import (
	QPushButton, QAction, QLabel, QCheckBox, QLineEdit, QHBoxLayout,
	QVBoxLayout, QWidget, QDialog, QDialogButtonBox,  # QTabWidget,
	QGroupBox, QGridLayout
	# ,QStyleFactory, QActionGroup, QComboBox
)
# noinspection PyUnusedImports, PyUnresolvedReferences
from PyQt5.QtCore import (Qt, QSettings, QObject)  #QObject not currently used

import sys
import warnings
from QTabWidgetExtras import extendedTabWidget
from Common import *

warnings.warn("Compiling SettingsControl")
enableTrivials = False
# Section####################################### Start Settings Handling ###############################################
class settingsManager(QDialog):
	def __init__ (self, parent = None):
		# noinspection PyArgumentList
		super(settingsManager, self).__init__()
		self.setParent(parent)

		self.settingsFile = QSettings(
				"MySwitchboard.cfg",
				QSettings.IniFormat
		)

		self.settingsFile.setPath(
				QSettings.IniFormat,
				QSettings.UserScope,
				"MySwitchboard.cfg"
		)

		global settingsList, settingEntry
		settingsList = []

		# noinspection PyRedeclaration, PyArgumentList
		class settingEntry(QWidget):
			# CURRENTLY ONLY WORKS WITH WIDGET BASED SETTINGS		FIXME
			def __init__ (self, widget, cfgName):
				super(settingEntry, self).__init__()
				'''	The widget corresponding to the setting	'''
				self.widget = widget
				'''	The "key associated with the setting	'''
				self.cfgName = cfgName
				'''	Add this settingEntry to the list	'''
				settingsList.append(self)
		# self.windowFlags()
		# flags = Qt.WindowFlags()
		# flags = Qt.Dialog
		# self.setWindowFlags(flags)
		# self.show=self.appPreferences()

		self.resize(500, 500)  # TEMPORARY
		'''	create checkboxes for window flag controls	'''
		self.windowStaysOnTopCheckBox = self.flagCheckBox("Keep the window on top?")
		self.framelessWindowCheckBox = self.flagCheckBox("Frameless window mode")
		self.windowTitleCheckBox = self.flagCheckBox("Show title bar?")

		if __name__ == "__main__":  # TEMPORARY
			actQuit = QAction("&Quit", self)
			actQuit.setShortcut("Ctrl+q")
			# noinspection PyUnresolvedReferences
			actQuit.triggered.connect(sys.exit)
			self.addAction(actQuit)
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
	def getCurrentValues (self):
		config = self.settingsFile
		for settingEntry in settingsList:
			setting = settingEntry.widget
			settingName = settingEntry.cfgName
			# TODO: Handle different types, consider handling special cases
			if True:  # setting.isModified()
				print(settingName + " has been changed, but not saved. Refreshing field value.")
				if (type(setting) == QLineEdit) and (setting.isModified()):
					setting.setText(config.value(settingName))
				elif (type(setting) == QLineEdit):
					continue  # Temp
				# elif (type(setting) == QCheckBox):	#Temp
				# 	print("State: " + str(setting.checkState()))	#Temp
				# 	print("Setting: " + str(config.value(settingName)))	#Temp
				# 	# print("Corrected setting: " + str(correctBoolean(config.value(settingName))))	#Temp
				elif (type(setting) == QCheckBox) and (setting.checkState() != correctBoolean(config.value(settingName))):
					if correctBoolean(config.value(settingName)) == True:
						setting.setChecked(True)
					elif correctBoolean(config.value(settingName)) == False:
						setting.setChecked(False)
				elif (type(setting) == QCheckBox):
					continue  # Temp
				elif type(setting) == QPushButton:
					pass
				else:
					print("Setting \"" + settingName + "\" matches no handled type. Its type is " + str(type(setting)))

	'''	Refresh field values ONLY for checkboxes associated with a window flag	'''

	def syncWindowFlagCheckStates (self):
		config = self.settingsFile
		for settingEntry in settingsList:
			setting = settingEntry.widget
			settingName = settingEntry.cfgName
			if settingName.startswith("WindowFlags/"):
				setting.setChecked(correctBoolean(config.value(settingName)))

	'''	Update config file contents to match field values	'''  # TODO: TRY TO FIND A BETTER WAY THAN THIS

	# noinspection PyShadowingNames
	def updateModifiedValues (self):
		config = self.settingsFile
		for settingEntry in settingsList:
			setting = settingEntry.widget
			settingName = settingEntry.cfgName
			# TODO:Handle different types, consider handling special cases
			if True:  # setting.isModified()
				print(settingName + " has been modified. Now saving.")

				if (type(setting) == QLineEdit) and (setting.isModified()):
					config.setValue(settingName, setting.text())
				elif (type(setting) == QCheckBox) and (correctBoolean(config.value(settingName)) != setting.checkState()):
					config.setValue(settingName, setting.checkState())
					pass
				elif type(setting) == QPushButton:
					pass
				else:
					print("Setting \"" + settingName + "\" matches no handled type. Its type is " + str(type(setting)))

	'''	Create check boxes for group boxes	'''

	# Suppress warnings about unresolved references to connect() using noinspection PyUnresolvedReferences
	# noinspection PyShadowingNames, PyUnresolvedReferences
	def flagCheckBox (self, text = "<placeholder>"):
		# Would have prevented a weak warning if it worked, but parameters and nonlocal variables can't have the same name. Using noinspection instead...
		# nonlocal self
		box = QCheckBox(text)

		# Temporarily putting off fixing this until more content has been implemented
		# box.stateChanged.connect(
		# 	wrapper(self.updateFlags, self.parent).call
		# 	# self.updateFlags
		# )

		def Link ():
			wrapper(testPrint, "Flag Toggled").call()

		box.stateChanged.connect(Link)
		return box

	def makeWindowFlagBox (self):  # consider having all the flag-checkboxes automatically added to a list
		windowFlagBox = QGroupBox("Window Flags",
								  self)  # Need to remember to pass self so that windowFlagBox becomes a descendant of settingsManager
		# Create settingEntry for each checkbox
		flag1 = settingEntry(self.windowStaysOnTopCheckBox, "WindowFlags/cfgKeepOnTop")
		flag2 = settingEntry(self.framelessWindowCheckBox, "WindowFlags/cfgIsFrameless")
		flag3 = settingEntry(self.windowTitleCheckBox, "WindowFlags/cfgShowTitle")
		# sync checked states
		self.syncWindowFlagCheckStates()
		# Add checkbox widgets to layout
		flagBoxLayout = QGridLayout()
		flagBoxLayout.addWidget(self.windowStaysOnTopCheckBox)
		flagBoxLayout.addWidget(self.framelessWindowCheckBox)
		flagBoxLayout.addWidget(self.windowTitleCheckBox)
		windowFlagBox.setLayout(flagBoxLayout)
		return windowFlagBox

	# noinspection PyAttributeOutsideInit, noinspection PyArgumentList
	def appPreferences (self):
		if enableTrivials: print("Preferences selected")

		config = self.settingsFile
		global settingEntry
		self.setWindowTitle("Settings")

		# NOTICE: createCheckBox USED TO BE HERE
		# NOTICE: getCurrentValues USED TO BE HERE
		# NOTICE: updateModifiedValues USED TO BE HERE
		# self.update()
		parentLayout = QVBoxLayout()

		#Create the 3 possible responses to the dialog
		responses = QDialogButtonBox(QDialogButtonBox.NoButton, Qt.Horizontal)
		responses.apply = responses.addButton("Accept Changes", QDialogButtonBox.AcceptRole)
		# responses.good = responses.addButton("Okay", QDialogButtonBox.ActionRole)			#reminder: Consider if having a 3rd button is really necessary
		responses.discard = responses.addButton("Discard Changes", QDialogButtonBox.RejectRole)

		def accResp ():
			wrapper(testPrint, "Accepting Changes...").call()

			# Check for and save any changed settings
			self.updateModifiedValues()
			self.accept()  #TEMPORARY? See reminder above
			# print(winTitle.text()); #text, textChanged, textEdited, setValidator, setText. setTooltip. QLineEdit,displayText
			config.sync()
			print("Leaving Settings")  #TEMPORARY? See reminder above

		def rejResp ():
			wrapper(testPrint, "Discarding Changes...").call()
			self.getCurrentValues()
			self.reject()

		# def good ():
		# 	# self.setResult(QDialog.accepted())
		# 	# self.done(QDialog.accepted())
		# 	self.accept()
		# 	getCurrentValues()
		# 	print("Leaving Settings")

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
			# elif sender.text() == "Okay":
			# 	good()

		#When any of the three responses is clicked, go to onClicked
		responses.apply.clicked.connect(onClicked)
		# responses.good.clicked.connect(onClicked)		# see reminder above
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
		windowFlagBox = self.makeWindowFlagBox()
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
		self.flagTab = QWidget()  # placeholder
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
	def updateFlags (self, parent = None):
		config = self.settingsFile
		self.windowFlags()
		flags = Qt.WindowFlags()
		flags = Qt.Dialog  # Without this line, when MainWindow.window is set as parent, anything that would be displayed in its own dialog
		# by appPreferences is instead confined to the geometry of window

		# TODO: None of this part should apply to the settings window
		# TODO: Figure out how to get this to apply to the main window

		# probably going to need to pass this function the parent window or something
		if ((config.value("WindowFlags/cfgKeepOnTop")) == True) or (self.windowStaysOnTopCheckBox.isChecked()):
			flags |= Qt.WindowStaysOnTopHint
		if ((config.value("WindowFlags/cfgIsFrameless")) == True) or (self.framelessWindowCheckBox.isChecked()):
			flags |= Qt.FramelessWindowHint
		if ((config.value("WindowFlags/cfgShowTitle")) == True) or (self.windowTitleCheckBox.isChecked()):
			flags |= Qt.WindowTitleHint
		if ((config.value("WindowFlags/cfgDropShadow")) == True):  # or (self.windowNoDropShadowCheckBox.isChecked()):
			flags |= Qt.NoDropShadowWindowHint
		if ((config.value("WindowFlags/cfgSysMenu")) == True):  # or (self.windowSystemMenuCheckBox.isChecked()):
			flags |= Qt.WindowSystemMenuHint
		if ((config.value("WindowFlags/cfgShadeButton")) == True):  # or (self.windowShadeButtonCheckBox.isChecked()):
			flags |= Qt.WindowShadeButtonHint
		# if ((config.value("WindowFlags/cfgKeepOnBottom")) == True):# or (self.windowStaysOnBottomCheckBox.isChecked()):
		# 	flags |= Qt.WindowStaysOnBottomHint
		if ((config.value("WindowFlags/cfgCustomizeWindow")) == True):  # or (self.customizeWindowHintCheckBox.isChecked()):
			flags |= Qt.CustomizeWindowHint
		# if parent is not None:
		# 	parent.setWindowFlags(flags)
		# else:
		self.setWindowFlags(flags)

	def retrieveFlags (self):  # WIP
		config = self.settingsFile
		flags = Qt.WindowFlags()
		flags = Qt.Window
		if ((config.value("WindowFlags/cfgKeepOnTop")) == True) or (self.windowStaysOnTopCheckBox.isChecked()):
			flags |= Qt.WindowStaysOnTopHint
		if ((config.value("WindowFlags/cfgIsFrameless")) == True) or (self.framelessWindowCheckBox.isChecked()):
			flags |= Qt.FramelessWindowHint
		if ((config.value("WindowFlags/cfgShowTitle")) == True) or (self.windowTitleCheckBox.isChecked()):
			flags |= Qt.WindowTitleHint
		if ((config.value("WindowFlags/cfgDropShadow")) == True):  # or (self.windowNoDropShadowCheckBox.isChecked()):
			flags |= Qt.NoDropShadowWindowHint
		if ((config.value("WindowFlags/cfgSysMenu")) == True):  # or (self.windowSystemMenuCheckBox.isChecked()):
			flags |= Qt.WindowSystemMenuHint
		if ((config.value("WindowFlags/cfgShadeButton")) == True):  # or (self.windowShadeButtonCheckBox.isChecked()):
			flags |= Qt.WindowShadeButtonHint
		# if ((config.value("WindowFlags/cfgKeepOnBottom")) == True):# or (self.windowStaysOnBottomCheckBox.isChecked()):
		# 	flags |= Qt.WindowStaysOnBottomHint
		if ((config.value("WindowFlags/cfgCustomizeWindow")) == True):  # or (self.customizeWindowHintCheckBox.isChecked()):
			flags |= Qt.CustomizeWindowHint
		return flags

	def initSettings (self):
		# NOTE:Is toolbar moveable or locked in place. Is it floatable. Maybe if i figure out how to let the user adjust contents,
		# NOTE: add an option to disable that ability? Enable/disable certain widgets?
		# TODO: Figure out how to add descriptive text into the config file, if at all possible

		config = self.settingsFile  # test=config.setValue("test", 3);    print("test=" + str(config.value("test")))
		#TODO: Add print/logging statements when values need to be reset to default
		'''	Style Configs	'''
		cfgStyle = config.value("primaryStyle")
		if str(config.value("primaryStyle")).capitalize().replace(" ", "") not in validStyles:
			if sys.platform.startswith("win32"):
				config.setValue("primaryStyle", "Windows Vista")
			else:
				config.setValue("primaryStyle", "Fusion")
			if enableTrivials: ("Resetting style to hard default")

		'''	Main Toolbar Configs	'''
		config.beginGroup("MainToolbar")

		cfgMainToolBarPos = config.value("mainToolBarPosition",
										 Qt.LeftToolBarArea)  #Setting defaults like this while also including a case for invalid values may be redundant
		if cfgMainToolBarPos == "\n" or cfgMainToolBarPos not in ["1", "2", "4", "8"]:
			config.setValue("mainToolBarPosition", Qt.LeftToolBarArea)  # Default toolbar position is on the left side

		cfgMainToolBarMoveable = correctBoolean(config.value("isMainToolBarMovable", True))
		if cfgMainToolBarMoveable == -1:
			config.setValue("isMainToolBarMovable", True)  # Main toolbar is movable by default
		elif cfgMainToolBarMoveable != -1:
			config.setValue("isMainToolBarMovable", cfgMainToolBarMoveable)

		cfgMainToolBarFloatable = correctBoolean(config.value("isMainToolBarFloatable", True))
		if cfgMainToolBarMoveable == -1:
			config.setValue("isMainToolBarFloatable", True)  # Main toolbar is floatable by default
		elif cfgMainToolBarMoveable != -1:
			config.setValue("isMainToolBarFloatable", cfgMainToolBarFloatable)

		config.endGroup()

		# WIP: Add checkboxes for these to config manager
		config.beginGroup("WindowFlags")

		cfgKeepOnTop = correctBoolean(config.value("cfgKeepOnTop", False))
		if cfgKeepOnTop == -1:
			config.setValue("cfgKeepOnTop", False)
		elif cfgKeepOnTop != -1:
			config.setValue("cfgKeepOnTop", cfgKeepOnTop)
		self.windowStaysOnTopCheckBox.setChecked(cfgKeepOnTop)

		cfgIsWindowFrameless = correctBoolean(config.value("cfgIsFrameless", False))
		if cfgIsWindowFrameless == -1:
			config.setValue("cfgIsFrameless", False)
		elif cfgIsWindowFrameless != -1:
			config.setValue("cfgIsFrameless", cfgIsWindowFrameless)
		self.framelessWindowCheckBox.setChecked(cfgIsWindowFrameless)

		cfgShowWindowTitle = correctBoolean(config.value("cfgShowTitle", True))
		if cfgShowWindowTitle == -1:
			config.setValue("cfgShowTitle", True)
		elif cfgShowWindowTitle != -1:
			config.setValue("cfgShowTitle", cfgShowWindowTitle)
		self.windowTitleCheckBox.setChecked(cfgShowWindowTitle)

		cfgDropShadow = correctBoolean(config.value("cfgDropShadow", True))
		if cfgDropShadow == -1:
			config.setValue("cfgDropShadow", True)
		elif cfgDropShadow != -1:
			config.setValue("cfgDropShadow", cfgDropShadow)
		# self.<CHECKBOX NAME>.setChecked(cfgDropShadow)

		cfgShowSysMenu = correctBoolean(config.value("cfgSysMenu", True))
		if cfgShowSysMenu == -1:
			config.setValue("cfgSysMenu", True)
		elif cfgShowSysMenu != -1:
			config.setValue("cfgSysMenu", cfgShowSysMenu)

		cfgShadeButton = correctBoolean(config.value("cfgShadeButton", True))
		if cfgShadeButton == -1:
			config.setValue("cfgShadeButton", True)
		elif cfgShadeButton != -1:
			config.setValue("cfgShadeButton", cfgShadeButton)

		# Considering enabling this
		# cfgKeepOnBottom = correctBoolean(config.value("cfgKeepOnBottom",False))
		# if cfgKeepOnBottom == -1:
		# 	config.setValue("cfgKeepOnBottom", False)
		# elif cfgKeepOnBottom != -1:
		# 	config.setValue("cfgKeepOnBottom", cfgKeepOnBottom)

		cfgCustomizeWindow = correctBoolean(config.value("cfgCustomizeWindow", True))
		if cfgCustomizeWindow == -1:
			config.setValue("cfgCustomizeWindow", True)
		elif cfgCustomizeWindow != -1:
			config.setValue("cfgCustomizeWindow", cfgCustomizeWindow)

		self.updateFlags()  # parent.setflags(retrieveflags)
		# self.parent().setWindowFlags(self.retrieveFlags())


		config.endGroup()

		'''	Other Configs	'''
		cfgTitle = config.value("cfgWindowTitle", "I am a window")
		if cfgTitle == "\n":
			# This isn't really required, but it makes sure that the config has a value set in the config file even if the field was cleared.
			config.setValue("cfgWindowTitle", "I am a window")

		cfgCreateSystemTrayIcon = correctBoolean(config.value("cfgShouldCreateTrayIcon", True))
		if cfgCreateSystemTrayIcon == -1:
			config.setValue("cfgShouldCreateTrayIcon", True)
		elif cfgCreateSystemTrayIcon != -1:
			config.setValue("cfgShouldCreateTrayIcon", cfgCreateSystemTrayIcon)

		# Makes sure that default window geometry value is available in case there isn't one in the config
		cfgWindowGeometry = config.value("mainWindowGeometry", defaultWindowGeometry)
		if type(cfgWindowGeometry) is None or cfgWindowGeometry == "\n" or cfgWindowGeometry == "":
			config.setValue("mainWindowGeometry", defaultWindowGeometry)
			if enableTrivials: print("Defaulting geometry")

if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication

	app = QApplication(sys.argv)
	app.setApplicationName("SettingsControl")
	# print(str(app.effectiveWinId()))

	display = settingsManager()

	display.initSettings()
	# print(display.settingsFile.value("WindowFlags/cfgKeepOnTop"))
	display.appPreferences()
	# display.dumpObjectInfo()
	# display.dumpObjectTree()
	sys.exit(app.exec_())
