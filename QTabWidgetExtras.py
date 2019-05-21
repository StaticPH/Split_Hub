from PyQt5.QtWidgets import (
	QTabWidget,  # QWidget, QTabBar,
	# QLayout, QHBoxLayout, QVBoxLayout, QGridLayout, QDialog
	# QStatusBar QActionGroup, QCheckBox, QStyleFactory
	QWidget
)

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (
	QSize  # , Qt, QObject, QSettings
)

import warnings
from utilities import translations as tr

warnings.warn('Interpreting QTabWidgetExtras')

class extendedTabWidget(QTabWidget):
	"""Tweaks and extended functionality for QTabWidget"""

	def __init__(self, parent = None):
		super(extendedTabWidget, self).__init__()


	# NOTE: Consider adding optional parameters from which to set the following functions to the constructor
	# self.setTabPosition()			#options are North(above pages)(DEFAULT), South(below pages), East(right of pages), West(left of pages)
	# self.setTabShape()			#options are Rounded(DEFAULT), Triangular
	# self.setTabBarAutoHide()		#boolean, DEFAULT:False
	# self.setTabClosable()			#boolean, DEFAULT:????
	# self.setUsesScrollButtons()	#boolean, DEFAULT: Style dependant
	# self.setMovable()				#boolean, DEFAULT: False

	@PendingDeprecationWarning
	def setMaxIconSize(self, maxSize: int):
		"""Allow calling setIconSize using a more explicit function name"""
		self.setIconSize(QSize(maxSize, maxSize))

	def enableTab(self, index: int):
		"""Explicitly enable tab with a call to setTabEnabled"""
		self.setTabEnabled(index, True)

	def disableTab(self, index: int):
		"""Explicitly disable tab with a call to setTabEnabled"""
		self.setTabEnabled(index, False)

	def getWidgetAt(self, index: int):
		"""
		Return the widget at the given index position.
		If the index is out of range, return the widget at index position 0.
		"""
		return self.widget(index)

	def addTabExtended(self, widget: QWidget, tabLabel: str = tr.TR_PLACEHOLDER,
					   tabIcon: QIcon = QIcon(None), toolTip: str = None,
					   index: int = None  # , whatsThis = None
					   ) -> None:
		"""
		Extended version of the addTab method. Also supports insertion, or adding a tab at a given position
		Note: If tabLabel contains an ampersand(&), the character following the ampersand will become a shortcut to focus on this tab.
		"""
		# Insert (Add at position = index)
		if index is not None:
			if index > self.count() + 1:
				print('Index out of range; appending tab instead.\n')	#NOTE: I honestly cant remember if this actually did anything differently or not, but it doesn't look like it does currently
			self.insertTab(index, widget, tabLabel)

		# Normal add
		else:
			self.addTab(widget, tabLabel)
			index = self.count()
		if tabIcon is not None:
			self.setTabIcon(index - 1, tabIcon)
		# if whatsThis is not None:
		# 	self.setTabWhatsThis(index, whatsThis)
		if toolTip is not None:
			self.setTabToolTip(index - 1, toolTip)

if __name__ == '__main__':
	import sys
	from PyQt5.QtWidgets import QApplication, QPushButton, QAction

	app = QApplication(sys.argv)
	app.setApplicationName('QTabWidgetExtras')

	# print(str(app.effectiveWinId()))

	foo = extendedTabWidget()

	actQuit = QAction(tr.TR_ACT_QUIT)
	actQuit.setShortcut('Ctrl+q')
	actQuit.triggered.connect(sys.exit)
	foo.addAction(actQuit)

	btn = QPushButton('Do Nothing', foo)
	btn.clicked.connect(lambda: print('test button for QTabWidgetExtras'))

	foo.addTabExtended(btn, 'Test Button', QIcon('Logo.png'), toolTip = 'placeholder')

	foo.show()

	sys.exit(app.exec_())