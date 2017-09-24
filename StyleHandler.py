from PyQt5.QtWidgets import (
	QApplication, QStyle, QStyleFactory
)
from PyQt5.QtCore import (Qt, QDir)
from Common import *

enableNotifications = False
styleSheets = []

class StyleHandler(object):
	def __init__ (self, debug = False):
		# super(object, self).__init__()
		# self.parent = parent
		self.styleName = None
		self.addValidStyles()
		self.findAddedStyleSheets()
		global enableNotifications
		enableNotifications = debug
		if enableNotifications: self.listAll()

	'''
	Look for directories under ./assets/styles and, making the assumption that there will only be directories corresponding to
	custom styles, add an entry for each to the list of valid styles. The name of said entry will be the same as the directory
	name, with only the first letter capitalized, and with spaces removed.
	'''
	@staticmethod
	def addValidStyles ():
		styleDir = QDir("assets/styles")
		# noinspection PyArgumentList
		if len(styleDir.entryList(filters = QDir.Dirs | QDir.NoDotAndDotDot)) == 0:
			if enableNotifications: print("No new styles found.")
			return
		# noinspection PyArgumentList
		for style in styleDir.entryList(filters = QDir.Dirs | QDir.NoDotAndDotDot):
			if enableNotifications: print("Found new valid style: " + style)
			validStyles.append(str(style).capitalize().replace(" ", ""))

	'''
	Look for directories under ./assets/stylesheets and, making the assumption that there will only be directories corresponding to
	custom stylesheets add an entry for each to the list of custom stylesheets. The name of said entry will be the same as the
	directory name, normalized to lowercase, and with spaces removed. There may be special cases implemented for specific stylesheets.
	'''
	@staticmethod
	def findAddedStyleSheets ():
		sheetDir = QDir("assets/stylesheets")
		# noinspection PyArgumentList
		for sheet in sheetDir.entryList(filters = QDir.Dirs | QDir.NoDotAndDotDot):
			if enableNotifications: print("Found new stylesheet: " + sheet)
			'''Dark Style'''
			if (sheet == "dark") and ("qdarkstyle" not in styleSheets):
				styleSheets.append("qdarkstyle")
				if enableNotifications: print("\tAdding alternate name for \"" + sheet + "\": \"qdarkstyle\"")
			if (sheet == "qdarkstyle") and ("dark" not in styleSheets):
				styleSheets.append("dark")
				if enableNotifications: print("\tAdding alternate name for \"" + sheet + "\": \"dark\"")
			styleSheets.append(str(sheet).lower().replace(" ", ""))

	# TODO: try to find a way to programmatically detect and import styles and stylesheets
	'''Attempt to load/apply a stylesheet passed in as the variable 'text' '''
	# noinspection PyArgumentList
	@staticmethod
	def loadStyleSheet (text):
		if text == "qdarkstyle" or text == "dark":
			import assets.stylesheets.qdarkstyle as dark
			QApplication.instance().setStyleSheet(dark.loadQDarkStyle())
		elif text == "default" or text == "":
			QApplication.instance().setStyleSheet("")
		else:
			print("Cannot find a stylesheet by the name of \"" + text + "\"")

	'''Attempt to load/apply a style passed in as the variable 'text' '''
	def applyStyle (self, text):
		if text.capitalize().replace(" ", "") not in validStyles:
			print("Cannot apply style \"" + text + "\". No such style.")
		elif enableNotifications:
			print("Setting style to " + text)
		# noinspection PyArgumentList
		QApplication.instance().setStyle(QStyleFactory.create(text))
		if text is not None:
			self.styleName = text
		else:
			print("Cannot set style to None")

	'''Print the names of all known(accepted) stylesheets and styles'''
	# noinspection PyArgumentList
	@staticmethod
	def listAll ():
		print("\nAvailable stylesheet options: " + str(styleSheets) + " + default")
		print("Available styles: " + str(QStyleFactory.keys()) + "\n")
