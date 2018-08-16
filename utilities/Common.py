statusTips = {  # TODO: Move this to something that does localization
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

def testPrint(text = "Debug"):
	print(text)

def isInt(number):
	try:
		return number % 1 == 0
	except TypeError:
		try:
			return int(number) % 1 == 0
		except (TypeError, ValueError):
			return False

def isFloat(number):
	try:
		return number % 1 == 1
	except TypeError:
		try:
			return float(number) % 1 == 1
		except (TypeError, ValueError):
			return False
