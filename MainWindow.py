from PyQt5.QtWidgets import (
	QApplication, QWidget,
	QMainWindow, QVBoxLayout, QTabWidget,
	QActionGroup, QStatusBar, QColorDialog, QStyleFactory
)
from PyQt5.QtCore import Qt

from functools import partial

from MainToolBar import mainToolBar
from utilities.Common import *
from utilities.builders import *
from utilities import translations as lang

from trayItem import trayItem
from settings.SettingsControl import settingsManager

enableTrivials = False

# TODO: Replace as many wrappers as possible with lambdas

# noinspection PyAttributeOutsideInit
class window(QMainWindow):
	def __init__(self):
		super(window, self).__init__()
		self.setObjectName('Mother Window')  # print('I am the '+ self.objectName())
		self.setAttribute(Qt.WA_QuitOnClose, True)  # TODO:Ensures that closing the main window also closes the preferences window
		self.declareGeneralActions()
		self.createPartials()

		'''System-wide clipboard'''
		self.clip = QApplication.clipboard()

		'''Configs'''
		self.settingsMan = settingsManager()
		# self.settingsMan.setParent(self)
		self.settingsMan.initSettings()
		self.settings = self.settingsMan.settingsFile

		if enableTrivials: ('Window flags: ' + str(self.windowFlags()))  # WIP

		self.setupUI()

		if self.settings.value('cfgShouldCreateTrayIcon') == True:
			self.trayObject = trayItem(self, 'assets/Logo.png')
			# maybe: Move the addition of actions and setting of the context menu to here?
			# maybe: By which I mean call something to do that from here, rather than in trayItem.__init__()
			self.trayObject.show()

		if enableTrivials:
			('Window width:' + str(self.width()))
			print('Window height:' + str(self.height()))
			print('done init')

	def setupUI(self):
		self.setWindowTitle(lang.TR_APPNAME)
		self.setWindowIcon(QIcon('assets/Logo.png'))

		'''Sets the window style to the configured value'''
		style = str(self.settings.value('Style_Options/primaryStyle')).replace(' ', '')
		self.setStyleFromString(style)

		self.setStatusBar(QStatusBar(self))
		# self.XY = QLabel(
		# 		'Cursor:')  # TODO: Make this come with something to display the numerical position of the cursor; might involve the timerEvent of QStatusBar
		# # self.statusBar.addPermanentWidget(self.XY)
		# QStatusBar.addPermanentWidget(self.statusBar(), self.XY)

		self.clearClipboardButton = self.clickButton(lang.TR_CLR_CLIP, wrapper(self.clip.clear))  # Button which clears the system clipboard
		# if enableTrivials: print(self.clip.text())#print clipboard text

		self.setupTopMenu()

		'''Create and add toolbar(s) to window'''
		self.mainToolBar = mainToolBar(self)
		# self.mainToolBar.setupUI()
		self.addToolBar(self.mainToolBar.toolBarPosition, self.mainToolBar)
		# TODO: store the position value before closing

		self.pageBar = self.makePageBar()
		self.mainToolBar.addWidget(self.pageBar)

		# Maybe: It might be good to move this if/else block to whatever will eventually be responsible for reloading/refreshing MainWindow's settings
		if self.settings.value('mainWindowGeometry'):
			# 	# G = self.restoreGeometry(bytes(self.settings.value("mainWindowGeometry")))
			# 	# print(G)
			# 	a = QByteArray(self.saveGeometry())
			# 	print(a)
			# 	print("ZIL")
			# 	b = self.restoreGeometry(
			# 		b'\x04\xb0\x00\x00\x02\xd7\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x00\x00\x00\x00\x00\x00\x07\x80').to_bytes()
			# 	print(b)
			# # t = self.geo
			self.restoreGeometry(self.settings.value('mainWindowGeometry'))
		else:
			self.restoreGeometry(defaultWindowGeometry)

	# noinspection PyUnresolvedReferences
	def declareGeneralActions(self):  # WIP
		"""Declare application wide Actions"""

		'''Cut'''
		# def Link(): wrapper(print, 'Cut').call()
		self.actCut = createAction(self, lang.TR_ACT_CUT, lambda: print('Cut'), 'Ctrl+X')

		'''Copy'''
		# def Link(): wrapper(print, 'Copy').call()
		self.actCopy = createAction(self, lang.TR_ACT_COPY, lambda: print('Copy'), 'Ctrl+C')

		'''Paste'''
		# def Link(): wrapper(print, 'Paste').call()
		self.actPaste = createAction(self, lang.TR_ACT_PASTE, lambda: print('Paste'), 'Ctrl+v')

	def createPartials(self):
		self.clickButton = partial(clickButton, self)
		self.triggerButton = partial(triggerButton, self)
		self.basicCheckBox = partial(basicCheckBox, self)
		self.menuItem = partial(menuItem, self)

	def setStyleFromString(self, styleName: str): self.setStyle(QStyleFactory.create(styleName))

	# MAYBE: REFACTOR
	def setupTopMenu(self):
		"""Add menus and populate them with actions"""
		config = self.settings  # ; self.statusBar()
		mainMenu = self.menuBar()

		# Make menu items
		# prefs = self.menuItem(self.settingsMan.show, 'Preferences', 'View and edit application settings')
		# prefs.setMenuRole(QAction.PreferencesRole)
		styleGroup = QActionGroup(mainMenu)
		windows = wrapper(self.setStyleFromString, 'Windows')
		winVista = wrapper(self.setStyleFromString, 'Windowsvista')
		winXP = wrapper(self.setStyleFromString, 'Windowsxp')
		fusion = wrapper(self.setStyleFromString, 'Fusion')
		# TODO:only add a menu item if its name is in QStyleFactory.keys()
		style1 = self.menuItem(
				fusion, lang.TR_STYLEMENU_FUSION, lang.TR_STYLEMENU_FUSION_TOOLTIP,
				isToggle = True, group = styleGroup
		)
		style2 = self.menuItem(
				windows, lang.TR_STYLEMENU_WINDOWS, lang.TR_STYLEMENU_WINDOWS_TOOLTIP,
				isToggle = True, group = styleGroup
		)
		style3 = self.menuItem(
				winVista, lang.TR_STYLEMENU_VISTA, lang.TR_STYLEMENU_VISTA_TOOLTIP,
				isToggle = True, group = styleGroup
		)
		style4 = self.menuItem(
				winXP, lang.TR_STYLEMENU_XP, lang.TR_STYLEMENU_XP_TOOLTIP,
				isToggle = True, group = styleGroup
		)

		# Makes sure that the configured style appears as checked on load
		for style in styleGroup.actions():
			# print('style: '+str(style.text()).capitalize().replace(' ', '') + '	setting: '+config.value('Style_Options/primaryStyle'))
			if (str(style.text()).capitalize().replace(' ', '')) == config.value('Style_Options/primaryStyle').capitalize().replace(' ', ''):
				style.setChecked(True)
		if sys.platform.startswith('win32'):
			style3.setText(
					style3.text() + ' (' + lang.TR_DEFAULT + ')')  # On Windows operating systems, mark 'Windows Vista' as the default style
		else:
			style1.setText(style1.text() + ' (' + lang.TR_DEFAULT + ')')  # On non-Windows operating systems, mark 'Fusion' as the default style

		# TODO: Reset layout of window to default?
		# resetPlacement = self.menuItem(None, 'Reset Window Layout', 'Reset the window layout to default')
		colorPicker = self.menuItem(QColorDialog.getColor, lang.TR_COLR_PKR)

		# Make menus
		fileMenu = mainMenu.addMenu(lang.TR_MAINMENU_FILE)
		editMenu = mainMenu.addMenu(lang.TR_MAINMENU_EDIT)
		viewMenu = mainMenu.addMenu(lang.TR_MAINMENU_VIEW)

		styleMenu = viewMenu.addMenu(lang.TR_VIEWMENU_STYLES)
		layoutMenu = viewMenu.addMenu(lang.TR_VIEWMENU_LAYOUT)

		# Add actions to menus
		# fileMenu.addAction(self.actQuit)
		# fileMenu.addAction(prefs)

		editMenu.addAction(self.actCopy)
		editMenu.addAction(self.actCut)
		editMenu.addAction(self.actPaste)

		viewMenu.addAction(colorPicker)

		layoutMenu.addAction(self.menuItem(lambda: print('Something in layout menu'), None))  # TODO:give meaningful functions later

		styleMenu.addAction(style1)
		styleMenu.addAction(style2)
		styleMenu.addAction(style3)
		styleMenu.addAction(style4)

	# TODO: move to MainToolBar.py
	# noinspection PyArgumentList
	def makePageBar(self):
		"""	Move all of the code for the contents of the pageBar out of the __init__ """
		pageBar = QTabWidget(self)
		tab1 = QWidget()

		pop = self.clickButton('test', wrapper(print, 'clicked clickButton : pop'), None)
		box = self.basicCheckBox(wrapper(print, 'toggled basicCheckbox : box'))

		tab1Layout = QVBoxLayout()
		tab1Layout.addStretch(1)
		tab1Layout.addWidget(pop)
		tab1Layout.addWidget(self.clearClipboardButton)
		tab1Layout.addWidget(box)

		tab1.setLayout(tab1Layout)

		pageBar.addTab(tab1, 'tab1')

		return pageBar

	def closeEvent(self, *args, **kwargs):
		self.settings.setValue('mainWindowGeometry', self.saveGeometry())
		# print('Saving Geometry')
		# print(self.settings.value('mainWindowGeometry'))
		# print(self.saveGeometry())
		# self.settings.setValue('Style_Options/primaryStyle', self.style())
		if self.settings.value('cfgShouldCreateTrayIcon') == True:
			# should replace this with some sort of try block, because the trayObject might not be properly cleaned up if the setting is changed to false while the program is running
			self.trayObject.deleteLater()
		self.close()

if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)
	app.setApplicationName(lang.TR_APPNAME)

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
	# print('\n\n\n\n\n\n\n\n')

	sys.exit(app.exec_())

# Quit			THIS IS A BAD SHORTCUT! DONT DO IT!
# self.actQuit = QAction('&Quit', self)
# self.actQuit.setShortcut('Ctrl+q')
# self.actQuit.setStatusTip('Close the application')
# self.actQuit.triggered.connect(self.closeEvent)