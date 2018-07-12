import json
from json.decoder import JSONDecodeError
from collections import OrderedDict
from collections.abc import Mapping

from AnkiTools.dir import module_path


def _default(self, obj):
    return getattr(obj.__class__, "to_json_object", _default.default)(obj)


_default.default = json.JSONEncoder().default
json.JSONEncoder.default = _default


class ReadOnlyJsonObject(Mapping):
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
    def _data(self):
        return json.loads(self._json_string, **self._loads_kw)

    def to_json_object(self):
        return self._data

    def __getitem__(self, key):
        try:
            return json.loads(self._data[key], **self._loads_kw)
        except (TypeError, JSONDecodeError):
            return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __str__(self):
        return json.dumps(self._data, indent=2)

    def __repr__(self):
        return self._json_string


# Load auto-generated default values from Anki (collection.anki2)
with open(module_path('defaults.json')) as f:
    defaults = json.load(f, object_pairs_hook=OrderedDict)

DEFAULT_COLLECTION = ReadOnlyJsonObject(defaults['col'])
DEFAULT_MODEL = ReadOnlyJsonObject(tuple(DEFAULT_COLLECTION['models'].values())[0])
DEFAULT_TEMPLATE = ReadOnlyJsonObject(DEFAULT_MODEL['tmpls'][0])

# Load author-defined default values
with open(module_path('defaults_api.json')) as f:
    defaults = json.load(f, object_pairs_hook=OrderedDict)

DEFAULT_API_MODEL_DEFINITION = ReadOnlyJsonObject(defaults['model_definition'])


# # Load is_json settings
# IS_JSON = OrderedDict()
# with open(module_path('defaults_formatted.json')) as f:
#     defaults = json.load(f, object_pairs_hook=OrderedDict)
# for table_name, table_dict in defaults.items():
#     IS_JSON[table_name] = OrderedDict()
#     if table_dict is None:
#         continue
#
#     for header_item, v in table_dict.items():
#         try:
#             if v['is_json'] is True:
#                 IS_JSON[table_name][header_item] = True
#             else:
#                 IS_JSON[table_name][header_item] = False
#         except TypeError:
#             IS_JSON[table_name][header_item] = False
#
# IS_JSON = ReadOnlyJsonObject(IS_JSON)


def get_constants():
    constants = OrderedDict()

    for k, v in globals().items():
        if k.isupper():
            constants[k] = v

    return constants


if __name__ == '__main__':
    pass
    # print(IS_JSON['col'])
