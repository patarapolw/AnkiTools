import os
import json
import inspect
from collections import OrderedDict

TESTS_ROOT = os.path.abspath(os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename))


def get_testing_file(filename):
    return os.path.join(TESTS_ROOT, 'files', filename)


def get_testing_parameters():
    with open(os.path.join(TESTS_ROOT, 'parameters.json')) as f:
        params = json.load(f, object_pairs_hook=OrderedDict)

    return params
