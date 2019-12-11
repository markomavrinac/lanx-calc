import sys
from cx_Freeze import setup, Executable
import GUI

includeFiles = ['preset.ini','changelog.txt','icon.ico']
bdist_msi_options = {
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\LanxCalc',
    }
setup(
    name = "LanxCalc",
    version = GUI.version,
    description = "Calculate return times like a boss.",
    executables = [Executable("GUI.py", base = "Win32GUI", icon = "icon.ico")],
    options={'bdist_msi': bdist_msi_options,'build_exe':{'include_files':includeFiles}})
