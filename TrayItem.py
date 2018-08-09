from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction

class trayItem(QSystemTrayIcon):
	# maybe:Add an action to the context menu that will disable(and hide) the tray icon
	# maybe:It would need a tooltip mentioning that it would need to be re-enabled via the config or the menu
	# considering the addition of other context menu items
	def __init__(self, parent, icon = None):
		super(trayItem, self).__init__()
		self.setParent(parent)
		print("trayItem's parent is : " + str(self.parent.__name__) + "\t" + str(self.parent()))
		self.setIcon(QIcon(icon))
		self.setToolTip("Switchboard")
		context = self.rightClickResponse()
		self.setContextMenu(context)
		self.activated.connect(self.clickRestraint)

	# Be sure that right clicking properly brings up the context menu, rather than triggering the same response as a left click
	def clickRestraint(self, clickType):
		if clickType == self.Trigger:
			self.leftClickResponse()

	def leftClickResponse(self):
		parent = self.parent()
		if parent.isMinimized():
			parent.activateWindow()
			parent.showNormal()
		else:
			parent.showMinimized()
			# print("Should be minimized? " + str(parent.isMinimized()))
			pass  # annoyance where things dont want to collapse

	def rightClickResponse(self):
		parent = self.parent()
		menu = QMenu(parent)

		quitAction = QAction("&Quit", self)
		quitAction.triggered.connect(parent.closeEvent)
		menu.addAction(quitAction)

		clearClip = QAction("Clear Clipboard", self)
		clearClip.triggered.connect(parent.clip.clear)
		menu.addAction(clearClip)

		# colorPicker = QAction("Color Picker", self)
		# colorPicker.triggered.connect(QColorDialog.getColor)
		# menu.addAction(colorPicker)
		return menu
