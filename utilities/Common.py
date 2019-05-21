import sys
from typing import Any

funcType = type(lambda: None)

# validStyles = ['Windows', 'Windowsxp', 'Windowsvista', 'Fusion']  # TODO: check which styles actually exist on non win32 machines.
defaultWindowGeometry = b'\x04\xb0\x00\x00\x02\xd7\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x00\x00\x00\x00\x00\x00\x07\x80'

# settingsList = []
#
# # noinspection PyRedeclaration, PyArgumentList
# class settingEntry(QWidget):
# 	# CURRENTLY ONLY WORKS WITH WIDGET BASED SETTINGS		FIXME
# 	def __init__ (self, widget, cfgName):
# 		super(settingEntry, self).__init__()
# 		'''	The widget corresponding to the setting	'''
# 		self.widget = widget
# 		'''	The "key associated with the setting	'''
# 		self.cfgName = cfgName
# 		'''	Add this settingEntry to the list	'''
# 		# print(cfgName)
# 		settingsList.append(self)

# Temp
# import customLogging
# customLogging.trivialLog('Testing 1,2,3')
class wrapper(object):
	def __init__(self, func, *args):
		self.func = func
		self.args = args

	def call(self):
		return self.func(*self.args)

def isInt(number: Any) -> bool:
	"""
	Check if a number is an integer.
	Returns ``True`` for whole number floats and strings convertible to integers,
	but returns ``False`` for strings containing whole number floats\\\n
	``Examples:``
		``isInt(5) -> True``\\\n
		``isInt('5') -> True``\\\n
		``isInt(5.0) -> True``\\\n
		``isInt(5.1) -> False``\\\n
		``isInt('5.0') -> False``\\\n
		``isInt('5.1') -> False``
	"""
	try:
		return number % 1 == 0
	except TypeError:
		try:
			return int(number) % 1 == 0
		except (TypeError, ValueError):
			return False

def isFloat(number: Any) -> bool:
	""" Check if a number is a float. Returns false for strings containing floats. """
	return type(number) == float

def export(func):
	""" A decorator for adding functions and classes to __all__, thus allowing them to be imported by `from module import *` """
	module = sys.modules[func.__module__]
	if hasattr(module, '__all__'):
		module.__all__.append(func.__name__)
	else:
		module.__all__ = [func.__name__]
	return func

#TODO: look into programmatically excluding imported objects
#Unfortunately, static linters dont always seem to respect this
def gen__All__(localScope, exclude: list = None):
	"""
	Create and return a list for use as __all__ for a module.
	localScope should be a call to the locals() builtin, or a variable of some iterable type containing members of the local scope.
	__all__, gen__All__, and the contents of `exclude` will be left out
	"""
	if exclude is None:
		exclude = []
	if 'gen__All__' not in exclude:
		exclude.append('gen__All__')

	_all = filter(
			lambda x: (not x.startswith('__')) and (x not in exclude),
			localScope
	)

	# If debugging with pydev debugger, ignore the related symbols
	_all = filter(lambda x: not x.startswith('_pydev'), _all)
	return list(_all)

#####################################################################################################
# import platform
# from os import path
#
# class osHelpers:
# 	def isWindows(self) -> bool:
# 		"""Returns True if platform is determined to be Windows, otherwise False"""
# 		return platform.system() == 'Windows'
#
# 	def isMac(self) -> bool:
# 		"""Returns True if platform is determined to be Darwin, otherwise False"""
# 		try:
# 			return platform.system() == 'Darwin'
# 		except Exception:
# 			return path.exists('/System/Library/CoreServices/Finder.app')
#
# 	def isLinux(self) -> bool:
# 		"""Returns True if platform is determined to be Linux, otherwise False"""
# 		return platform.system() == 'Linux'
#####################################################################################################
# import inspect
# def getCallerName() -> str:
# 	"""Returns the name of the calling method as a string."""
# 	return inspect.stack()[1][3]