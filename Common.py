extendedBools = [0, 1, "0", "1", "t", "T", "f", "F", "true", "True", "false", "False"]
extendedTruths = [1, "1", "t", "T", "true", "True"]
extendedFalsehoods = [0, "0", "f", "F", "false", "False"]
statusTips = {
	"fusion": "Set window style to Fusion",
	"windows": "Set window style to Windows",
	"vista": "Set window style to Windows Vista",
	"XP": "Set window style to Windows XP"
}
validStyles = ["Windows", "Windowsxp", "Windowsvista", "Fusion"]  # Need to check which styles actually exist on non win32 machines.
defaultWindowGeometry = b'\x01\xd9\xd0\xcb\x00\x02\x00\x00\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x00\x00\x00\x00\x00\x00\x07\x80'


# import customLogging
# customLogging.trivialLog("BLABLAHBALAHABKADNLSDL")
class wrapper(object):
	def __init__ (self, func, *args):
		self.func = func
		self.args = args

	def call (self):
		return self.func(*self.args)


# Convert extendedBools to standard bools. Returns -1 for values not in extendedBools
def correctBoolean (var):
	if (var == True) or (var in extendedTruths) or (str(var).capitalize() in extendedTruths):
		# print(str(var) + " evaluated to: " + str(True))
		return True
	elif (var == False) or (var in extendedFalsehoods) or (str(var).capitalize() in extendedFalsehoods):
		# print(str(var) + " evaluated to: " + str(False))
		return False
	else:
		# print(str(var) + " evaluated to: " + str(-1) +".\nValue should be corrected.")
		return -1


def isTruth (var):
	if correctBoolean(var) == True:
		return True
	else:
		return False


def isFalsehood (var):
	if correctBoolean(var) == False:
		return True
	else:
		return False


def negate (boolean):
	return not boolean

def testPrint (text = "Debug"):
	print(text)
