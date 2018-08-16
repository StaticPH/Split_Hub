from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from utilities.Common import wrapper

# TODO: see how this works on QActions
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

# TODO: FIND SOMETHING BETTER FOR DOCSTRINGS!!!
def createAction(name: str, parent: QObject, func, shortcut: str = None):
	"""Generate and return a QAction with a name and connected function.\\\n
	Shortcuts snd a mnemonic can also be specified.

	**name:**
		This string will appear as the name of the QAction if used in a GUI.\\\n
		A mnemonic can be specified by placing an ampersand ('&') before a single character of choice. The ampersand wont be displayed.\\\n
		Examples:
				``'Paste'``\\\n
				``'Cu&t'``\\\n
	**parent:**
		The QObject to set as the parent of the QAction.
	**func:**
		The function to be called when the action is triggered.
	**shortcut:**
		Keyboard shortcut that will trigger the action.\\\n
		-- Technically this would also work with mouse shortcuts, but this function isn't set up to handle that.\\\n
		Examples:
		 	``'Ctrl+v'``\\\n
		 	``'Ctrl+Alt+0'``\\\n
		 	``'Alt+Shift+U'``\\\n
	"""
	act = QAction(name)
	act.setParent(parent)
	if shortcut is not None:
		act.setShortcut(shortcut)

	# def Link():
	# 	wrapper(print, "Cut").call()

	# act.triggered.connect(Link)

	# noinspection PyUnresolvedReferences
	act.triggered.connect(func)  # Might be best to replace this with setTriggerFunction instead

	return act

# TODO: FIND SOMETHING BETTER FOR DOCSTRINGS!!!
def createAction2(name: str, parent: QObject, func, shortcut: str = None, icon: QIcon = QIcon(None), toolTip: str = None, statusTip: str = None,
				  isCheckable: bool = None):
	"""Generate and return a QAction intended to be visually added to a GUI.\\\n
	====

	**name:**
		This string will appear as the name of the QAction if used in a GUI.\\\n
		A mnemonic can be specified by placing an ampersand ('&') before a single character of choice. The ampersand wont be displayed.\\\n
		Examples:
				``'Paste'``\\\n
				``'Cu&t'``\\\n
	**parent:**
		The QObject to set as the parent of the QAction.
	**func:**
		The function to be called when the action is triggered.
	**shortcut:**
		Keyboard shortcut that will trigger the action.\\\n
		-- Technically this would also work with mouse shortcuts, but this function isn't set up to handle that.\\\n
		Examples:
		 	``'Ctrl+v'``\\\n
		 	``'Ctrl+Alt+0'``\\\n
		 	``'Alt+Shift+U'``\\\n
	**icon:**
		An icon to display with the QAction. This **must** be set for tooltips to display. Accepted default of ``QIcon(None)``.
	**toolTip:**
		This string will be displayed as a tooltip when the cursor is placed over the QAction.
	**statusTip:**
		If shown in a GUI with a status bar, this string will be displayed in the status bar when the cursor is placed over the QAction.
		Requires ``parent`` not to be ``None``.
	**isCheckable:**
		Whether this QAction should display with a visible marking to indicate its state.
	"""
	act = createAction(name, parent, func, shortcut)

	if icon is None:
		act.setIcon(QIcon(None))
	else:
		act.setIcon(icon)

	if statusTip is not None:
		act.setStatusTip(statusTip)
	if toolTip is not None:
		act.setToolTip(toolTip)
	if isCheckable is not None:
		act.setCheckable(isCheckable)

	return act

# '''Generate and return a QAction intended to be visually added to a GUI.\\\n
#  Parameters
# ====
#
# 	**statusTip:**
# 		If shown in a GUI with a status bar, this string will be displayed in the status bar when the cursor is placed over the QAction.
# '''
