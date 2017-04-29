import sys
from PyQt5.QtWidgets import (
	QApplication, QMainWindow, QPushButton, QAction, QLabel, QCheckBox,
	QProgressBar, QMessageBox, QComboBox, QDial, QHBoxLayout,
	QVBoxLayout, QTabWidget, QWidget, QDialog, QDialogButtonBox,QStyleFactory,
	QGridLayout, QLineEdit, QActionGroup, QStatusBar,QToolBar, QColorDialog, QGroupBox)
# technically could've used the functions as they are inherited by QMainWindow instead of using QStatusBar and QToolBar directly
from PyQt5.QtGui import QIcon, QClipboard
# from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import (Qt, QObject, QSettings)
import SettingsControl

import Common
defaultWindowGeometry=Common.defaultWindowGeometry
extendedBools=Common.extendedBools
extendedFalsehoods=Common.extendedFalsehoods
extendedTruths=Common.extendedTruths
statusTips=Common.statusTips
validStyles=Common.validStyles
testPrint=Common.testPrint
wrapper=Common.wrapper
# class wrapper(object):
# 	def __init__ (self, func, *args):	self.func = func;		self.args = args
# 	def call (self): return self.func(*self.args)
class picker(QWidget):
	# def __init__(self):
	# 	super(picker,self).__init__()
	# 	self.pickerDialog=self.openColorDialog()
	def openColorDialog(self):
		color = QColorDialog.getColor()
		if color.isValid():		print(color.name())
# extendedBools=[0,1,"t","T","f","F","true","True","false","False"]
# extendedTruths=[1, "t", "T", "true", "True"]
# extendedFalsehoods=[0, "f", "F", "false", "False"]
# statusTips={
#     "fusion":"Set window style to Fusion",
#     "windows":"Set window style to Windows",
#     "vista":"Set window style to Windows Vista",
#     "XP":"Set window style to Windows XP"
#     }
# validStyles=["Windows", "Windowsxp", "Windowsvista", "Fusion"]
# defaultWindowGeometry=b'\x01\xd9\xd0\xcb\x00\x02\x00\x00\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x00\x00\x00\x00\x00\x00\x07\x80'

