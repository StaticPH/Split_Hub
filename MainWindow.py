from PyQt5.QtWidgets import (
	QMainWindow, QProgressBar, QMessageBox, QDial, QHBoxLayout,
	QVBoxLayout, QTabWidget,
	QActionGroup, QStatusBar, QToolBar, QColorDialog, QSystemTrayIcon, QMenu
	# Already imported elsewhere, change "import settingsManager" to "import *" to make the following imports redundant
, QWidget, QPushButton, QAction, QLabel, QCheckBox
)
from PyQt5.QtCore import Qt, QObject, QByteArray, QVariant
from PyQt5.QtGui import QIcon, QClipboard, QContextMenuEvent

from StyleHandler import *
from settings.SettingsControl import settingsManager
from QTabWidgetExtras import extendedTabWidget
from Common import *
enableTrivials = False


# noinspection PyUnresolvedReferences
class trayItem(QSystemTrayIcon):
	# maybe:Add an action to the context menu that will disable(and hide) the tray icon
	# maybe:It would need a tooltip mentioning that it would need to be re-enabled via the config or the menu
	# considering the addition of other context menu items
	def __init__ (self, parent, icon = None):
		super(trayItem, self).__init__()
		self.setParent(parent)
		print("trayItem's parent is : " + str(self.parent.__name__) + "\t" + str(self.parent()))
		self.setIcon(QIcon(icon))
		self.setToolTip("Switchboard")
		context = self.rightClickResponse()
		self.setContextMenu(context)
		self.activated.connect(self.clickRestraint)

	# Be sure that right clicking properly brings up the context menu, rather than triggering the same response as a left click
	def clickRestraint (self, clickType):
		if clickType == self.Trigger:
			self.leftClickResponse()

	def leftClickResponse (self):
		parent = self.parent()
		if parent.isMinimized():
			parent.activateWindow()
			parent.showNormal()
		else:
			parent.showMinimized()
			# print("Should be minimized? " + str(parent.isMinimized()))
			pass  # annoyance where things dont want to collapse

	def rightClickResponse (self):
		parent = self.parent()
		menu = QMenu(parent)

		quitAction = QAction("&Quit", self)
		quitAction.triggered.connect(parent.closeEvent)
		menu.addAction(quitAction)

		clearClip = QAction("Clear Clipboard", self)
		clearClip.triggered.connect(parent.clip.clear)
		menu.addAction(clearClip)

		colorPicker = QAction("Color Picker", self)
		colorPicker.triggered.connect(QColorDialog.getColor)
		menu.addAction(colorPicker)
		return menu


