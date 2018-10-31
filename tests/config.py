import json
from collections import OrderedDict
from pathlib import Path


with Path('tests/parameters.json').open() as f:
    PARAMS = json.load(f, object_pairs_hook=OrderedDict)
