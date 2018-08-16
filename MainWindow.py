from PyQt5.QtWidgets import (
	QApplication, QWidget,
	QMainWindow, QVBoxLayout, QTabWidget,
	QActionGroup, QStatusBar, QToolBar, QColorDialog, QMenu, QPushButton, QAction, QCheckBox, QStyleFactory
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QContextMenuEvent

from utilities.BooleanUtils import negate
from utilities.Common import *
from utilities.Qtilities import *

from TrayItem import trayItem
from settings.SettingsControl import settingsManager

enableTrivials = False

class mainToolWindow(QToolBar):
	# noinspection PyUnresolvedReferences
	def __init__(self, parent = None):
		super(mainToolWindow, self).__init__()
		self.setParent(parent)
		self.settings = parent.settings

		self.setWindowTitle("Main Toolbar")
		self.toolBarPosition = int(self.settings.value("MainToolbar/mainToolBarPosition"))

		self.popupMenu = QMenu()
		self.popupMenu.setToolTipsVisible(True)

		self.addAllActionsToObject(self.popupMenu)
		self.refreshChecks()

	# noinspection PyAttributeOutsideInit
	def declareActions(self):
		""" Just keep all the action declarations out of __init__ for cleanliness """
		self.isLockedInPosition = createAction2("Docked Mode", self, self.toggleDockingMode, isCheckable = True,
												statusTip = "Lock(/unlock(dock/undock) the toolbar")
		floatOptionTooltip = ("NOTE: Disabling does not automatically unfloat the toolbar.\n" +
							  "Moving the toolbar a little bit will unfloat it and return it to its docked position in the window.")
		self.canToolWindowFloat = createAction2("Floating Mode", self, self.toggleFloatingMode, isCheckable = True,
												statusTip = "Enable/disable floating the toolbar as a separate window",
												toolTip = floatOptionTooltip)

	# MAYBE: Move this function to Qtilities.py, as this is already quite generic as it is, and might be useful elsewhere
	def addAllActionsToObject(self, obj):
		""" Find all QActions whose parent is ``self`` and call ``obj.addAction()`` for each of them. """
		for member in vars(self).values():
			# print(type(member))
			if type(member) == QAction:
				# print("Found action " + str(member.__class__))
				obj.addAction(member)

	def refreshProperties(self):
		self.setFloatable(self.settings.value("MainToolbar/isMainToolBarFloatable"))
		self.setMovable(self.settings.value("MainToolbar/isMainToolBarMovable"))

	def refreshChecks(self):
		# self.isLockedInPosition should be checked when self.isMovable() == False, so that the it is checked when locked in place
		self.isLockedInPosition.setChecked(negate(self.isMovable()))
		# self.canToolWindowFloat should be checked when self.isFloatable() == True, so that it is checked when the toolbar can float
		self.canToolWindowFloat.setChecked(self.isFloatable())

	def contextMenuEvent(self, event):
		pos = None  # This is just to make the inspector shut up, and is probably even considered incorrect practice for Python
		if event.reason() == QContextMenuEvent.Mouse:
			pos = event.globalPos()
		# item = self.actionAt(event.pos())
		if pos is not None:
			self.popupMenu.popup(pos)

	# Todo: I can't quite put my finger on it, but I can see that this function could be refactored, specifically the first 3 lines.
	# noinspection PyArgumentList
	def toggleDockingMode(self):
		self.setMovable(negate(self.isMovable()))
		self.isLockedInPosition.setChecked(negate(self.isMovable()))
		self.settings.setValue("MainToolbar/isMainToolBarMovable", self.isMovable())
		self.refreshProperties()
		# QApplication.setStyle(QStyleFactory.create(text))
		self.setStyle(QStyleFactory.create(self.settings.value("Style_Options/primaryStyle")))

	def toggleFloatingMode(self):
		self.setFloatable(negate(self.isFloatable()))
		self.canToolWindowFloat.setChecked(self.isFloatable())
		self.settings.setValue("MainToolbar/isMainToolBarFloatable", self.isFloatable())
		self.refreshProperties()

	# noinspection PyUnresolvedReferences
	def toolBar_Icon(self, icon, func, tooltip, statustip = None):
		"""	'Template' function for a toolbar button with an icon	"""
		item = QAction(QIcon(icon), tooltip, self)  # TODO: consider replacing this with a call to createAction2

		if statustip is not None:
			item.setStatusTip(statustip)

		setTriggerResponse(item, func, "One or more icon type items on your toolbar")

		return item

	# noinspection PyUnresolvedReferences
	def toolBar_Text(self, text, func):
		"""	'Template' function for a text-only toolbar button	"""
		item = QAction(text, self)  # TODO: consider replacing this with a call to createAction

		setTriggerResponse(item, func, "One or more text type items on your toolbar")

		return item

	def setup(self):
		"""	Add toolbars and populate them with buttons	"""
		# Make buttons

		test = wrapper(print, "test")

		iconB = self.toolBar_Icon(
				"assets/Logo.png", test, "icon", "Do something"
		)
		textB = self.toolBar_Text("&Textual Button", test)

		# Add buttons to toolbars
		self.addAction(iconB)
		self.addAction(textB)

class window(QMainWindow):
	def __init__(self):  # noinspection PyArgumentList
		super(window, self).__init__()
		self.setObjectName("Mother Window")  # print("I am the "+ self.objectName())
		self.setAttribute(Qt.WA_QuitOnClose, True)  # TODO:Ensures that closing the main window also closes the preferences window

		'''System-wide clipboard'''
		# noinspection PyArgumentList
		self.clip = QApplication.clipboard()

		'''Configs'''
		self.settingsMan = settingsManager()
		# self.settingsMan.setParent(self)
		self.settingsMan.initSettings()
		self.settings = self.settingsMan.settingsFile

		if enableTrivials: ("Window flags: " + str(self.windowFlags()))  # WIP

		'''Sets the window style to the configured value'''
		style = str(self.settings.value("Style_Options/primaryStyle")).replace(" ", "")
		self.setStyleFromString(style)

		'''setup window aspects'''
		self.setWindowTitle("Switchboard")
		self.setWindowIcon(QIcon('assets/Logo.png'))
		self.declareGeneralActions()

		self.setStatusBar(QStatusBar(self))
		# self.XY = QLabel(
		# 		"Cursor:")  # TODO: Make this come with something to display the numerical position of the cursor; might involve the timerEvent of QStatusBar
		# # self.statusBar.addPermanentWidget(self.XY)
		# QStatusBar.addPermanentWidget(self.statusBar(), self.XY)

		self.clearClipboardButton = self.clickButton("Clear Clipboard", wrapper(self.clip.clear))  # Button which clears the system clipboard
		# if enableTrivials: print(self.clip.text())#print clipboard text

		self.topMenu()
		self.mainToolBar = mainToolWindow(self)
		self.mainToolBar.setup()
		'''Add toolbars to window. CRITICAL STEP'''
		self.addToolBar(self.mainToolBar.toolBarPosition, self.mainToolBar)

		self.pageBar = self.makePageBar()
		self.mainToolBar.addWidget(self.pageBar)
		if self.settings.value("cfgShouldCreateTrayIcon") == True:
			self.trayObject = trayItem(self, 'assets/Logo.png')
			# maybe move the addition of actions and setting of the context menu to here
			self.trayObject.show()

		if self.settings.value("mainWindowGeometry"):
			# 	# G = self.restoreGeometry(bytes(self.settings.value("mainWindowGeometry")))
			# 	# print(G)
			# 	a = QByteArray(self.saveGeometry())
			# 	print(a)
			# 	print("ZIL")
			# 	b = self.restoreGeometry(
			# 		b'\x04\xb0\x00\x00\x02\xd7\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x00\x00\x00\x00\x00\x00\x07\x80').to_bytes()
			# 	print(b)
			# # t = self.geo
			self.restoreGeometry(self.settings.value("mainWindowGeometry"))
		else:
			self.restoreGeometry(defaultWindowGeometry)

		if enableTrivials:
			("Window width:" + str(self.width()))
			print("Window height:" + str(self.height()))
			print("done init")

	# noinspection PyUnresolvedReferences,PyAttributeOutsideInit
	def declareGeneralActions(self):  # WIP
		"""Declare application wide Actions"""

		# Cut
		def Link(): wrapper(print, "Cut").call()

		self.actCut = createAction("Cu&t", self, Link, "Ctrl+X")

		# Copy
		def Link(): wrapper(print, "Copy").call()

		self.actCopy = createAction("&Copy", self, Link, "Ctrl+C")

		# Paste
		def Link(): wrapper(print, "Paste").call()

		self.actPaste = createAction("&Paste", self, Link, "Ctrl+v")

	def setStyleFromString(self, styleName: str):
		# noinspection PyArgumentList,PyCallByClass
		self.setStyle(QStyleFactory.create(styleName))

	def triggerButton(self, text = 'test', func = None, tip = None, X: int = None, Y: int = None):
		"""Simple (trigger-type response) button with optional parameters for position, label, and tooltip(none)"""
		btn = QPushButton(text, self)
		btn.adjustSize()
		btn.setToolTip(tip)

		if X is not None and Y is not None:
			btn.move(X, Y)

		setTriggerResponse(btn, func, "triggerButton with text " + repr(text))

		return btn

	def clickButton(self, text = 'test', func = None, tip = None, X: int = None, Y: int = None):
		"""Simple (click-type response) button with optional parameters for position, label, and tooltip(none)"""
		btn = QPushButton(text, self)
		btn.adjustSize()
		btn.setToolTip(tip)

		if X is not None and Y is not None:
			btn.move(X, Y)

		setClickedResponse(btn, func, "clickButton with text " + repr(text))

		return btn

	# FIXME
	# noinspection PyUnresolvedReferences
	def basicCheckBox(self, func = None, text = 'test', X: int = None, Y: int = None, isTri = False):
		"""Simple checkbox with some handling for tri-state boxes"""
		checkBox = QCheckBox(text, self)
		checkBox.adjustSize()

		if X is not None and Y is not None:
			checkBox.move(X, Y)

		if isTri == True:
			checkBox.setTristate(True)

		if isinstance(func, wrapper):
			def link():
				func.call()

			checkBox.stateChanged.connect(link)
		elif func is not None:
			checkBox.stateChanged.connect(func)
		else:
			print("basicCheckbox with text " + repr(text) + " has no function")

		return checkBox

	def menuItem(self, func, name, tip = None, shortcut = None, isToggle = False, group = None):
		"""	'Template' function for a simple menu item	"""
		item = QAction(name, self)  # self reminder: item is now a QAction
		item.setStatusTip(tip)

		if shortcut is not None:
			item.setShortcut(shortcut)  # ;else: print("no shortcut for menu item \""+name+"\"")
		if isToggle != False:
			item.setCheckable(True)
		if group is not None:
			group.addAction(item)

		errMsgHead = "Menu item " + repr(name)
		setTriggerResponse(item, func, errMsgHead)

		return item

	# MAYBE: REFACTOR
	def topMenu(self):
		"""Add menus and populate them with actions"""
		config = self.settings  # ; self.statusBar()
		mainMenu = self.menuBar()

		# Make menu items
		# prefs = self.menuItem(self.settingsMan.show, "Preferences", "View and edit application settings")
		# prefs.setMenuRole(QAction.PreferencesRole)

		styleGroup = QActionGroup(mainMenu)
		windows = wrapper(self.setStyleFromString, "Windows")
		winVista = wrapper(self.setStyleFromString, "Windowsvista")
		winXP = wrapper(self.setStyleFromString, "Windowsxp")
		fusion = wrapper(self.setStyleFromString, "Fusion")
		# TODO:only add a menu item if its name is in QStyleFactory.keys()
		style1 = self.menuItem(fusion, "Fusion", statusTips["fusion"], isToggle = True, group = styleGroup)
		style2 = self.menuItem(windows, "Windows", statusTips["windows"], isToggle = True, group = styleGroup)
		style3 = self.menuItem(winVista, "Windows Vista", statusTips["vista"], isToggle = True, group = styleGroup)
		style4 = self.menuItem(winXP, "Windows XP", statusTips["XP"], isToggle = True, group = styleGroup)

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
		fileMenu = mainMenu.addMenu("&File")
		editMenu = mainMenu.addMenu("&Edit")
		viewMenu = mainMenu.addMenu("&View")

		styleMenu = viewMenu.addMenu("&Styles")
		layoutMenu = viewMenu.addMenu("&Layout")

		# Add actions to menus
		# fileMenu.addAction(self.actQuit)
		# fileMenu.addAction(prefs)

		editMenu.addAction(self.actCopy)
		editMenu.addAction(self.actCut)
		editMenu.addAction(self.actPaste)

		viewMenu.addAction(colorPicker)

		tempMsg = "Something in layout menu"
		layoutMenu.addAction(self.menuItem(wrapper(print, tempMsg), None))  # TODO:give meaningful functions later

		styleMenu.addAction(style1)
		styleMenu.addAction(style2)
		styleMenu.addAction(style3)
		styleMenu.addAction(style4)

	# noinspection PyArgumentList
	def makePageBar(self):
		"""	Move all of the code for the contents of the pageBar out of the __init__ """
		pageBar = QTabWidget(self)
		tab1 = QWidget()

		pop = self.clickButton('test', wrapper(print, "clicked clickButton : pop"), None)
		box = self.basicCheckBox(wrapper(print, "toggled basicCheckbox : box"))

		tab1Layout = QVBoxLayout()
		tab1Layout.addStretch(1)
		tab1Layout.addWidget(pop)
		tab1Layout.addWidget(self.clearClipboardButton)
		tab1Layout.addWidget(box)

		tab1.setLayout(tab1Layout)

		pageBar.addTab(tab1, "tab1")

		return pageBar

	def closeEvent(self, *args, **kwargs):
		self.settings.setValue("mainWindowGeometry", self.saveGeometry())
		# print("Saving Geometry")
		# print(self.settings.value("mainWindowGeometry"))
		# print(self.saveGeometry())
		# self.settings.setValue("Style_Options/primaryStyle", self.style())
		if self.settings.value(
				"cfgShouldCreateTrayIcon") == True:  # should replace this with some sort of try block, because the trayObject might not be properly cleaned up if the setting is changed to false while the program is running
			self.trayObject.deleteLater()
		self.close()

if __name__ == "__main__":
	import sys

	app = QApplication(sys.argv)
	app.setApplicationName("My Switchboard")

	display = window()
	display.show()

	# Proof of concept for adding a method to ALL instances of a class defined by a python language binding. also works for those NOT defined by a binding.
	# Even adds the new method to the __dict__ entry for the target class! though if you want to check that it's available to an object that extends that class, you'd need to call dir(<OBJECT>) and look through the results; it'll be there!
	# def proof():
	# 	def getName(self):
	# 		print("getting object's class name..." + self.__class__.__name__)
	# 	QObject.getName=getName
	# proof()
	# display.settingsMan.getName()
	# display.clip.getName()
	# display.settings.getName()
	# display.clearClipboardButton.getName()
	# # print(QObject.__dict__)
	# print(dir(settingsManager))
	# print("\n\n\n\n\n\n\n\n")

	sys.exit(app.exec_())

# Quit			THIS IS A BAD SHORTCUT! DONT DO IT!
# self.actQuit = QAction("&Quit", self)
# self.actQuit.setShortcut("Ctrl+q")
# self.actQuit.setStatusTip("Close the application")
# self.actQuit.triggered.connect(self.closeEvent)
