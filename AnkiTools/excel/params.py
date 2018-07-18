from datetime import datetime
from typing import NamedTuple
from collections import OrderedDict
import enum

from AnkiTools.tools.defaults import DEFAULT_MODEL


class AddNotePattern(enum.Enum):
    """
    Specify how cards are distributed when add notes with AnkiDirect.add()
    """
    IN_ONE_DECK=enum.auto()
    ONE_CARD_TYPE_PER_SUB_DECK=enum.auto()


class Params(NamedTuple):
    """
    Output to the top of '.settings'
    - created: str ISO format of created datetime
    - modified: str ISO format of modified datetime
    - add_note_pattern: AddNotePattern enum
    - add_note_template: str JSON string of defaults of how notes are added.
    """
    created: str=datetime.fromtimestamp(datetime.now().timestamp()).isoformat()
    modified: str=datetime.fromtimestamp(datetime.now().timestamp()).isoformat()
    add_note_pattern: AddNotePattern=AddNotePattern.ONE_CARD_TYPE_PER_SUB_DECK
    add_note_template: str='{}'


class CardsInDeckTuple(NamedTuple):
    """
    Output to '.settings' CardsInDeck table.
    """
    card_id: int
    note_id: int
    deck_name: str
    template_name: str
    order: int


class AnkiTuple(NamedTuple):
    """
    Output to *.xlsx is in this order:
    - params: Params
    - models: sorted k, v pair (OrderedDict), where k is deck_id and v is ModelTuple.
    - decks: sorted k, v pair (OrderedDict), where k is deck_id and v is CardsInDeckTuple.
             params, definitions, and decks are all in '.settings' sheet.
    - notes: sorted k, v pair (OrderedDict), where k is note_id and v is OrderedDict.
             notes are in unique sheets for for each notes
    """
    params: Params=Params()
    models: OrderedDict=OrderedDict()
    decks: OrderedDict=OrderedDict()
    notes: OrderedDict=OrderedDict()


class ModelTuple(NamedTuple):
    """
    Invaluable field names for a model.
    - id: int: model_id (unique)
    - name: str: model_name (unique)
    - fields_list: list of str: list of field names
    - templates_list: list of TemplateTuple:
    - css: str: CSS formatting all templates in templates_list
    """
    id: int
    name: str
    fields_list: list
    templates_list: list
    css: str = DEFAULT_MODEL['css']


class TemplateTuple(NamedTuple):
    """
    Minimal parameters for defining a template.
    - name: str: template_name
    - qfmt: str: question format, containing `{{%s}}` in fields_list. Must not be empty when rendered.
    - afmt: str: answer format, containing `{{%s}}` in fields_list. Can be empty, though.
    """
    name: str
    qfmt: str
    afmt: str
