import json
from collections import OrderedDict

from AnkiTools.dir import module_path

# Load auto-generated default values from Anki (collection.anki2)
with open(module_path('defaults.json')) as f:
    defaults = json.load(f, object_pairs_hook=OrderedDict)

DEFAULT_MODEL = tuple(defaults['models'].values())[0]
DEFAULT_TEMPLATE = DEFAULT_MODEL['tmpls'][0]

# Load author-defined default values
with open(module_path('defaults_api.json')) as f:
    defaults = json.load(f, object_pairs_hook=OrderedDict)

DEFAULT_API_MODEL_DEFINITION = defaults['model_definition']
