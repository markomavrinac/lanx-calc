import sys
from cx_Freeze import setup, Executable

includeFiles = ['preset.ini']
bdist_msi_options = {
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\BPC',
    }
setup(
    name = "LanxCalc",
    version = "0.9b",
    description = "Calculate return times like a boss.",
    executables = [Executable("GUI.py", base = "Win32GUI", icon = "icon.ico")],
    options={'bdist_msi': bdist_msi_options,'build_exe':{'include_files':includeFiles}})
