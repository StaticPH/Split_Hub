from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget

extendedBools = [0, 1, "0", "1", "t", "T", "f", "F", "true", "True", "false", "False", "y", "Y", "n", "N", "yes", "Yes", "no", "No"]
extendedTruths = [1, "1", "t", "T", "true", "True", "y", "Y", "yes", "Yes"]
extendedFalsehoods = [0, "0", "f", "F", "false", "False", "n", "N", "no", "No"]
statusTips = {
	"fusion": "Set window style to Fusion",
	"windows": "Set window style to Windows",
	"vista": "Set window style to Windows Vista",
	"XP": "Set window style to Windows XP"
}
validStyles = ["Windows", "Windowsxp", "Windowsvista", "Fusion"]  # TODO: check which styles actually exist on non win32 machines.
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
# customLogging.trivialLog("BLABLAHBALAHABKADNLSDL")
class wrapper(object):
	def __init__(self, func, *args):
		self.func = func
		self.args = args

	def call(self):
		return self.func(*self.args)

# Converts extendedBools to standard bools. Returns -1 for values not in extendedBools
# def correctBoolean (var):
# 	if (var == True) or (var in extendedTruths) or (str(var).capitalize() in extendedTruths):
# 		# print(str(var) + " evaluated to: " + str(True))
# 		return True
# 	elif (var == False) or (var in extendedFalsehoods) or (str(var).capitalize() in extendedFalsehoods):
# 		# print(str(var) + " evaluated to: " + str(False))
# 		return False
# 	else:
# 		#In some cases, the value assigned to a setting for 'True' is actually an integer greater than 1.
# 		#try to convert var to an int and check that, but don't mind it if the conversion fails
# 		print(var)
# 		try:
# 			if int(var) > 0: return True
# 			elif int(var) == 0: return False
# 		except:
# 			pass
# 		# print(str(var) + " evaluated to: " + str(-1) +".\nValue should be corrected.")
# 		return -1

def correctBoolean(choice: str):
	choice = str(choice)  # In case a boolean mistakenly gets passed in
	if choice.lower() in ('true', 't', 'yes', 'y', '1'):
		return True
	elif choice.lower() in ('false', 'f', 'no', 'n', '0'):
		return False
	else:
		# In some cases, the value assigned to a setting for 'True' is actually an integer greater than 1.
		# try to convert var to an int and check that, but don't mind it if the conversion fails
		# print(var)
		try:
			if int(choice) > 0:
				return True
			elif int(choice) == 0:
				return False
		except:
			pass
		# raise TypeError('String `' + choice + "` cannot be equated to a boolean value.")
		return -1

def negate(boolean):
	return not boolean

def isTruth(var):
	return correctBoolean(var)

def isFalsehood(var):
	return negate(correctBoolean(var))

def testPrint(text = "Debug"):
	print(text)

def setTriggerResponse(obj: QObject, func, errMsgHead: str = None):
	if isinstance(func, wrapper):
		def link():
			func.call()

		obj.triggered.connect(link)
	elif func is not None:
		# print(func.__name__ + " is not a wrapper. It is a " + type(func).__name__)
		obj.triggered.connect(func)
	else:
		if errMsgHead is None:
			print("A functionless object has been triggered.")
		else:
			print(errMsgHead + " has no function")

def setClickedResponse(obj: QObject, func, errMsgHead: str = None):
	if isinstance(func, wrapper):
		def link():
			func.call()

		obj.clicked.connect(link)
	elif func is not None:
		# print(func.__name__ + " is not a wrapper. It is a " + type(func).__name__)
		obj.clicked.connect(func)
	else:
		if errMsgHead is None:
			print("A functionless object has been triggered.")
		else:
			print(errMsgHead + " has no function")
