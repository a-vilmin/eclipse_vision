# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'bundle_files': 1}},
    zipfile = None,
    console = [
        {
            "script": "main.py",
            "icon_resources": [(0, "icon.ico")]
            }
        ],    
)
