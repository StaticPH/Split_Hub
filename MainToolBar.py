from PyQt5.QtGui import QContextMenuEvent, QIcon
from PyQt5.QtWidgets import QToolBar, QMenu, QAction, QStyleFactory

from utilities.booleanUtils import negate
from utilities.Common import wrapper
from utilities.Qtilities import createAction2, setTriggerResponse
from utilities import translations as tr

class mainToolBar(QToolBar):
	# noinspection PyUnresolvedReferences
	def __init__(self, parent = None):
		super(mainToolBar, self).__init__()
		self.setParent(parent)
		self.settings = parent.settings

		self.setWindowTitle("Main Toolbar")
		self.toolBarPosition = int(self.settings.value("MainToolbar/mainToolBarPosition"))

		self.popupMenu = QMenu()
		self.popupMenu.setToolTipsVisible(True)

		self.declareActions()
		self.addAllActionsToObject(self.popupMenu)
		self.refreshChecks()

	# noinspection PyAttributeOutsideInit
	def declareActions(self):

		""" Just keep all the action declarations out of __init__ for cleanliness """
		self.isLockedInPosition = createAction2(tr.TR_TOOLBAR_DOCKMODE, self, self.toggleDockingMode, isCheckable = True,
												statusTip = tr.TR_TOOLBAR_DOCKMODE_STIP)
		self.canToolWindowFloat = createAction2(tr.TR_TOOLBAR_FLOATMODE, self, self.toggleFloatingMode, isCheckable = True,
												statusTip = tr.TR_TOOLBAR_FLOATMODE_STIP,
												toolTip = tr.TR_TOOLBAR_FLOATMODE_TTIP)

	# MAYBE: Move this function to Qtilities.py, as this is already quite generic as it is, and might be useful elsewhere
	def addAllActionsToObject(self, obj):
		""" Find all QActions whose parent is ``self`` and call ``obj.addAction()`` for each of them. """
		for member in vars(self).values():
			if type(member) == QAction:
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
