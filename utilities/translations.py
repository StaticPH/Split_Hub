# The method used here was inspired by Ninja IDE
# https://github.com/ninja-ide/ninja-ide/blob/master/ninja_ide/translations.py

# Though it currently doesnt exactly work
# https://github.com/ninja-ide/ninja-ide/blob/4935283901c8ea8f38bf507a73e5e6b346b4aa61/ninja_ide/gui/__init__.py#L77
# http://doc.qt.io/qt-5/internationalization.html

from PyQt5.QtCore import QCoreApplication

tr = QCoreApplication.translate

TR_APPNAME = tr('application name', 'ControlHub')
TR_DEFAULT = tr('string', 'Default')
TR_PLACEHOLDER = tr('string', 'placeholder')
TR_STATUSTIP_SUFFIX = '_STIP'
TR_TOOLTIP_SUFFIX = '_TTIP'

# Tools
TR_COLR_PKR = tr('Tool Name', 'Color Picker')
TR_CLR_CLIP = tr('Tool Name', 'Clear Clipboard')

# Main Menu Entries	 (Level 1)
TR_MAINMENU_FILE = tr('Main Menu', '&File')
TR_MAINMENU_EDIT = tr('Main Menu', '&Edit')
TR_MAINMENU_VIEW = tr('Main Menu', '&View')

# Submenu Entries	 (Level 2)
TR_FILEMENU_PREFS = tr('File Menu', 'Preferences')
TR_VIEWMENU_STYLES = tr('View Menu', '&Styles')
TR_VIEWMENU_LAYOUT = tr('View Menu', '&Layout')

# File Menu Statustips
TR_FILEMENU_PREFS_STIP = tr('File Menu', 'View and edit application settings')

# Style Menu Entries (Level 3)
TR_STYLEMENU_FUSION = tr('Style Name', 'Fusion')
TR_STYLEMENU_WINDOWS = tr('Style Name', 'Windows')
TR_STYLEMENU_WINDOWSVISTA = tr('Style Name', 'Windows Vista')
TR_STYLEMENU_WINDOWSXP = tr('Style Name', 'Windows XP')
TR_STYLEMENU_MACINTOSH = tr('Style Name', 'macOS')
TR_STYLEMENU_GTK = tr('Style Name', 'GTK')

# Style Menu Statustips
TR_STYLEMENU_GENERIC_STIP = tr('Style Menu', 'Set window style to ')
# TR_STYLEMENU_UNDEFINED_STIP = tr('Style Menu', '???')
TR_STYLEMENU_FUSION_STIP = tr('Style Menu', TR_STYLEMENU_GENERIC_STIP + TR_STYLEMENU_FUSION)
TR_STYLEMENU_WINDOWS_STIP = tr('Style Menu', TR_STYLEMENU_GENERIC_STIP + TR_STYLEMENU_WINDOWS)
TR_STYLEMENU_WINDOWSVISTA_STIP = tr('Style Menu', TR_STYLEMENU_GENERIC_STIP + TR_STYLEMENU_WINDOWSVISTA)
TR_STYLEMENU_WINDOWSXP_STIP = tr('Style Menu', TR_STYLEMENU_GENERIC_STIP + TR_STYLEMENU_WINDOWSXP)
TR_STYLEMENU_MACINTOSH_STIP = tr('Style Menu', TR_STYLEMENU_GENERIC_STIP + TR_STYLEMENU_MACINTOSH)
TR_STYLEMENU_GTK_STIP = tr('Style Menu', TR_STYLEMENU_GENERIC_STIP + TR_STYLEMENU_GTK)

# Actions
TR_ACT_CUT = tr('Actions', 'Cu&t')
TR_ACT_COPY = tr('Actions', '&Copy')
TR_ACT_PASTE = tr('Actions', '&Paste')
TR_ACT_QUIT = tr('Actions', '&Quit')

# Action Statustips
TR_ACT_CUT_STIP = tr('Action Statustips', 'Cut to clipboard')
TR_ACT_COPY_STIP = tr('Action Statustips', 'Copy to clipboard')
TR_ACT_PASTE_STIP = tr('Action Statustips', 'Paste from clipboard')
TR_ACT_QUIT_STIP = tr('Action Statustips', 'Exit ' + TR_APPNAME)


# Toolbar
TR_TOOLBAR_DOCKMODE = tr('Toolbar Mode', 'Docked Mode')
TR_TOOLBAR_FLOATMODE = tr('Toolbar Mode', 'Floating Mode')
TR_TOOLBAR_DOCKMODE_STIP = tr('Toolbar Mode StatusTip', 'Lock(/unlock(dock/undock) the toolbar')
TR_TOOLBAR_FLOATMODE_STIP = tr('Toolbar Mode StatusTip', 'Enable/disable floating the toolbar as a separate window')
TR_TOOLBAR_FLOATMODE_TTIP = tr('Toolbar Mode ToolTip', 'NOTE: Disabling does not automatically unfloat the toolbar.\n' +
							   'Moving the toolbar a little bit will unfloat it and return it to its docked position in the window.')