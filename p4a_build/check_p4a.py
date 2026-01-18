#!/usr/bin/env python3
import sys
print("Python version:", sys.version)
print("Python path:", sys.path)
try:
    import pythonforandroid
    print("Python for Android version:", pythonforandroid.__version__)
except ImportError as e:
    print("Import error:", e)
    import traceback
    traceback.print_exc()