class mainToolBar(QToolBar):
	# noinspection PyUnresolvedReferences
	def __init__ (self, parent = None):
		super(mainToolBar, self).__init__()
		self.setParent(parent)
		self.settings = parent.settings

		self.setWindowTitle("Main Toolbar")
		self.toolBarPosition = int(self.settings.value("MainToolbar/mainToolBarPosition"))

		self.popupMenu = QMenu()
		self.popupMenu.setToolTipsVisible(True)

		# Create QActions with 1st parameter 'QIcon(None)' to make tooltips visible, and 3rd parameter 'self' to make status tips visible
		self.locked = QAction(QIcon(None), "Docked Mode", self)
		self.locked.setCheckable(True)
		self.locked.setStatusTip("Lock(/unlock(dock/undock) the toolbar")
		self.locked.triggered.connect(self.toggleDockingMode)

		self.floatingSwitch = QAction(QIcon(None), "Floatable Mode", self)
		self.floatingSwitch.setCheckable(True)
		self.floatingSwitch.setStatusTip("Enable/disable floating the toolbar as a separate window.")
		self.floatingSwitch.setToolTip(
				"NOTE: Disabling does not automatically unfloat the toolbar.\n" +
				"Moving the toolbar a little bit will unfloat it and return it to its docked position in the window"
		)
		self.floatingSwitch.triggered.connect(self.toggleFloatingMode)

		self.popupMenu.addAction(self.floatingSwitch)
		self.popupMenu.addAction(self.locked)
		self.refreshChecks()

	def refreshProperties (self):
		self.setFloatable(self.settings.value("MainToolbar/isMainToolBarFloatable"))
		self.setMovable(self.settings.value("MainToolbar/isMainToolBarMovable"))

	def refreshChecks (self):
		# self.locked should be checked when self.isMovable() == False, so that the it is checked when locked in place
		self.locked.setChecked(negate(self.isMovable()))
		# self.floatingSwitch should be checked when self.isFloatable() == True, so that it is checked when the toolbar can float
		self.floatingSwitch.setChecked(self.isFloatable())

	def contextMenuEvent (self, event):
		pos = None  # This is just to make the inspector shut up, and is probably even considered incorrect practice for Python
		if event.reason() == QContextMenuEvent.Mouse:
			pos = event.globalPos()
		# item = self.actionAt(event.pos())
		if pos is not None:
			self.popupMenu.popup(pos)

	# noinspection PyArgumentList
	def toggleDockingMode (self):
		self.setMovable(negate(self.isMovable()))
		self.locked.setChecked(negate(self.isMovable()))
		self.settings.setValue("MainToolbar/isMainToolBarMovable", self.isMovable())
		self.refreshProperties()
		# QApplication.setStyle(QStyleFactory.create(text))
		self.setStyle(QStyleFactory.create(self.settings.value("Style_Options/primaryStyle")))

	def toggleFloatingMode (self):
		self.setFloatable(negate(self.isFloatable()))
		self.floatingSwitch.setChecked(self.isFloatable())
		self.settings.setValue("MainToolbar/isMainToolBarFloatable", self.isFloatable())
		self.refreshProperties()

	'''	"Template" function for a toolbar button with an icon	'''
	# noinspection PyUnresolvedReferences
	def toolBar_Icon (self, icon, func, tooltip, statustip = "Null"):
		item = QAction(QIcon(icon), tooltip, self)

		if statustip != "Null":
			item.setStatusTip(statustip)

		if func is not None:
			item.triggered.connect(func)
		else:
			print("One or more icon type items on your toolbar has no function")

		return item

	'''	"Template" function for a text-only toolbar button	'''
	# noinspection PyUnresolvedReferences
	def toolBar_Text (self, text, func):
		item = QAction(text, self)

		if func is not None:
			item.triggered.connect(func)
		else:
			print("One or more text type items on your toolbar has no function")

		return item

	'''	Add toolbars and populate them with buttons	'''
	def setup (self):
		# Make buttons
		iconB = self.toolBar_Icon(
				"assets/logo.png", testPrint, "icon", "Do something"
		)
		textB = self.toolBar_Text("&Textual Button", testPrint)

		# Add buttons to toolbars
		self.addAction(iconB)
		self.addAction(textB)


