from PyQt5.QtWidgets import (
	QTabWidget,  # QWidget, QTabBar,
	# QLayout, QHBoxLayout, QVBoxLayout, QGridLayout,
	# QDialog, QDialogButtonBox, QLabel,
	QPushButton  # , QMessageBox, QStatusBar, QLineEdit, QActionGroup, QCheckBox, QStyleFactory, QGroupBox, QComboBox
)

from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import (Qt, QObject, QSettings)

import warnings
from utilities.Common import *
from utilities import translations as tr
warnings.warn("Interpreting QTabWidgetExtras")

# Tweaks and extended functionality for QTabWidget
class extendedTabWidget(QTabWidget):
	def __init__ (self, parent = None):
		super(extendedTabWidget, self).__init__()
		if __name__ == "__main__":  # TEMPORARY
			from PyQt5.QtWidgets import QAction
			actQuit = QAction(tr.TR_ACT_QUIT, self)
			actQuit.setShortcut("Ctrl+q")
			#noinspection PyUnresolvedReferences
			actQuit.triggered.connect(sys.exit)
			self.addAction(actQuit)
		#NOTE: Consider adding optional parameters from which to set the following functions to the constructor
		# self.setTabPosition()			#options are North(above pages)(DEFAULT), South(below pages), East(right of pages), West(left of pages)
		# self.setTabShape()			#options are Rounded(DEFAULT), Triangular
		# self.setTabBarAutoHide()		#boolean, DEFAULT:False
		# self.setTabClosable()			#boolean, DEFAULT:????
		# self.setUsesScrollButtons()	#boolean, DEFAULT: Style dependant
		# self.setMovable()				#boolean, DEFAULT: False

	# Allow calling setIconSize using a more explicit function name
	def setMaxIconSize (self, maxSize):
		from PyQt5.QtCore import QSize
		self.setIconSize(QSize(maxSize, maxSize))

	# Explicitly enable tab with a call to setTabEnabled
	def enableTab (self, index):
		self.setTabEnabled(index, True)

	# Explicitly disable tab with a call to setTabEnabled
	def disableTab (self, index):
		self.setTabEnabled(index, False)

	# Return the widget at the given index position(If the index is out of range, return the widget at index position 0)
	def getWidgetAt (self, index):
		return self.widget(index)

	# Extended version of the addTab method. Also supports insertion, or adding a tab at a given position
	# Note: If tabLabel contains an ampersand(&), the character following the ampersand will become a shortcut to focus on this tab
	def addTabExtended (self, widget,
						tabLabel = "placeholder", tabIcon = None,
						toolTip = None, index = None,
						# whatsThis = None
						):
		# Insert (Add at position = index)
		if index is not None:
			if index > self.count() + 1:
				print("Index out of range; appending tab instead.\n")
			self.insertTab(index, widget, tabLabel)

		# Normal add
		else:
			self.addTab(widget, tabLabel)
			index = self.count()
		if tabIcon is not None:
			self.setTabIcon(index - 1, tabIcon)
		if toolTip is not None:
			self.setTabToolTip(index - 1, toolTip)
		# if whatsThis is not None:
		# 	self.setTabWhatsThis(index, whatsThis)

if __name__ == "__main__":
	import sys
	from PyQt5.QtWidgets import QApplication

	app = QApplication(sys.argv)
	app.setApplicationName("SettingsControl")


	# print(str(app.effectiveWinId()))

	# Because something isn't very smart, as A.B.connect(func) doesn't work correctly
	# when func tries to print a variable with a default value
	def dumbPrint (): testPrint()


	foo = extendedTabWidget()

	btn = QPushButton("Do Nothing", foo)
	# noinspection PyUnresolvedReferences
	btn.clicked.connect(dumbPrint)

	foo.addTabExtended(btn, "Test Button", QIcon("Logo.png"), toolTip = "placeholder")
	foo.show()

	sys.exit(app.exec_())