class window(QMainWindow):
	def __init__ (self):
		super(window, self).__init__()
		print("Starting to do things")
		self.setObjectName("Mother Window")# print("I am the "+ self.objectName())
		self.setAttribute(Qt.WA_QuitOnClose, True)#FIXME:Ensures that closing the main window also closes the preferences window
		self.clip=QApplication.clipboard()#System-wide clipboard
		# self.pickerButton=self.clickButton("Pipette",QColorDialog.getColor)

					#Configs
		# self.settings=SettingsControl.initSettings()
		# settingsManager=SettingsControl.settingsManager
		# self.settings=settingsManager.settingsFile
		tq=SettingsControl.settingsManager()
		tq.initSettings()
		self.settings=tq.settingsFile
		self.themeControl(str(self.settings.value("primaryStyle")).replace(" ", ""))  # Sets the window style to the configured value
		# print(self.settings.allKeys())

		# setup window aspects
		self.setWindowTitle(self.settings.value("cfgWindowTitle"))
		self.setWindowIcon(QIcon('logo.png'))
		self.declareActions()

		self.setStatusBar(QStatusBar(self))
		self.XY=QLabel("Cursor:") # TODO: Make this come with something to display the numerical position of the cursor; might involve the timerEvent of QStatusBar
		# self.statusBar.addPermanentWidget(self.XY)
		QStatusBar.addPermanentWidget(self.statusBar(),self.XY)

		#TODO: Check if status bar properly has its QSizeGrip, using isSizeGripEnabled()

		self.topMenu()
		self.mainToolBar = QObject

		# self.preferencesDialog = SettingsControl.settingsManager
		self.setupToolBars()
		#NOTE: for QMainWindow, do a find for things with menu, status, tab, tool

		pop=self.basicButton('test', self.popup, None, 25, 100)

		box = self.basicCheckBox(self.editTitle)

		self.bar = self.progressBar(325, 75, 160, 28)
		self.doProgress = self.basicButton('Increment Progress', self.progress, "", 200, 75)

		clearClipboard= self.basicButton("Clear Clipboard", self.clip.clear)#Button which clears the system clipboard
		#print(self.clip.text())#print clipboard text
		Dial=self.dial(1, 100, 300)

		self.pageBar = QTabWidget(self)  # TabWidget is a QWidget
		self.tab1 = QWidget()  # ;self.tab1.adjustSize()
		self.tab2 = QWidget()  # ;self.tab2.adjustSize()


		tab1Layout= QVBoxLayout()
		tab1Layout.addStretch(1)
		tab1Layout.addWidget(pop)
		tab1Layout.addWidget(clearClipboard)
		tab1Layout.addWidget(box)
		tab1Layout.addWidget(Dial)

		progressBox = QHBoxLayout()
		progressBox.addStretch(1)
		progressBox.addWidget(self.doProgress)
		progressBox.addWidget(self.bar)

		self.tab1.setLayout(tab1Layout)
		self.tab2.setLayout(progressBox)#previously took progressBox as param


		self.pageBar.addTab(self.tab1, "tab1")
		self.pageBar.addTab(self.tab2, "tab2")
		# self.mainToolBar

		# tesT=QVBoxLayout()
		# tesT.addWidget(self.mainToolBar)
		# tesT.addWidget(self.pageBar)
		# self.setLayout(tesT)
		self.mainToolBar.addWidget(self.pageBar)
		# self.mainToolBar.addAction(self.actCopy)
		# self.mainToolBar.setLayout=QHBoxLayout(self)

		# make the pageBar occupy everything below the toolbar.
		# anything else being displayed must be part of a tab,
		# otherwise it will end up being rendered behind the pageBar
		# self.setCentralWidget()

		tempPref=self.basicButton('Options', tq.appPreferences(), None, 300, 300)

		self.restoreGeometry(self.settings.value("mainWindowGeometry"))
		print("Window width:"+ str(self.width()))
		print("Window height:"+ str(self.height()))
		print("done init")
	#Declare application wide Actions
	# noinspection PyUnresolvedReferences
	def declareActions (self):  # WIP
		# cut
		self.actCut = QAction("Cu&t", self)
		self.actCut.setShortcut("Ctrl+x")

		def Link (): wrapper(testPrint, "Cut").call()
		self.actCut.triggered.connect(Link)

		# copy
		self.actCopy = QAction("&Copy", self)
		self.actCopy.setShortcut("Ctrl+c")

		def Link (): wrapper(testPrint, "Copy").call()
		self.actCopy.triggered.connect(Link)

		# paste
		self.actPaste = QAction("&Paste", self)
		self.actPaste.setShortcut("Ctrl+v")

		def Link (): wrapper(testPrint, "Paste").call()
		self.actPaste.triggered.connect(Link)

		# quit
		self.actQuit = QAction("&Quit", self)
		self.actQuit.setShortcut("Ctrl+q")
		# self.actQuit.triggered.connect(endProgram)
		# self.actQuit.setToolTip("Close the Application")
		self.actQuit.setStatusTip("Close the application")
		self.actQuit.triggered.connect(self.closeEvent)

	#Simple button with default parameters for position, label, and tooltip(none)
	# noinspection PyUnresolvedReferences
	def basicButton (self, text = 'test', func = None, tip = None, X = 200, Y = 200):
		btn = QPushButton(text, self)
		btn.adjustSize()
		btn.move(X, Y)
		btn.setToolTip(tip)

		if isinstance(func, wrapper):
			def link ():    func.call()
			# print("Calling wrapped function according to button press")
			btn.triggered.connect(link)
		# might need to be clicked instead of triggered
		elif func is not None:  btn.clicked.connect(func)
		else:   print("no function");   pass
		return btn

	#Tri-state checkbox     WIP
	def triCheckBox (self, func = None, text = 'test', X = 25, Y = 75):
		self.basicCheckBox(func, text, X, Y, True)

	#TODO:Rewrite
	#Simple checkbox with default parameters for position and label, and handling for tri-state boxes
	# noinspection PyUnresolvedReferences
	def basicCheckBox (self, func = None, text = 'test', X = 25, Y = 75, isTri = False):
		checkBox = QCheckBox(text, self)
		checkBox.adjustSize()
		checkBox.move(X, Y)
		if isTri == True:   checkBox.setTristate(True)
		if func is not None:    checkBox.stateChanged.connect(func)
		return checkBox

	# Round dial/knob        WIP
	def dial (self, func = None, X = 200, Y = 200, radius = 50, wrap = False):
		knob = QDial(self)
		knob.move(X, Y)
		knob.resize(radius, radius)
		knob.setWrapping(wrap)

		if func is not None:
			func
		# TODO:something something show number in a box nearby

		return knob
	# "Template" function for a toolbar button with an icon
	def toolBar_Icon (self, icon, func, tooltip, statustip = "Null"):
		item = QAction(QIcon(icon), tooltip, self)
		if statustip != "Null": item.setStatusTip(statustip)
		# noinspection PyUnresolvedReferences
		if func is not None:item.triggered.connect(func)
		else: print("One or more icon type items on your toolbar has no function")
		return item

	# "Template" function for a text-only toolbar button
	def toolBar_Text (self, text, func):
		item = QAction(text, self)
		# noinspection PyUnresolvedReferences
		if func is not None:item.triggered.connect(func)
		else: print("One or more text type items on your toolbar has no function")
		return item

	# Add toolbars and populate them with buttons
	def setupToolBars (self):
		# Make buttons
		iconB = self.toolBar_Icon(
				"logo.png", testPrint, "icon", "Do something"
		)
		textB = self.toolBar_Text("&Textual Button", testPrint)

		# Make toolbars
		self.mainToolBar = QToolBar("Main Toolbar")

		# Add toolbars to window. CRITICAL STEP
		mainToolBarPosition=int(self.settings.value("MainToolbar/mainToolBarPosition"))
		print("Main toolbar pos: " + str(mainToolBarPosition))
		self.mainToolBar.setFloatable(self.settings.value("MainToolbar/isMainToolBarFloatable"))
		self.mainToolBar.setMovable(self.settings.value("MainToolbar/isMainToolBarMovable"))
		self.addToolBar(mainToolBarPosition, self.mainToolBar)

		# Add buttons to toolbars
		self.mainToolBar.addAction(iconB)
		self.mainToolBar.addAction(textB)

	# "Template" function for a simple menu item
	def menuItem (self, func, name, tip = None, shortcut = "Null", isToggle=False, group=None):
		item = QAction(name, self)  # self reminder: item is now a QAction
		item.setStatusTip(tip)
		if shortcut != "Null": item.setShortcut(shortcut) # ;else: print("no shortcut for menu item \""+name+"\"")
		if isToggle !=False: item.setCheckable(True)
		if group is not None: group.addAction(item)

		if isinstance(func, wrapper):
			def link ():	func.call()
			# noinspection PyUnresolvedReferences
			item.triggered.connect(link)
		elif func is not None:
			#print(func.__name__ + " is not a wrapper. It is a " + type(func).__name__)
			# noinspection PyUnresolvedReferences
			item.triggered.connect(func)
		else: print("Menu item \"" + name + "\" has no function")
		return item

	# Add menus and populate them with actions
	def topMenu (self):
		config=self.settings  #; self.statusBar()
		mainMenu = self.menuBar()

		# Make menu items
		prefs = self.menuItem(SettingsControl.appPreferences(), "Preferences","View and edit application settings")
		prefs.setMenuRole(QAction.PreferencesRole)

		styleGroup=QActionGroup(mainMenu)
		windows = wrapper(self.themeControl, "Windows")
		winVista = wrapper(self.themeControl, "Windowsvista")
		winXP = wrapper(self.themeControl, "Windowsxp")
		fusion = wrapper(self.themeControl, "Fusion")
		style1 = self.menuItem(fusion, "Fusion", statusTips["fusion"], isToggle=True, group=styleGroup)
		style2 = self.menuItem(windows, "Windows", statusTips["windows"], isToggle=True, group=styleGroup)
		style3 = self.menuItem(winVista, "Windows Vista", statusTips["vista"], isToggle=True, group=styleGroup)
		style4 = self.menuItem(winXP, "Windows XP", statusTips["XP"], isToggle=True, group=styleGroup)
		for style in styleGroup.actions():
			# print("style: "+str(style.text()).capitalize().replace(" ", "") + "	setting: "+config.value("primaryStyle"))
			if (str(style.text()).capitalize().replace(" ", ""))==config.value("primaryStyle"):style.setChecked(True)
			# Makes sure that the configured style appears as checked on load
		style3.setText(style3.text() + " (Default)")

		colorPicker=self.menuItem(QColorDialog.getColor,"Color Picker")
		# TODO: Reset layout of window to default?
		#resetPlacement = self.menuItem(None, "Reset Window Layout", "Reset the window layout to default")

		# Make menus
		fileMenu = mainMenu.addMenu("File")
		editMenu = mainMenu.addMenu("Edit")
		viewMenu = mainMenu.addMenu("View")

		styleMenu = viewMenu.addMenu("Styles")
		layoutMenu = viewMenu.addMenu("Layout")

		# Add actions to menus
		fileMenu.addAction(self.actQuit)
		fileMenu.addAction(prefs)

		editMenu.addAction(self.actCopy)
		editMenu.addAction(self.actCut)
		editMenu.addAction(self.actPaste)

		viewMenu.addAction(colorPicker)

		layoutMenu.addAction(self.menuItem(testPrint, None))  # TODO:give meaningful functions later

		styleMenu.addAction(style1)
		styleMenu.addAction(style2)
		styleMenu.addAction(style3)
		styleMenu.addAction(style4)
		pass

	def themeControl (self, text):
		print("Setting style to " + text)
		QApplication.setStyle(QStyleFactory.create(text))
		self.settings.setValue("primaryStyle",text)

	# Progress bar           WIP
	def progressBar (self, X = 25, Y = 75, length = 100, height = 30):
		bar = QProgressBar(self)
		bar.setGeometry(X, Y, length, height)

		return bar


	# Basic,does nothing much, pop-up window prompt; probably wont make a template
	def popup (self):
		choice = QMessageBox(self)
		choice.setText("What do you do?")  # move to center of popup
		Boring = choice.addButton(
				"Don't push Arnold",
				QMessageBox.AcceptRole)
		Arnold = choice.addButton(
				"Push Arnold (you know you want to....)",
				QMessageBox.ActionRole)
		Exit = choice.addButton(QMessageBox.Cancel)
		Exit.hide()

		choice.setEscapeButton(Exit)
		choice.setDefaultButton(Arnold)
		choice.exec()

		if choice.clickedButton() is Arnold:    print("*Heavy Austrian accent* OUCH!")
		elif choice.clickedButton() is Boring:  print("Well you're no fun")		# ...yeah, I had gotten frustrated at that time, and decided to be a bit silly
	def editTitle (self, state):
		if state == Qt.Unchecked:   self.setWindowTitle("Temporary Title")
		else:   self.setWindowTitle(self.settings.value("cfgWindowTitle"))
	# there has to be a way to specify which progress bar this is for, but for the life of me I can't think of how.
	# Cross that bridge if/when I come to it
	def progress (self):
		if self.bar.value() < 100:
			self.bar.setValue(self.bar.value() + 1)
			if self.bar.value() == 100: 	print("Progress: Done")
			elif self.bar.value() % 10 == 0:    print("Progress: " + str(self.bar.value()))
		else: pass

	def closeEvent(self, *args, **kwargs):
		self.settings.setValue("mainWindowGeometry", self.saveGeometry())
		# print("Saving Geometry")
		# print(self.settings.value("mainWindowGeometry"))
		# print(self.saveGeometry())
		self.close()
#Section############################### Start Test Functions #######################################
	def clickButton (self, text = 'test', func = None, tip = None, X = 200, Y = 200):
		btn = QPushButton(text, self)
		btn.adjustSize()
		btn.move(X, Y)
		btn.setToolTip(tip)

		if isinstance(func, wrapper):
			def link ():func.call()
			btn.clicked.connect(link)
		else:print("no function");pass
		return btn
#Section############################### End Test Functions #######################################

def endProgram ():    print("Goodbye");  sys.exit()
def testPrint (text = "Debug"): print(text)

def run ():
	app = QApplication(sys.argv)
	app.setApplicationName("My Switchboard")
	#app.setApplicationDisplayName("My Switchboard")
	display = window()
	display.show()
	sys.exit(app.exec_())

run()