"""
Defines ROOT as project_name/project_name/. Useful when installing using pip/setup.py.
"""

import os
import inspect

ROOT = os.path.abspath(os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename))


def module_path(filename):
    return os.path.join(ROOT, filename)


def excel_path(filename):
    return os.path.join(ROOT, 'excel', filename)
