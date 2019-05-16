import sys
from functools import partial

from PyQt5.QtWidgets import QMenuBar, QActionGroup, QColorDialog, QStyleFactory

from utilities import translations as tr
from utilities.Common import wrapper
from utilities.QtHelpers import setAppStyleFromString
from utilities.builders import menuItem, basicCheckBox, triggerButton, clickButton, createAction

class mainMenu(QMenuBar):
	def __init__(self, parent = None):
		super(mainMenu, self).__init__()
		# Whether or not to set parent should also depend on whether or not all windows should share a single menu bar on Macs
		# If they should, then don't set the parent, and just share the menu between individual windows.
		self.setParent(parent if parent is not None else None)  # This SHOULD be the same as just blindly setting it, but I need to confirm
		self.createPartials()
		self.declareGeneralActions()

		# Make menus
		self.fileMenu = self.addMenu(tr.TR_MAINMENU_FILE)
		self.editMenu = self.addMenu(tr.TR_MAINMENU_EDIT)
		self.viewMenu = self.addMenu(tr.TR_MAINMENU_VIEW)

		self.styleMenu = self.viewMenu.addMenu(tr.TR_VIEWMENU_STYLES)
		self.layoutMenu = self.viewMenu.addMenu(tr.TR_VIEWMENU_LAYOUT)

		# Make any groups that need to be externally accessible
		self.styleGroup = QActionGroup(self)

		# Fully populate the main menu
		self.populateMenus()

	# noinspection PyAttributeOutsideInit
	def createPartials(self):
		self.clickButton = partial(clickButton, self)
		self.triggerButton = partial(triggerButton, self)
		self.basicCheckBox = partial(basicCheckBox, self)

	# self.menuItem = partial(menuItem, self)

	# noinspection PyAttributeOutsideInit
	def declareGeneralActions(self):  # WIP
		"""Declare application wide Actions"""

		'''Cut'''
		# def Link(): wrapper(print, 'Cut').call()
		self.actCut = createAction(self, tr.TR_ACT_CUT, lambda: print('Cut'), 'Ctrl+X')

		'''Copy'''
		# def Link(): wrapper(print, 'Copy').call()
		self.actCopy = createAction(self, tr.TR_ACT_COPY, lambda: print('Copy'), 'Ctrl+C')

		'''Paste'''
		# def Link(): wrapper(print, 'Paste').call()
		self.actPaste = createAction(self, tr.TR_ACT_PASTE, lambda: print('Paste'), 'Ctrl+v')

	def populateFileMenu(self):
		# prefs = menuItem(self, self.settingsMan.show, tr.TR_FILEMENU_PREFS, tr.TR_FILEMENU_PREFS_STIP)
		# prefs.setMenuRole(QAction.PreferencesRole)

		# fileMenu.addAction(self.actQuit)
		# fileMenu.addAction(prefs)
		pass

	def populateEditMenu(self):
		self.editMenu.addAction(self.actCopy)
		self.editMenu.addAction(self.actCut)
		self.editMenu.addAction(self.actPaste)

	def populateViewMenu(self):
		colorPicker = menuItem(self, QColorDialog.getColor, tr.TR_COLR_PKR)
		self.viewMenu.addAction(colorPicker)

	def populateStyleMenu(self):
		names = sorted(QStyleFactory.keys())  # As I understand things, any custom styles will need to be loaded before this point
		upperNames = [n.upper() for n in names]
		menuEntries = iter(sorted(filter(
				lambda x: str.endswith(x, tuple(upperNames)),
				dir(tr)
		)))

		for name in names:
			try:
				nameEntry = next(menuEntries)
				trName = eval('tr.' + nameEntry)
				trStatusTip = eval('tr.' + nameEntry + tr.TR_STATUSTIP_SUFFIX)
				style = menuItem(
						# self, lambda: setAppStyleFromString(name),	# For some reason, this always uses the last name in names. Weird
						self, wrapper(setAppStyleFromString, name),
						trName, trStatusTip,
						None, True, self.styleGroup)

				if not sys.platform.startswith('win32') and name.upper() == 'FUSION':
					# Mark 'Fusion' as the default style on non-Windows operating systems
					style.setText(style.text() + ' (' + tr.TR_DEFAULT + ')')
				elif sys.platform.startswith('win32'):
					# On Windows operating systems, mark 'Windows Vista' as the default style if found, otherwise, go with 'Fusion'
					if name.upper() == 'WINDOWSVISTA' or (name.upper() == 'FUSION' and 'WINDOWSVISTA' not in upperNames):
						style.setText(style.text() + ' (' + tr.TR_DEFAULT + ')')

				self.styleMenu.addAction(style)
			except StopIteration:
				break

	def populateLayoutMenu(self):
		# TODO: Reset layout of window to default?
		# TODO:give meaningful functions later
		# resetPlacement = menuItem(self,None, 'Reset Window Layout', 'Reset the window layout to default')
		self.layoutMenu.addAction(menuItem(self, lambda: print('Something in layout menu'), str(None)))

	def populateMenus(self):
		self.populateFileMenu()
		self.populateEditMenu()
		self.populateViewMenu()
		self.populateStyleMenu()
		self.populateLayoutMenu()

if __name__ == '__main__':
	from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
	from utilities.QtHelpers import stdMainSetup

	app = QApplication(sys.argv)

	btn = QPushButton('button')
	btn.setToolTip('tooltip')

	lay = QVBoxLayout()
	lay.addWidget(mainMenu())
	lay.addWidget(btn)

	win = stdMainSetup('MainMenu', QWidget())
	win.setLayout(lay)
	win.show()

	sys.exit(app.exec_())