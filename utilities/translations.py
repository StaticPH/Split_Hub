# The method used here was inspired by Ninja IDE
# https://github.com/ninja-ide/ninja-ide/blob/master/ninja_ide/translations.py

# Though it currently doesnt exactly work
# https://github.com/ninja-ide/ninja-ide/blob/4935283901c8ea8f38bf507a73e5e6b346b4aa61/ninja_ide/gui/__init__.py#L77
# http://doc.qt.io/qt-5/internationalization.html

from PyQt5.QtCore import QCoreApplication

tr = QCoreApplication.translate

TR_DEFAULT = tr("string", "Default")
TR_PLACEHOLDER = tr("string", "placeholder")

# Tools
TR_COLR_PKR = tr("Tool Name", "Color Picker")
TR_CLR_CLIP = tr("Tool Name", "Clear Clipboard")

# Main Menu Entries	 (Level 1)
TR_MAINMENU_FILE = tr("MainMenu", "&File")
TR_MAINMENU_EDIT = tr("MainMenu", "&Edit")
TR_MAINMENU_VIEW = tr("MainMenu", "&View")

# Submenu Entries	 (Level 2)
TR_VIEWMENU_STYLES = tr("ViewMenu", "&Styles")
TR_VIEWMENU_LAYOUT = tr("ViewMenu", "&Layout")

# Style Menu Entries (Level 3)
TR_STYLEMENU_FUSION = tr("Style Name", "Fusion")
TR_STYLEMENU_WINDOWS = tr("Style Name", "Windows")
TR_STYLEMENU_VISTA = tr("Style Name", "Windows Vista")
TR_STYLEMENU_XP = tr("Style Name", "Windows XP")

# Style Menu Tooltips
TR_STYLEMENU_FUSION_TOOLTIP = tr("Style Menu", "Set window style to Fusion")
TR_STYLEMENU_WINDOWS_TOOLTIP = tr("Style Menu", "Set window style to Windows")
TR_STYLEMENU_VISTA_TOOLTIP = tr("Style Menu", "Set window style to Windows Vista")
TR_STYLEMENU_XP_TOOLTIP = tr("Style Menu", "Set window style to Windows XP")
# TR_STYLEMENU_UNDEFINED_TOOLTIP = tr("Style Menu", "???")

# Actions
TR_ACT_CUT = tr("Actions", "Cu&t")
TR_ACT_COPY = tr("Actions", "&Copy")
TR_ACT_PASTE = tr("Actions", "&Paste")
TR_ACT_QUIT = tr("Actions", "&Quit")

# Toolbar
TR_TOOLBAR_DOCKMODE = tr("Toolbar Mode", "Docked Mode")
TR_TOOLBAR_FLOATMODE = tr("Toolbar Mode", "Floating Mode")
TR_TOOLBAR_DOCKMODE_STIP = tr("Toolbar Mode StatusTip", "Lock(/unlock(dock/undock) the toolbar")
TR_TOOLBAR_FLOATMODE_STIP = tr("Toolbar Mode StatusTip", "Enable/disable floating the toolbar as a separate window")
TR_TOOLBAR_FLOATMODE_TTIP = tr("Toolbar Mode StatusTip", "NOTE: Disabling does not automatically unfloat the toolbar.\n" +
							   "Moving the toolbar a little bit will unfloat it and return it to its docked position in the window.")
