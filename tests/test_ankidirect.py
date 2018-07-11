import pytest
import os
import shutil
from collections import OrderedDict
import json
from uuid import uuid4

from .dir import parameters_path

from AnkiTools import AnkiDirect
from AnkiTools.tools.path import get_collection_path

with open(parameters_path('test_parameters.json')) as f:
    test_parameters = json.load(f, object_pairs_hook=OrderedDict)['test_ankidirect']


clean_collection_path = parameters_path('clean_collection.anki2')
clean_ankidirect = AnkiDirect(anki_database=clean_collection_path)

collection_path = parameters_path('collection.anki2')
ankidirect = AnkiDirect(anki_database=collection_path)


@pytest.mark.skipif(os.getenv('ANKI_APP_OPENED', '0') == '1',
                    reason='AnkiDirect() (no args) requires Anki to be closed.')
class TestAnkiDirectNoArgs:
    @pytest.mark.parametrize('is_clean', [(True,), (False,)])
    def test_models_dict(self, is_clean):
        if is_clean:
            ankidirect = clean_ankidirect

        k, v = list(ankidirect.models_dict.items())[0]
        assert k.isdigit()
        assert isinstance(v, dict)

    @pytest.mark.parametrize('is_clean', [(True,), (False,)])
    def test_decks_dict(self, is_clean):
        if is_clean:
            ankidirect = clean_ankidirect

        k, v = list(ankidirect.decks_dict.items())[0]
        assert k.isdigit()
        assert isinstance(v, dict)

    @pytest.mark.parametrize('is_clean', [(True,), (False,)])
    def test_notes(self, is_clean):
        if is_clean:
            ankidirect = clean_ankidirect

        try:
            assert isinstance(next(ankidirect.notes), (dict, OrderedDict))
        except StopIteration:
            pass

    @pytest.mark.parametrize('is_clean', [(True,), (False,)])
    def test_cards(self, is_clean):
        if is_clean:
            ankidirect = clean_ankidirect

        try:
            assert isinstance(next(ankidirect.cards), (dict, OrderedDict))
        except StopIteration:
            pass

    @pytest.mark.parametrize('is_clean', [(True,), (False,)])
    def test_data(self, is_clean):
        if is_clean:
            ankidirect = clean_ankidirect

        for v in ankidirect.data.values():
            try:
                item_id, item_dict = list(v.items())[0]
                assert item_id.isdigit()
                assert isinstance(item_dict, (dict, OrderedDict))
            except IndexError as e:
                print(e)

        assert set(ankidirect.data.keys()) - {'models', 'decks', 'notes', 'cards'} == set()

    @pytest.mark.parametrize('is_clean', [(True,), (False,)])
    def test_name_to_id(self, is_clean):
        if is_clean:
            ankidirect = clean_ankidirect

        for v in ankidirect.name_to_id.values():
            try:
                item_name, item_ids = list(v.items())[0]
                assert isinstance(item_name, str)
                print(all([isinstance(item_id, int) for item_id in item_ids]))
            except IndexError as e:
                print(e)

        assert set(ankidirect.name_to_id.keys()) - {'models', 'decks'} == set()

    @pytest.mark.parametrize('is_clean', [(True,), (False,)])
    @pytest.mark.parametrize('data_list, result', test_parameters['TestAnkiDirectNoArgs']['test_add_sequential'])
    def test_add_sequential(self, data_list, result, is_clean):
        if is_clean:
            ankidirect = clean_ankidirect

        with UniqueCollectionData(is_clean) as unique:
            for data in data_list:
                assert unique.ankidirect.add(data) == result

    @pytest.mark.parametrize('is_clean', [(True,), (False,)])
    @pytest.mark.parametrize('data_list, result', test_parameters['TestAnkiDirectNoArgs']['test_verify_add_info'])
    def test_verify_add_info(self, data_list, result, is_clean):
        assert ankidirect.verify.verify_add_info(data_list) == result

    @pytest.mark.parametrize('is_clean', [(True,), (False,)])
    @pytest.mark.parametrize('data_list_add, data_verify, result',
                             test_parameters['TestAnkiDirectNoArgs']['test_verify_add_info_after_add'])
    def test_verify_add_info_after_add(self, data_list_add, data_verify, result, is_clean):
        with UniqueCollectionData(is_clean) as unique:
            for data in data_list_add:
                unique.ankidirect.add(data)
            assert unique.ankidirect.verify.verify_add_info(data_verify) == result


class UniqueCollectionData:
    def __init__(self, is_clean):
        if is_clean:
            path = clean_collection_path
        else:
            path = collection_path

        self.collection_path = '{}{}'.format(path, uuid4())
        shutil.copy(src=path, dst=self.collection_path)
        self.ankidirect = AnkiDirect(anki_database=self.collection_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.collection_path)
