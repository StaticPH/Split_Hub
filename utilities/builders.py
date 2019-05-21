from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
	QAction, QPushButton, QCheckBox, QDialog, QDialogButtonBox, QLineEdit, QLabel, QHBoxLayout, QMessageBox
)

from utilities.QtHelpers import setTriggerResponse, setClickedResponse, setStateChangedResponse

# TODO: limit to use EITHER toolTip OR statusTip, but not both at once

def createAction(parent: QObject or None, name: str, func, shortcut: str = None,
				 sContext:Qt.ShortcutContext=Qt.WindowShortcut) -> QAction:
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
	**sContext:**
		What context the shortcut is valid in.
	"""
	act = QAction(name)
	if parent is not None:
		act.setParent(parent)
	if shortcut is not None:  # Technically act.setShortcut can be called even if shortcut is None, but just to be safe...
		act.setShortcut(shortcut)
		if sContext is not None:
			act.setShortcutContext(sContext)

	# if isinstance(func, wrapper):
	# 	def link():
	# 		func.call()
	#
	# 	act.triggered.connect(link)  # Might be best to replace this with setTriggerFunction instead
	# elif func is not None:
	# 	act.triggered.connect(func)  # Might be best to replace this with setTriggerFunction instead
	# else:
	# 	raise ("Error! Cannot create QAction " + repr(name) + " with func = None.")
	setTriggerResponse(act, func)
	return act

# TODO: FIND SOMETHING BETTER FOR DOCSTRINGS
def createAction2(parent: QObject or None, name: str, func, shortcut: str = None,
				  sContext:Qt.ShortcutContext=Qt.WindowShortcut, icon: QIcon = QIcon(None),
				  toolTip: str = None, statusTip: str = None, isCheckable: bool = None) -> QAction:
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
	**sContext:**
		What context the shortcut is valid in.
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
	act = createAction(parent, name, func, shortcut, sContext)

	if icon is None:
		act.setIcon(QIcon(None))
	else:
		act.setIcon(icon)

	if statusTip is not None:  # Technically it should be fine even if these are all set to None, but just in case...
		act.setStatusTip(statusTip)
	if toolTip is not None:
		act.setToolTip(toolTip)
	if isCheckable is not None:
		act.setCheckable(isCheckable)

	# if shortcut	is not None:
	# 	act.setShortcutVisibleInContextMenu(True)

	return act

def uselessButton(parent: QObject, label: str = None,
				  toolTip: str = None, statusTip: str = None,
				  icon: QIcon = QIcon(None), X: int = None, Y: int = None) -> QPushButton:
	"""Create a ``QPushButton`` that serves no functional purpose.
		**parent:**
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
	btn = QPushButton(parent)

	# It might be desirable not to have a label at times
	if label is not None:
		btn.setText(label)

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

	btn.adjustSize()
	return btn

# Really, since this function(and triggerButton) just passes icon to uselessButton,
# which itself makes sure to set a valid QIcon, the icon parameter COULD just be `icon: str = None`
def clickButton(parent: QObject, label: str = None,
				func = None, toolTip: str = None, statusTip: str = None,
				icon: QIcon = QIcon(None), X: int = None, Y: int = None) -> QPushButton:
	"""	Creates a simple (click-type response) ``QPushButton``.\\\n
	**parent:**
		The ``QObject`` to set as the parent of the ``QPushButton``.
	**func:**
		The function to be called when the ``QPushButton`` is clicked.\\\n
	See ``uselessButton`` for other parameters.
	"""
	btn = uselessButton(parent, label, toolTip, statusTip, icon, X, Y)

	setClickedResponse(btn, func, 'clickButton with text ' + repr(label))

	return btn

