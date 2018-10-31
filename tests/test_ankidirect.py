import pytest
import shutil
from collections import OrderedDict
import json
import tempfile
import os
from pathlib import Path

from .config import PARAMS

from AnkiTools import AnkiDirect
from AnkiTools.tools.path import get_collection_path

test_parameters = PARAMS['test_ankidirect']

if 'CI' in os.environ or os.getenv('ANKI_APP_OPENED', '0') == '1':
    default_collection = Path('tests/input/collection.anki2')
else:
    default_collection = None

collections = [default_collection] + [Path('tests/input').joinpath(col) for col in json.loads(
    os.getenv('ANKI_ADDITIONAL_COLLECTIONS',
              json.dumps(["clean_collection.anki2", "dirty_collection.anki2"])))]
ankidirects = dict()
for collection in collections:
    ankidirects[collection] = AnkiDirect(anki_database=collection)


@pytest.mark.parametrize('collection', collections)
def test_models_dict(collection):
    ankidirect = ankidirects[collection]

    k, v = list(ankidirect.models_dict.items())[0]
    assert k.isdigit()
    assert isinstance(v, dict)


@pytest.mark.parametrize('collection', collections)
def test_decks_dict(collection):
    ankidirect = ankidirects[collection]

    k, v = list(ankidirect.decks_dict.items())[0]
    assert k.isdigit()
    assert isinstance(v, dict)


@pytest.mark.parametrize('collection', collections)
def test_notes(collection):
    ankidirect = ankidirects[collection]

    try:
        assert isinstance(next(ankidirect.notes), (dict, OrderedDict))
    except StopIteration:
        pass


@pytest.mark.parametrize('collection', collections)
def test_cards(collection):
    ankidirect = ankidirects[collection]

    try:
        assert isinstance(next(ankidirect.cards), (dict, OrderedDict))
    except StopIteration:
        pass


@pytest.mark.parametrize('collection', collections)
def test_data(collection):
    ankidirect = ankidirects[collection]

    for v in ankidirect.data.values():
        try:
            item_id, item_dict = list(v.items())[0]
            assert item_id.isdigit()
            assert isinstance(item_dict, (dict, OrderedDict))
        except IndexError as e:
            print(e)

    assert set(ankidirect.data.keys()) - {'models', 'decks', 'notes', 'cards'} == set()


@pytest.mark.parametrize('collection', collections)
def test_name_to_id(collection):
    ankidirect = ankidirects[collection]

    for v in ankidirect.name_to_id.values():
        try:
            item_name, item_ids = list(v.items())[0]
            assert isinstance(item_name, str)
            assert all([item_id.isdigit() for item_id in item_ids]) is True  # item_ids are actually digital strings.
        except IndexError as e:
            print(e)

    assert set(ankidirect.name_to_id.keys()) - {'models', 'decks'} == set()


@pytest.mark.parametrize('collection', collections)
@pytest.mark.parametrize('data_list, result', test_parameters['test_add_sequential'])
def test_add_sequential(collection,
                        data_list, result):
    with UniqueCollection(collection) as unique:
        for data in data_list:
            assert unique.ankidirect.add(data) == result


@pytest.mark.parametrize('collection', collections)
@pytest.mark.parametrize('data_list, result', test_parameters['test_verify_add_info'])
def test_verify_add_info(collection,
                         data_list, result):
    ankidirect = ankidirects[collection]

    assert ankidirect.verify.verify_add_info(data_list) == result


@pytest.mark.parametrize('collection', collections)
@pytest.mark.parametrize('data_list_add, data_verify, result',
                         test_parameters['test_verify_add_info_after_add'])
def test_verify_add_info_after_add(collection,
                                   data_list_add, data_verify, result):
    with UniqueCollection(collection) as unique:
        for data in data_list_add:
            unique.ankidirect.add(data)
        assert unique.ankidirect.verify.verify_add_info(data_verify) == result


class UniqueCollection:
    def __init__(self, collection):
        if collection is None:
            collection = get_collection_path()

        self.collection_path = next(tempfile._get_candidate_names())
        shutil.copy(src=collection, dst=self.collection_path)
        self.ankidirect = AnkiDirect(anki_database=self.collection_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.collection_path)
