from typing import Any
# I cant help but wonder how much overhead is added by including QObject solely for type hinting
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QAction, QLayout

from utilities.Common import wrapper

def addAllActionsToObject(parent, obj):
	""" Find all QActions whose parent is ``self`` and call ``obj.addAction()`` for each of them. """
	for member in vars(parent).values(): obj.addAction(member) if type(member) == QAction else None

# TODO: stop using such a shoddy method of doing this. Hopefully much of this can be replaced with lambdas
def funcLink(func: Any):
	if isinstance(func, wrapper):
		def link(): func.call()

		return link
	elif callable(func):
		# print(func.__name__ + ' is not a wrapper. It is a ' + type(func).__name__)
		return func
	else:
		return None

def setTriggerResponse(obj: QObject, func: Any, errMsgHead: str = None):
	"""	Set a ``QObject``'s response to being triggered.\\\n
	:param obj: The ``QObject`` for which to set the trigger response
	:param func: The function to call when the ``QObject`` is triggered
	:param errMsgHead: If ``func`` is None, this string will be used for an error message that will print to the console.
	"""
	_func = funcLink(func)
	if _func is not None:
		# obj.triggered.connect(_func, Qt.AutoConnection) #Qt.AutoConnection is the default anyways
		obj.triggered.connect(_func)
	else:
		if errMsgHead is None:
			print('A functionless object has been triggered.')
		else:
			print(errMsgHead + ' has no function')

def setClickedResponse(obj: QObject, func: Any, errMsgHead: str = None):
	"""	Set a ``QObject``'s response to being clicked.\\\n
	:param obj: The ``QObject`` for which to set the click response
	:param func: The function to call when the ``QObject`` is clicked
	:param errMsgHead: If ``func`` is None, this string will be used for an error message that will print to the console.
	"""
	_func = funcLink(func)
	if _func is not None:
		obj.clicked.connect(_func)
	else:
		if errMsgHead is None:
			print('A functionless object has been clicked.')
		else:
			print(errMsgHead + ' has no function')

def setStateChangedResponse(obj: QObject, func: Any, errMsgHead: str = None):
	"""	Set a ``QObject``'s response to a change in its state.\\\n
	:param obj: The ``QObject`` for which to set the response
	:param func: The function to call when the ``QObject`` experiences a state change
	:param errMsgHead: If ``func`` is None, this string will be used for an error message that will print to the console.
	"""
	_func = funcLink(func)
	if _func is not None:
		obj.statechanged.connect(_func)
	else:
		if errMsgHead is None:
			print('A functionless object has changed states.')
		else:
			print(errMsgHead + ' has no function')

# noinspection PyUnusedLocal
def setSignalResponse(obj: QObject, signal: pyqtSignal, func: Any, errMsgHead: str = None):
	"""	Set a ``QObject``'s response to some signal.\\\n
	:param obj: The ``QObject`` for which to set the signal response
	:param signal: The signal to which the ``QObject`` is responding
	:param func: The function to call when the ``QObject`` is signaled
	:param errMsgHead: If ``func`` is None, this string will be used for an error message that will print to the console.
	"""
	# obj.signal = signal
	_func = funcLink(func)
	if _func is not None:
		obj.signal.connect(_func)
	else:
		if errMsgHead is None:
			print('A functionless object has been signaled.')
		else:
			print(errMsgHead + ' has no function')

def layoutContents(layout: QLayout): return (layout.itemAt(i) for i in range(layout.count()))