from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QPushButton, QCheckBox

from utilities.Common import wrapper

# TODO: see how this works on QActions. If it works well, call it from createAction
def setTriggerResponse(obj: QObject, func, errMsgHead: str = None):
	"""	Set a ``QObject``'s response to being triggered.\\\n
	:param obj: The ``QObject`` for which to set the trigger response
	:param func: The function to call when the ``QObject`` is triggered
	:param errMsgHead: If ``func`` is None, this string will be used for an error message that will print to the console.
	"""
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
	"""	Set a ``QObject``'s response to being clicked.\\\n
	:param obj: The ``QObject`` for which to set the click response
	:param func: The function to call when the ``QObject`` is clicked
	:param errMsgHead: If ``func`` is None, this string will be used for an error message that will print to the console.
	"""
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
	**self:**
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
	if shortcut is not None:  # Technically I can just call act.setShortcut even if shortcut is None, but just to be safe...
		act.setShortcut(shortcut)

	if isinstance(func, wrapper):
		def link():
			func.call()

		# noinspection PyUnresolvedReferences
		act.triggered.connect(link)  # Might be best to replace this with setTriggerFunction instead
	elif func is not None:
		# noinspection PyUnresolvedReferences
		act.triggered.connect(func)  # Might be best to replace this with setTriggerFunction instead
	else:
		raise ("Error! Cannot create QAction " + repr(name) + " with func = None.")
	return act

# TODO: FIND SOMETHING BETTER FOR DOCSTRINGS!!!
def createAction2(name: str, parent: QObject, func,
				  shortcut: str = None, icon: QIcon = QIcon(None),
				  toolTip: str = None, statusTip: str = None, isCheckable: bool = None):
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
		An icon to display with the QAction. Accepted default of ``QIcon(None)``.
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

	if statusTip is not None:  # Technically I should be fine even if these are all set to None, but just in case...
		act.setStatusTip(statusTip)
	if toolTip is not None:
		act.setToolTip(toolTip)
	if isCheckable is not None:
		act.setCheckable(isCheckable)

	return act

def uselessButton(self: QObject, label: str = 'test',
				  toolTip: str = None, statusTip: str = None,
				  icon: QIcon = QIcon(None), X: int = None, Y: int = None):
	"""Create a ``QPushButton`` that serves no functional purpose.
		**self:**
			The ``QObject`` to set as the parent of the ``QPushButton``.
		**label:**
			This string will appear as the name of the ``QPushButton`` if used in a GUI.
		**toolTip:**
			This string will be displayed as a tooltip when the cursor is placed over the ``QPushButton``.
		**statusTip:**
			If shown in a GUI with a status bar, this string will be displayed in the status bar when the cursor is placed over the ``QPushButton``.
			Requires ``self`` not to be ``None``.
		**icon:**
			An icon to display with the ``QPushButton``. Accepted default of ``QIcon(None)``.
		**X, Y:**
			**x** and **y** coordinates for the ``QPushButton``
	"""
	btn = QPushButton(label, self)
	# It might be desirable not to have a label at times
	if label is None:
		btn.setText(None)

	btn.adjustSize()

	if toolTip is not None:
		btn.setToolTip(toolTip)
	if statusTip is not None:
		btn.setStatusTip(statusTip)

	if icon is None:
		btn.setIcon(QIcon(None))
	else:
		btn.setIcon(icon)

	if X is not None and Y is not None:
		btn.move(X, Y)

	return btn

# Really, since this function(and triggerButton) just passes icon to uselessButton,
# which itself makes sure to set a valid QIcon, I COULD just say something like icon: str = None
def clickButton(self: QObject, label: str = 'test',
				func = None, toolTip: str = None, statusTip: str = None,
				icon: QIcon = QIcon(None), X: int = None, Y: int = None):
	"""	Creates a simple (click-type response) ``QPushButton``.\\\n
	**self:**
		The ``QObject`` to set as the parent of the ``QPushButton``.
	**func:**
		The function to be called when the ``QPushButton`` is clicked.\\\n
	See ``uselessButton`` for other parameters.
	"""
	btn = uselessButton(self, label, toolTip, statusTip, icon, X, Y)

	setClickedResponse(btn, func, "clickButton with text " + repr(label))

	return btn

def triggerButton(self: QObject, label: str = 'test',
				  func = None, toolTip: str = None, statusTip: str = None,
				  icon: QIcon = QIcon(None), X: int = None, Y: int = None):
	"""	Creates a simple (trigger-type response) ``QPushButton``.\\\n
	**self:**
		The ``QObject`` to set as the parent of the ``QPushButton``.
	**func:**
		The function to be called when the action is triggered.\\\n
	See ``uselessButton`` for other parameters.
	"""
	btn = uselessButton(self, label, toolTip, statusTip, icon, X, Y)

	setTriggerResponse(btn, func, "triggerButton with text " + repr(label))

	return btn

# FIXME, I'M A MESS
# noinspection PyUnresolvedReferences
def basicCheckBox(self: QObject, func = None, text: str = 'test',
				  X: int = None, Y: int = None, isTri: bool = False):
	"""Simple checkbox with some handling for tri-state boxes"""
	checkBox = QCheckBox(text, self)
	checkBox.adjustSize()

	if X is not None and Y is not None:
		checkBox.move(X, Y)

	if isTri == True:
		checkBox.setTristate(True)

	if isinstance(func, wrapper):
		def link():
			func.call()

		checkBox.stateChanged.connect(link)
	elif func is not None:
		checkBox.stateChanged.connect(func)
	else:
		print("basicCheckbox with text " + repr(text) + " has no function")

	return checkBox
