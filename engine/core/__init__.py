"""Core module for BOS-FS."""
import importlib
import sys
import os

_core_dir = os.path.dirname(os.path.abspath(__file__))
for name in sorted(os.listdir(_core_dir)):
    path = os.path.join(_core_dir, name)
    if os.path.isdir(path) and os.path.exists(os.path.join(path, '__init__.py')):
        if name not in sys.modules:
            sys.path.insert(0, path)
