# lanx-calc
Script for simple calculation of return times on OGame

Features:
- calculate speed, distance, travel time and return time
- supports early recall and takes interval between scans into consideration
- saves uni settings upon any changes*
- operates with server times, works with dates for extra long deploy missions
- assemble report and copy it on clipboard to share with other players

*saving does not work unless the script is provided write permissions, in Program Files folder this usually isn't the case so it's recommended to install the script in Documents folder

*if you still prefer the app in program files, you can manually edit preset.ini file to match your desired uni settings

GUI.py - main script

setup.py - cx_Freeze setup script

icon.ico - required for setup script to work correctly

preset.ini - settings file -> first two lines can be any number, following two lines are 0 for false or 1 for true and last two lines represent general and collector speed bonuses

Visit OGame EN LanxCalc forum topic for more info or questions or contact me on PM (savage)

