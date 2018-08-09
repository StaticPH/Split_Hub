Control Hub
===========
Control Hub is a utility type Python application that seeks to consolidate into one place
a number of features I regularly use from different applications.
One of the most important aspects of this application is configurability, the idea being to make
configurable everything I can forsee a reason for.


This project is made possible using the PyQt5 framework for Python 3, and is written entirely in the developer's free time.
As this project is very much experimental, there are likely to be sections of code of comments which serve no
purpose, and remain present solely as notes for the developer.
Suggestions, commits, contributions, constructive criticism, advice, and the like are all welcome.
Please note that the developer has no obligation to fix or respond to any reported issues or suggestions.


Features/TODO List
------------------
    *Mutually exclusive checkboxes/toggle buttons for battery settings/plans.
    *Histograph of motherboard, CPU, HDD, and SSD temperatures.
    *Display indicating current CPU clock speed. maybe only update every 5-10 seconds?
    *Display indicating CPU usage % and #of processes
    *Display indicating current RAM usage. probably in the form of a vertical bar AND a text label.
    *Display of (local/computer) date and time. local weather if arrangeable
    *Application close confirmation popup (Will be toggled in preferences)
    *Make status bar at bottom of page have clearly defined edges
    *Use QDockWidget to create a tool palette(like in a web browser) from which the user can customize which widgets should be where on the toolbar
    *Add a method of resetting the window layout to the default. Obviously this means there should *be* a default
    * Create an extended version of QSettings' setValue and value functions, which should respectively
        * require a parameter, either a string or a type(undecided), to indicate the type the value should be given. This should be prepended to all config entries, in the form of "B:"(bool), "S:"(string), etc.
        * ignore the first 2 characters of all config entries???, which should be an indicator of value type. Also, automatically run correctBoolean on all entries prepended with "B:"

    * ? Have a list of QActions initialized in some kind of loop?
    * ? Add a list of keybinds, maybe use https://doc.qt.io/qt-5/qaction.html#shortcuts ?
    * ?   Display of current network I/O ?
    * ?   Allow adjusting colors of histograph/chart/progress bar attributes through a (menu accessed popup or tab?) application preferences (menu?)
    * ? Make 'hidden'(only accessible via config, maybe even not shown there by default) config for specifying an alternate logo
    * ? "Quick Launch" buttons for various applications(Ex: Snipping Tool). Possibly even buttons that launch multiple at a time ?

    *WIP: Add config menu items for the desired window flags(Ex: Keep-on-top, frameless window, etc)
    *WIP: Implement a "Dark" mode
    * Make a page in the settings gui where menu entries can be customized to an extent. At the very least, make a list that autoloads all styles QStyleFactory already knows about, and allows the user to configure which styles show up in the menu.

    *REDO:  Keep on top capability
    *REDO:  Sync settings TO config before close

    *DONE:  Button to clear system clipboard
    *DONE:  Universal color picker function. WITH A PIPETTE TOOL
    *DONE:  Retain previous settings
    *DONE: 	Make sure that the configured style appears as checked on load
    *DONE: 	Edit the logo to make the white background transparent
    *DONE:  Add a system tray icon which can be enabled/disabled from the config file
    *DONE:  Give main toolbar its own context menu with a CHECKABLE option to lock/unlock the toolbar
    *DONE:  Give main toolbar its own context menu with a CHECKABLE option to float/unfloat the toolbar

    *NOT FEASIBLE WITHOUT REWORKING/REPLACING QSETTINGS. RECONSIDERING: Add descriptive text into the config file, if at all possible.
