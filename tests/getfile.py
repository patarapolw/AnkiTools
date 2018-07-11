import os
import json
from collections import OrderedDict


def get_file(filename):
    return os.path.join('tests', 'files', filename)


def get_parameters():
    with open(os.path.join('tests', 'parameters.json')) as f:
        params = json.load(f, object_pairs_hook=OrderedDict)

    return params
