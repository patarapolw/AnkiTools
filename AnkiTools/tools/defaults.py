import json
from collections import OrderedDict

from AnkiTools.dir import module_path


class ReadOnlyJsonObject:
    def __init__(self, data, dumps_kw: dict=None, loads_kw: dict=None):
        if dumps_kw is None:
            dumps_kw = dict()
        if loads_kw is None:
            self._loads_kw = dict(object_pairs_hook=OrderedDict)
        else:
            self._loads_kw = loads_kw

        if isinstance(data, str):
            self._json_string = data
        else:
            self._json_string = json.dumps(data, **dumps_kw)

    @property
    def data(self):
        return json.loads(self._json_string, **self._loads_kw)

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


# Load auto-generated default values from Anki (collection.anki2)
with open(module_path('defaults.json')) as f:
    defaults = json.load(f, object_pairs_hook=OrderedDict)

DEFAULT_MODEL = ReadOnlyJsonObject(tuple(defaults['models'].values())[0])
DEFAULT_TEMPLATE = ReadOnlyJsonObject(DEFAULT_MODEL['tmpls'][0])

# Load author-defined default values
with open(module_path('defaults_api.json')) as f:
    defaults = json.load(f, object_pairs_hook=OrderedDict)

DEFAULT_API_MODEL_DEFINITION = ReadOnlyJsonObject(defaults['model_definition'])
