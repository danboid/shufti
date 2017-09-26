# cx_freeze Windows msi package build script for shufti

# Install python 3 then use pip to install pyqt5 and cx_freeze. Then copy
# this file into the same dir as shufti.py, shufti.ico and cx_freeze and run:

# > python setup.py bdist_msi

from cx_Freeze import setup, Executable
import sys

buildOptions = dict(packages = [], excludes = [])

# base = 'Win32GUI' stops the python console window opening when starting shufti

executables = [
    Executable(script='shufti.py', base = 'Win32GUI', icon='shufti.ico')
]

setup(name='shufti',
      version = '2.3',
      description = 'The Persistent Image Viewer',
      author = 'Dan MacDonald',
      options = dict(build_exe = buildOptions),
      executables = executables)
