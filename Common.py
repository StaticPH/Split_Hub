# from PyQt5.QtWidgets import QWidget
#
# extendedBools = [0, 1, "0", "1", "t", "T", "f", "F", "true", "True", "false", "False"]
# extendedTruths = [1, "1", "t", "T", "true", "True"]
# extendedFalsehoods = [0, "0", "f", "F", "false", "False"]
# statusTips = {
# 	"fusion": "Set window style to Fusion",
# 	"windows": "Set window style to Windows",
# 	"vista": "Set window style to Windows Vista",
# 	"XP": "Set window style to Windows XP"
# }
# validStyles = ["Windows", "Windowsxp", "Windowsvista", "Fusion"]  # TODO: check which styles actually exist on non win32 machines.
# defaultWindowGeometry = b'\x04\xb0\x00\x00\x02\xd7\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x00\x00\x00\x00\x00\x00\x07\x80'
#
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
#
# # Temp
# # import customLogging
# # customLogging.trivialLog("BLABLAHBALAHABKADNLSDL")
# class wrapper(object):
# 	def __init__ (self, func, *args):
# 		self.func = func
# 		self.args = args
#
# 	def call (self):
# 		return self.func(*self.args)
#
# # Converts extendedBools to standard bools. Returns -1 for values not in extendedBools
# def correctBoolean (var):
# 	if (var == True) or (var in extendedTruths) or (str(var).capitalize() in extendedTruths):
# 		# print(str(var) + " evaluated to: " + str(True))
# 		return True
# 	elif (var == False) or (var in extendedFalsehoods) or (str(var).capitalize() in extendedFalsehoods):
# 		# print(str(var) + " evaluated to: " + str(False))
# 		return False
# 	else:
# 		#In some cases, the value assigned to a setting for 'True' is actually an integer greater than 0, which isn't always 1.
# 		#try to convert var to an int and check that, but don't mind it if the conversion fails
# 		print(var)
# 		try:
# 			if int(var) > 0: return True
# 			elif int(var) == 0: return False
# 		except:
# 			pass
# 		# print(str(var) + " evaluated to: " + str(-1) +".\nValue should be corrected.")
# 		return -1
#
# def isTruth (var):
# 	if correctBoolean(var) == True:
# 		return True
# 	else:
# 		return False
#
# def isFalsehood (var):
# 	if correctBoolean(var) == False:
# 		return True
# 	else:
# 		return False
#
# def negate (boolean):
# 	return not boolean
#
# def testPrint (text = "Debug"):
# 	print(text)