def triggerButton(parent: QObject, label: str = None,
				  func = None, toolTip: str = None, statusTip: str = None,
				  icon: QIcon = QIcon(None), X: int = None, Y: int = None) -> QPushButton:
	"""	Creates a simple (trigger-type response) ``QPushButton``.\\\n
	**parent:**
		The ``QObject`` to set as the parent of the ``QPushButton``.
	**func:**
		The function to be called when the action is triggered.\\\n
	See ``uselessButton`` for other parameters.
	"""
	btn = uselessButton(parent, label, toolTip, statusTip, icon, X, Y)

	setTriggerResponse(btn, func, 'triggerButton with text ' + repr(label))

	return btn

def basicCheckBox(parent: QObject, func = None, text: str = None,
				  toolTip: str = None, statusTip: str = None,
				  X: int = None, Y: int = None) -> QCheckBox:
	"""Simple checkbox"""
	# TODO: properly document
	checkBox = QCheckBox(parent)

	if text is not None:
		checkBox.setText(text)

	if toolTip not in (None, ''):
		checkBox.setToolTip(toolTip)
		if statusTip == '':
			checkBox.setStatusTip(toolTip)

	if statusTip not in (None, ''):
		checkBox.setStatusTip(statusTip)
		if toolTip == '':
			checkBox.setToolTip(statusTip)

	if X is not None and Y is not None:
		checkBox.move(X, Y)

	# if isinstance(func, wrapper):
	# 	def link():
	# 		func.call()
	#
	# 	checkBox.stateChanged.connect(link)
	# elif func is not None:
	# 	checkBox.stateChanged.connect(func)
	# else:
	# 	print("basicCheckbox with text " + repr(text) + " has no function")
	setStateChangedResponse(checkBox, func)

	checkBox.adjustSize()

	return checkBox

def menuItem(parent: QObject, func, name: str, statusTip: str = None,
			 shortcut: str = None, isToggle: bool = False, group = None) -> QAction:
	"""	'Template' function for a simple menu item	"""
	# TODO: Document
	item = QAction(name, parent)
	item.setStatusTip(statusTip)

	if shortcut is not None:
		item.setShortcut(shortcut)
	if isToggle != False:
		item.setCheckable(True)
	if group is not None:
		group.addAction(item)

	errMsgHead = 'Menu item ' + repr(name)
	setTriggerResponse(item, func, errMsgHead)

	return item

def toolBar_Text(parent: QObject, text: str, func, toolTip: str = None,
				 statusTip: str = None, enabled: bool = True) -> QAction:
	"""	'Template' function for a text-only toolbar button	"""
	# TODO: Document
	item = QAction(text, parent)

	setTriggerResponse(item, func, 'One or more text type items on your toolbar')

	if toolTip not in (None, ''):
		item.setToolTip(toolTip)
		if statusTip == '':
			item.setStatusTip(toolTip)

	if statusTip not in (None, ''):
		item.setStatusTip(statusTip)
		if toolTip == '':
			item.setToolTip(statusTip)

	item.setEnabled(enabled)
	return item

def toolBar_Icon(parent, icon: str, func, toolTip: str = None, statusTip: str = None):
	"""	'Template' function for a toolbar button with an icon	"""
	item = QAction(QIcon(icon), toolTip, parent)  # TODO: consider replacing this with a call to createAction2

	if toolTip is None and statusTip is not None:
		item.setStatusTip(statusTip)

	setTriggerResponse(item, func, 'One or more icon type items on your toolbar')

	return item

def createResponseButton(dialog: QDialog, obj: QPushButton, func, shortcut: str = None,
						 isDefault: bool = False, closeWhenDone: bool = True) -> QPushButton:
	# TODO: Document
	setClickedResponse(obj, func)
	if closeWhenDone:
		# In addition to the specified function, also close the dialog after clicking the button.
		setClickedResponse(obj, dialog.close)
	if shortcut is not None:
		obj.setShortcut(shortcut)
	if isDefault is not None:
		obj.setAutoDefault(isDefault)
		obj.setDefault(isDefault)
	return obj

