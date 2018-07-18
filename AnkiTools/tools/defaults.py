import simplejson as json
from simplejson.decoder import JSONDecodeError
from collections import OrderedDict
from collections.abc import Mapping
import importlib_resources


def _default(self, obj):
    return getattr(obj.__class__, "_asdict", _default.default)(obj)


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
defaults = json.loads(importlib_resources.read_text('AnkiTools', 'defaults.json'), object_pairs_hook=OrderedDict)

DEFAULT_ANKI = ReadOnlyJsonObject(defaults)
DEFAULT_COLLECTION = ReadOnlyJsonObject(defaults['col'])
DEFAULT_MODEL = ReadOnlyJsonObject(tuple(DEFAULT_COLLECTION['models'].values())[0])
DEFAULT_TEMPLATE = ReadOnlyJsonObject(DEFAULT_MODEL['tmpls'][0])
DEFAULT_NOTE = ReadOnlyJsonObject(defaults['notes_sample'][0])
DEFAULT_CARD = ReadOnlyJsonObject(defaults['cards_sample'][0])
DEFAULT_DECK = ReadOnlyJsonObject(tuple(DEFAULT_COLLECTION['decks'].values())[0])

# Load author-defined default values
defaults = json.loads(importlib_resources.read_text('AnkiTools', 'defaults_api.json'), object_pairs_hook=OrderedDict)

DEFAULT_API_MODEL_DEFINITION = ReadOnlyJsonObject(defaults["payload"]["minimal"]['model_definition'])
DEFAULT_API_PREFORMATTED_PAYLOAD = ReadOnlyJsonObject(defaults["payload"]["complete"])


def get_constants():
    constants = dict()

    for k, v in globals().items():
        if k.isupper():
            constants[k] = v

    return constants
