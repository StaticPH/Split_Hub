# from PyQt5.QtWidgets import QApplication

from utilities.builders import createAction
from utilities import translations as tr
from utilities.Common import gen__All__

# TODO: Make all shortcuts configurable

# app = QApplication.instance()

"""Declare editing Actions"""
# class editingActions()

#FIXME REWORK SHORTCUTS SO THEY ACTUALLY WORK. I suspect that they are being treated as invalud for some reason.
#FIXME make shortcuts visible in context menu. they reaaly should already be, but that requires the shortcuts be valid first.
'''Cut'''
# def Link(): wrapper(print, 'Cut').call()
actCut = createAction(None, tr.TR_ACT_CUT, lambda: print('Cut'), 'Ctrl+X')#, Qt.ApplicationShortcut)
actCut.setShortcutVisibleInContextMenu(True)

'''Copy'''
# def Link(): wrapper(print, 'Copy').call()
actCopy = createAction(None, tr.TR_ACT_COPY, lambda: print('Copy'), 'Ctrl+C')#, Qt.ApplicationShortcut)
actCopy.setShortcutVisibleInContextMenu(True)

'''Paste'''
# def Link(): wrapper(print, 'Paste').call()
actPaste = createAction(None, tr.TR_ACT_PASTE, lambda: print('Paste'), 'Ctrl+v')#, Qt.ApplicationShortcut)
actPaste.setShortcutVisibleInContextMenu(True)

__all__ = gen__All__(locals(), ['tr', 'createAction', 'QApplication', 'Qt'])
if __name__ == '__main__':
	print('__all__ = ', __all__)