def createResponseBox(dialog: QDialog, acceptFunc, rejectFunc,
					  acceptClose: bool = True, rejectClose: bool = True,
					  acceptText: str = 'Co&nfirm', rejectText: str = 'C&ancel',
					  default: bool = False) -> QDialogButtonBox:
	"""	Returns a QDialogButtonBox with buttons for accept and reject.\\\n
	**dialog:**
		The ``QDialog`` to which the ``QDialogButtonBox`` will be added.
	**acceptFunc:**
		The function to be called if the dialog is accepted.\\\n
	**rejectFunc:**
		The function to be called if the dialog is rejected.\\\n
	**acceptClose:**
		Whether accepting the dialog should close it.\\\n
	**rejectClose:**
		Whether rejecting the dialog should close it.\\\n
	**acceptText and rejectText:**
		The text string to display within the button.\\\n
		Inserting an ampersand before any character will specify that character as the button's mnemonic.
		Note that while the ampersand will not be displayed in the UI, the character it precedes will be.\\\n
	**default:**
		True if the default response is to accept the dialog, False for reject.\\\n
	"""

	responses = QDialogButtonBox(QDialogButtonBox.NoButton, Qt.Horizontal)
	responses.apply = responses.addButton(acceptText, QDialogButtonBox.AcceptRole)
	responses.discard = responses.addButton(rejectText, QDialogButtonBox.RejectRole)

	createResponseButton(dialog, responses.apply, acceptFunc, None, True if default else False, acceptClose)
	createResponseButton(dialog, responses.discard, rejectFunc, None, False if default else True, rejectClose)
	return responses

def createSignalingResponseBox(dialog: QDialog, acceptSignal: pyqtSignal, rejectSignal: pyqtSignal,
							   acceptEmission = 'Accept button clicked', rejectEmission = 'Reject button clicked',
							   acceptClose: bool = True, rejectClose: bool = True) -> QDialogButtonBox:
	# TODO: Document
	return createResponseBox(
			dialog,
			lambda: acceptSignal.emit(acceptEmission), lambda: rejectSignal.emit(rejectEmission),
			acceptClose, rejectClose
	)

# WIP
def aboutPopup(parent: QObject, text: str, title: str = None, icon: QIcon = QIcon(None), modal: bool = True):
	popup = QMessageBox()
	# popup.about()
	popup.setText(text)
	popup.setModal(modal)
	if parent is not None:
		popup.setParent(parent)
	if title is not None:
		popup.setWindowTitle(title)
	if icon is not None:
		popup.setIcon(icon)
	return popup

# WIP
def errorPopup(parent: QObject, text: str, title: str = None) -> None:
	popup = QMessageBox()
	popup.setText(text)
	popup.setAttribute(Qt.WidgetAttribute(Qt.ApplicationModal))
	if parent is not None:
		popup.setParent(parent)
	if title is not None:
		popup.setWindowTitle(title)
	popup.show()

# WIP
class LabeledLineEdit(QLineEdit, QLabel):
	"""A pre-paired QLineEdit and QLabel positioned directly adjacent to one another."""

	# TODO: Switch to using this instead of manually pairing Labels and LineEdits
	def __init__(self, label: str, placeHolderText: str = None, parent: QObject = None):
		super(LabeledLineEdit, self).__init__()
		if parent is not None:
			self.setParent(parent)
		self.line = QLineEdit()
		if placeHolderText is not None:
			self.line.setPlaceholderText(placeHolderText)
		self.label = QLabel(label)
		self.label.setBuddy(self.line)
		lay = QHBoxLayout()
		lay.addWidget(self.label)
		lay.addWidget(self.line, 10)
		self.setLayout(lay)

if __name__ == '__main__':
	import sys
	from PyQt5.QtCore import Qt
	from PyQt5.QtWidgets import QApplication

	app = QApplication(sys.argv)
	app.setApplicationName('test')
	app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
	# Start test code section

	# End test code section

	sys.exit(app.exec_())