class window(QMainWindow):
	def __init__ (self):  # noinspection PyArgumentList
		super(window, self).__init__()
		self.styler = StyleHandler(True)
		self.setObjectName("Mother Window")  # print("I am the "+ self.objectName())
		self.setAttribute(Qt.WA_QuitOnClose, True)  # FIXME:Ensures that closing the main window also closes the preferences window

		'''System-wide clipboard'''
		# noinspection PyArgumentList
		self.clip = QApplication.clipboard()
		# self.pickerButton=self.clickButton("Pipette",QColorDialog.getColor)

		'''Configs'''
		self.settingsMan = settingsManager(self)
		# self.settingsMan.setParent(self)
		self.settingsMan.initSettings()
		self.settings = self.settingsMan.settingsFile
		self.settingsMan.appPreferences()  # moved this from the last thing in init before checking if a tray icon should be created
		tempPref = self.basicButton('Options', self.settingsMan.show, None, 300, 300)  # temp

		# self.windowFlags()  # WIP
		# # self.settingsMan.updateFlags()  # WIP
		# # flags = Qt.WindowFlags()
		# flags = self.settingsMan.retrieveFlags()  # WIP
		# self.setWindowFlags(flags)
		# flags = Qt.WindowFlags()  # WIP
		# print("Window type mask= " + str(flags & Qt.WindowType_Mask.__class__.__qualname__))				# WIP
		# if flags and Qt.WindowStaysOnTopHint:  # WIP
		# 	print("Window should be staying on top")  # WIP
		# else:  # WIP
		# 	print("Flags not set")  # WIP
		# print(str(flags))																					# WIP
		if enableTrivials: ("Window flags: " + str(self.windowFlags()))  # WIP

		'''Sets the window style to the configured value'''
		self.styler.applyStyle(str(self.settings.value("Style_Options/primaryStyle")).replace(" ", ""))
		self.styler.loadStyleSheet(str(self.settings.value("Style_Options/styleSheet")).replace(" ", ""))

		'''setup window aspects'''
		self.setWindowTitle(self.settings.value("cfgWindowTitle"))
		self.setWindowIcon(QIcon('assets/logo.png'))
		self.declareActions()

		self.setStatusBar(QStatusBar(self))
		self.XY = QLabel(
				"Cursor:")  # TODO: Make this come with something to display the numerical position of the cursor; might involve the timerEvent of QStatusBar
		# self.statusBar.addPermanentWidget(self.XY)
		QStatusBar.addPermanentWidget(self.statusBar(), self.XY)

		# TODO: Check if status bar properly has its QSizeGrip, using isSizeGripEnabled()

		self.clearClipboardButton = self.basicButton("Clear Clipboard", self.clip.clear)  # Button which clears the system clipboard
		# if enableTrivials: print(self.clip.text())#print clipboard text

		self.topMenu()
		self.mainToolBar = mainToolBar(self)
		self.mainToolBar.setup()
		'''Add toolbars to window. CRITICAL STEP'''
		self.addToolBar(self.mainToolBar.toolBarPosition, self.mainToolBar)

		# NOTE: for QMainWindow, do a find for things with menu, status, tab, tool

		self.pageBar = self.makePageBar()
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
		# self.setCentralWidget(self.mainToolBar)
		pass
		# tempFlagCheck = self.basicCheckBox( self.test )

		if self.settings.value("cfgShouldCreateTrayIcon") == True:
			self.trayObject = trayItem(self, 'assets/logo.png')
			# maybe move the addition of actions and setting of the context menu to here
			self.trayObject.show()

		if self.settings.value("mainWindowGeometry"):
			# G = self.restoreGeometry(bytes(self.settings.value("mainWindowGeometry")))
			# print(G)
			a = QByteArray(self.saveGeometry())
			print(a)
			print("ZIL")
			b = self.restoreGeometry(
				b'\x04\xb0\x00\x00\x02\xd7\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x00\x00\x00\x00\x00\x00\x07\x80').to_bytes()
			print(b)
		# t = self.geo
		else:
			self.restoreGeometry(defaultWindowGeometry)
		self.updateFlags()

		if enableTrivials:
			("Window width:" + str(self.width()))
			print("Window height:" + str(self.height()))
			print("done init")

	# Declare application wide Actions
	# noinspection PyUnresolvedReferences,PyAttributeOutsideInit
	def declareActions (self):  # WIP		#TODO: Consider shifting this to Common
		# Cut
		self.actCut = QAction("Cu&t", self)
		self.actCut.setShortcut("Ctrl+x")

		def Link ():
			wrapper(testPrint, "Cut").call()

		self.actCut.triggered.connect(Link)

		# Copy
		self.actCopy = QAction("&Copy", self)
		self.actCopy.setShortcut("Ctrl+c")

		def Link ():
			wrapper(testPrint, "Copy").call()

		self.actCopy.triggered.connect(Link)

		# Paste
		self.actPaste = QAction("&Paste", self)
		self.actPaste.setShortcut("Ctrl+v")

		def Link ():
			wrapper(testPrint, "Paste").call()

		self.actPaste.triggered.connect(Link)

		# Quit
		self.actQuit = QAction("&Quit", self)
		self.actQuit.setShortcut("Ctrl+q")
		self.actQuit.setStatusTip("Close the application")
		self.actQuit.triggered.connect(self.closeEvent)

	# Simple button with default parameters for position, label, and tooltip(none)
	# noinspection PyUnresolvedReferences
	def basicButton (self, text = 'test', func = None, tip = None, X = 200, Y = 200):
		btn = QPushButton(text, self)
		btn.adjustSize()
		btn.move(X, Y)
		btn.setToolTip(tip)

		if isinstance(func, wrapper):
			def link ():
				func.call()

			# print("Calling wrapped function according to button press")
			btn.triggered.connect(link)
		# might need to be clicked instead of triggered
		elif func is not None:
			btn.clicked.connect(func)
		else:
			print("no function")

		return btn

	# TODO:Rewrite
	# Simple checkbox with default parameters for position and label, and handling for tri-state boxes
	# noinspection PyUnresolvedReferences
	def basicCheckBox (self, func = None, text = 'test', X = 25, Y = 75, isTri = False):
		checkBox = QCheckBox(text, self)
		checkBox.adjustSize()
		checkBox.move(X, Y)

		if isTri == True:
			checkBox.setTristate(True)

		if func is not None:
			checkBox.stateChanged.connect(func)

		return checkBox

	# Round dial/knob        WIP
	def dial (self, func = None, X = 200, Y = 200, radius = 50, wrap = False):
		knob = QDial(self)
		knob.move(X, Y)
		knob.resize(radius, radius)
		knob.setWrapping(wrap)

		if func is not None:
			# func
			pass
		# TODO:something something show number in a box nearby

		return knob

	# "Template" function for a simple menu item
	def menuItem (self, func, name, tip = None, shortcut = "Null", isToggle = False, group = None):
		item = QAction(name, self)  # self reminder: item is now a QAction
		item.setStatusTip(tip)

		if shortcut != "Null":
			item.setShortcut(shortcut)  # ;else: print("no shortcut for menu item \""+name+"\"")
		if isToggle != False:
			item.setCheckable(True)
		if group is not None:
			group.addAction(item)

		if isinstance(func, wrapper):
			def link ():
				func.call()

			# noinspection PyUnresolvedReferences
			item.triggered.connect(link)
		elif func is not None:
			# print(func.__name__ + " is not a wrapper. It is a " + type(func).__name__)
			# noinspection PyUnresolvedReferences
			item.triggered.connect(func)
		else:
			print("Menu item \"" + name + "\" has no function")

		return item

	# Add menus and populate them with actions
	def topMenu (self):
		config = self.settings  # ; self.statusBar()
		mainMenu = self.menuBar()

		# Make menu items
		prefs = self.menuItem(self.settingsMan.show, "Preferences", "View and edit application settings")
		prefs.setMenuRole(QAction.PreferencesRole)

		styleGroup = QActionGroup(mainMenu)  # QActionGroup is exclusive by default
		# maybe: Move construction of styles(and their associated names, tooltips, etc) into Common.py?
		# TODO: figure out a way to programmatically add available styles to the menu
		windows = wrapper(self.styler.applyStyle, "Windows")
		winVista = wrapper(self.styler.applyStyle, "Windowsvista")
		winXP = wrapper(self.styler.applyStyle, "Windowsxp")
		fusion = wrapper(self.styler.applyStyle, "Fusion")
		# TODO:only add a menu item if its name is in QStyleFactory.keys()
		style1 = self.menuItem(fusion, "Fusion", statusTips ["fusion"], isToggle = True, group = styleGroup)
		style2 = self.menuItem(windows, "Windows", statusTips ["windows"], isToggle = True, group = styleGroup)
		style3 = self.menuItem(winVista, "Windows Vista", statusTips ["vista"], isToggle = True, group = styleGroup)
		style4 = self.menuItem(winXP, "Windows XP", statusTips ["XP"], isToggle = True, group = styleGroup)

		# Makes sure that the configured style appears as checked on load
		for style in styleGroup.actions():
			# print("style: "+str(style.text()).capitalize().replace(" ", "") + "	setting: "+config.value("Style_Options/primaryStyle"))
			if (str(style.text()).capitalize().replace(" ", "")) == config.value("Style_Options/primaryStyle").capitalize().replace(" ", ""):
				style.setChecked(True)
		if sys.platform.startswith("win32"):
			style3.setText(style3.text() + " (Default)")  # On Windows operating systems, mark "Windows Vista" as the default style
		else:
			style1.setText(style1.text() + " (Default)")  # On non-Windows operating systems, mark "Fusion" as the default style

		# TODO: Reset layout of window to default?
		# resetPlacement = self.menuItem(None, "Reset Window Layout", "Reset the window layout to default")
		colorPicker = self.menuItem(QColorDialog.getColor, "Color Picker")
	
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

	# # noinspection PyArgumentList
	# def themeControl (self, text):
	# 	if enableTrivials: print("Setting style to " + text)
	# 	QApplication.setStyle(QStyleFactory.create(text))
	# 	self.settings.setValue("Style_Options/primaryStyle", text)

	def updateFlags (self):
		config = self.settings
		self.windowFlags()
		flags = Qt.WindowFlags()
		flags = Qt.Window
		if ((config.value("WindowFlags/cfgKeepOnTop")) == True):
			flags |= Qt.WindowStaysOnTopHint
		if ((config.value("WindowFlags/cfgIsFrameless")) == True):
			flags |= Qt.FramelessWindowHint
		self.setWindowFlags(flags)
		self.show()

	'''	Move all of the code for the contents of the pageBar out of the __init__	'''
	# noinspection PyArgumentList
	def makePageBar (self):
		pageBar = QTabWidget(self)  # Note: TabWidget is a QWidget
		tab1 = QWidget()  # ;self.tab1.adjustSize()
		tab2 = QWidget()  # ;self.tab2.adjustSize()

		pop = self.basicButton('test', self.popup, None, 25, 100)
		box = self.basicCheckBox(self.editTitle)
		Dial = self.dial(1, 100, 300)
		bar = self.progressBar(325, 75, 160, 28)
		doProgress = self.clickButton('Increment Progress', wrapper(self.progress, bar), "", 200, 75)

		tab1Layout = QVBoxLayout()
		tab1Layout.addStretch(1)
		tab1Layout.addWidget(pop)
		tab1Layout.addWidget(self.clearClipboardButton)
		tab1Layout.addWidget(box)
		tab1Layout.addWidget(Dial)

		progressBox = QHBoxLayout()
		progressBox.addStretch(10)
		progressBox.addWidget(doProgress)
		progressBox.addWidget(bar)

		tab1.setLayout(tab1Layout)
		tab2.setLayout(progressBox)  # previously took progressBox as param

		pageBar.addTab(tab1, "tab1")
		pageBar.addTab(tab2, "tab2")

		return pageBar

	# Progress bar           WIP
	def progressBar (self, X = 25, Y = 75, length = 100, height = 30):
		bar = QProgressBar(self)
		bar.setGeometry(X, Y, length, height)

		return bar

	'''	Basic,does nothing much, pop-up window prompt; probably wont make a template function	'''
	def popup (self):
		choice = QMessageBox(self)
		choice.setText("What do you do?")  # move to center of popup

		Boring = choice.addButton(
				"Don't push Arnold",
				QMessageBox.AcceptRole
		)

		Arnold = choice.addButton(
				"Push Arnold (you know you want to....)",
				QMessageBox.ActionRole
		)

		Exit = choice.addButton(QMessageBox.Cancel)
		Exit.hide()

		choice.setEscapeButton(Exit)
		choice.setDefaultButton(Arnold)
		choice.exec()

		if choice.clickedButton() is Arnold:
			print("*Heavy Austrian accent* OUCH!")
		elif choice.clickedButton() is Boring:
			print("Well you're no fun")  # ...yeah, I had gotten frustrated at that time, and decided to be a bit silly

	def editTitle (self, state):
		if state == Qt.Unchecked:
			self.setWindowTitle("Temporary Title")
		else:
			self.setWindowTitle(self.settings.value("cfgWindowTitle"))

	# There has to be a way to specify which progress bar this is for, but for the life of me I can't think of how.
	# Cross that bridge if/when I come to it
	def progress (self, bar):
		if bar.value() < 100:
			bar.setValue(bar.value() + 1)

			if bar.value() == 100:
				print("Progress: Done")
			elif bar.value() % 10 == 0:
				print("Progress: " + str(bar.value()))
		return bar

	def closeEvent (self, *args, **kwargs):
		self.settings.setValue("mainWindowGeometry", self.saveGeometry())
		# print("Saving Geometry")
		# print(self.settings.value("mainWindowGeometry"))
		# print(self.saveGeometry())
		self.settings.setValue("Style_Options/primaryStyle", self.styler.styleName)
		if self.settings.value("cfgShouldCreateTrayIcon") == True:
			self.trayObject.deleteLater()
		self.close()

	# Section############################### Start Test Functions #######################################
	def clickButton (self, text = 'test', func = None, tip = None, X = 200, Y = 200):
		btn = QPushButton(text, self)
		btn.adjustSize()
		btn.move(X, Y)
		btn.setToolTip(tip)

		if isinstance(func, wrapper):
			def link ():
				func.call()

			# noinspection PyUnresolvedReferences
			btn.clicked.connect(link)
		else:
			print("no function")
			pass

		return btn


# Section############################### End Test Functions #######################################

def endProgram ():
	print("Goodbye")
	sys.exit()


def testPrint (text = "Debug"):
	print(text)


if __name__ == "__main__":
	import sys

	# from assets.stylesheets import DarkS
	# noinspection PyUnusedImports
	# import style_rc
	app = QApplication(sys.argv)
	app.setApplicationName("My Switchboard")
	# app.setApplicationDisplayName("My Switchboard")

	display = window()
	# styleSheet = str(display.settings.value("Style_Options/primaryStyle")).capitalize().replace(" ", "")
	# if styleSheet in validStyles:
	# 	app.setStyleSheet(QStyleFactory.create(styleSheet))
	# else:
	# 	# import PyQt5.QtWidgets.QCommonStyle
	# 	print(styleSheet)
	# 	app.setStyleSheet(DarkS.loadDarkStyle())
	display.show()
	print("1")
	# display.dumpObjectInfo()
	# display.dumpObjectTree()
	sys.exit(app.exec_())
