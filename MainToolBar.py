from functools import partial

from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtWidgets import QToolBar, QMenu, QStyleFactory

from utilities.QtHelpers import addAllActionsToObject
from utilities.booleanUtils import negate
from utilities.builders import createAction2, toolBar_Text, toolBar_Icon
from utilities import translations as tr

# noinspection PyAttributeOutsideInit
class mainToolBar(QToolBar):
	def __init__(self, parent = None):
		super(mainToolBar, self).__init__()
		self.setParent(parent)
		self.settings = parent.settings

		self.setWindowTitle('Main Toolbar')
		self.toolBarPosition = int(self.settings.value('MainToolbar/mainToolBarPosition'))

		self.popupMenu = QMenu()
		self.popupMenu.setToolTipsVisible(True)

		self.createPartials()
		self.declareActions()
		self.addAllActionsToObject(self.popupMenu)
		self.refreshChecks()
		self.setupUI()

	def createPartials(self):
		self.toolBar_Icon = partial(toolBar_Icon, self)
		self.toolBar_Text = partial(toolBar_Text, self)
		self.createAction2 = partial(createAction2, self)
		self.addAllActionsToObject = partial(addAllActionsToObject, self)

	def declareActions(self):
		""" Just keep all the action declarations out of __init__ for cleanliness """
		self.isLockedInPosition = self.createAction2(tr.TR_TOOLBAR_DOCKMODE, self.toggleDockingMode,
													 isCheckable = True,
													 statusTip = tr.TR_TOOLBAR_DOCKMODE_STIP)
		self.canToolWindowFloat = self.createAction2(tr.TR_TOOLBAR_FLOATMODE, self.toggleFloatingMode,
													 isCheckable = True,
													 statusTip = tr.TR_TOOLBAR_FLOATMODE_STIP,
													 toolTip = tr.TR_TOOLBAR_FLOATMODE_TTIP)

	def refreshProperties(self):
		self.setFloatable(self.settings.value('MainToolbar/isMainToolBarFloatable'))
		self.setMovable(self.settings.value('MainToolbar/isMainToolBarMovable'))

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

	# TODO: I can't quite put my finger on it, but my gut tells me that this function could be refactored, specifically the first 3 lines.
	def toggleDockingMode(self):
		self.setMovable(negate(self.isMovable()))
		self.isLockedInPosition.setChecked(negate(self.isMovable()))
		self.settings.setValue('MainToolbar/isMainToolBarMovable', self.isMovable())
		self.refreshProperties()
		# QApplication.setStyle(QStyleFactory.create(text))
		self.setStyle(QStyleFactory.create(self.settings.value('Style_Options/primaryStyle')))

	def toggleFloatingMode(self):
		self.setFloatable(negate(self.isFloatable()))
		self.canToolWindowFloat.setChecked(self.isFloatable())
		self.settings.setValue('MainToolbar/isMainToolBarFloatable', self.isFloatable())
		self.refreshProperties()

	def setupUI(self):
		"""	Add toolbars and populate them with buttons	"""
		# Make buttons

		iconB = self.toolBar_Icon(
				'assets/Logo.png', lambda: print('iconB'), 'icon', 'Do something'
		)
		textB = self.toolBar_Text('&Textual Button', lambda: print('textB'))

		# Add buttons to toolbars
		self.addAction(iconB)
		self.addAction(textB)