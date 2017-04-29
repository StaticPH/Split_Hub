extendedBools=[0,1,"t","T","f","F","true","True","false","False"]
extendedTruths=[1, "t", "T", "true", "True"]
extendedFalsehoods=[0, "f", "F", "false", "False"]
statusTips={
    "fusion":"Set window style to Fusion",
    "windows":"Set window style to Windows",
    "vista":"Set window style to Windows Vista",
    "XP":"Set window style to Windows XP"
    }
validStyles=["Windows", "Windowsxp", "Windowsvista", "Fusion"]
defaultWindowGeometry=b'\x01\xd9\xd0\xcb\x00\x02\x00\x00\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x02\xbd\x00\x00\x00\xe4\x00\x00\x04\xb0\x00\x00\x02\xd7\x00\x00\x00\x00\x00\x00\x00\x00\x07\x80'
class wrapper(object):
	def __init__ (self, func, *args):	self.func = func;		self.args = args
	def call (self): return self.func(*self.args)
def testPrint (text = "Debug"): print(text)
