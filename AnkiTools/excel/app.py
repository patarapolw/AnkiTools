import pyexcel_xlsx

from tempfile import mkdtemp, mktemp
import os
from collections import OrderedDict, namedtuple
from datetime import datetime
import json
import logging

from AnkiTools.api.ankidirect import AnkiDirect
from AnkiTools.tools.defaults import DEFAULT_API_MODEL_DEFINITION

from .formatter import ExcelFormatter

CardTuple = namedtuple('CardTuple', ['card_id', 'note_id', 'deck_name', 'template_order'])


class AnkiExcelSync:
    SHEET_SETTINGS = '.settings'
    SHEET_DECKS = '.decks'

    def __init__(self, excel_filename: str, anki_database: str, read_only: bool=False):
        self.anki_direct = AnkiDirect(anki_database=anki_database)
        self.excel_filename = excel_filename
        self.read_only = read_only

        if os.path.exists(excel_filename):
            self.data = self.load_excel()
        else:
            self.data = self.new_data()
            self.load_anki_direct()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def new_data(self):
        timestamp = datetime.fromtimestamp(datetime.now().timestamp()).isoformat()
        data = {
            'meta': {
                self.SHEET_SETTINGS: OrderedDict([
                    ('Created', timestamp),
                    ('Modified', timestamp)
                ]),
                self.SHEET_DECKS: dict()
            },
            'data': OrderedDict()
        }

        return data

    def load_anki_direct(self):
        # Getting card distribution
        cards_iter = self.anki_direct.cards
        decks_dict = self.anki_direct.decks_dict
        for card in cards_iter:
            record = CardTuple(
                card_id=card['id'],
                note_id=card['nid'],
                deck_name=decks_dict[str(card['did'])]['name'],
                template_order=card['ord']
            )
            self.data['meta'][self.SHEET_DECKS][str(card['id'])] = record._asdict()

        # Getting sheet names
        models = self.anki_direct.models_dict

        for model_id, model_dict in models.items():
            sheet_name = model_dict['name']
            logging.info('Creating sheet {}'.format(sheet_name))

            # Writing header
            header = ['id']
            field_pairs = [(fld['ord'], fld['name']) for fld in model_dict['flds']]
            header.extend([x[1] for x in sorted(field_pairs)])
            header.append('Tags')

            model_dict['header'] = header

        # Getting sheet contents
        notes_iter = self.anki_direct.notes
        for note in notes_iter:
            sheet_name = models[str(note['mid'])]['name']
            header = models[str(note['mid'])]['header']

            # Writing record
            logging.info('Creating note {} - {}'.format(note['id'],
                                                        json.dumps(note['formatted_flds'], ensure_ascii=False)))

            record = [note['id']]
            record.extend(note['formatted_flds'])
            record.append(note['tags'])
            self.data['data'].setdefault(sheet_name, dict())[str(note['id'])] = OrderedDict(zip(header, record))

    def load_excel(self):
        data = dict()
        raw = pyexcel_xlsx.get_data(self.excel_filename)

        data['meta'] = dict()
        try:
            data['meta'][self.SHEET_SETTINGS] = OrderedDict()
            for row in raw.pop(self.SHEET_SETTINGS):
                data['meta'][self.SHEET_SETTINGS][row[0]] = row[1]
        except (KeyError, IndexError) as e:
            print(e)

        try:
            data['meta'][self.SHEET_DECKS] = dict()
            header, *records = raw.pop(self.SHEET_DECKS)
            for record in records:
                data['meta'][self.SHEET_DECKS][record[0]] = OrderedDict(zip(header, record))
        except (KeyError, IndexError) as e:
            print(e)

        data['data'] = OrderedDict()
        for note_type, values in raw.items():
            header, *records = values
            data['data'][note_type] = dict()
            for record in records:
                data['data'][note_type][record[0]] = OrderedDict(zip(header, record))

        return data

    def close(self):
        if not self.read_only:
            self.save()

    def save(self, formatted=False):
        if formatted:
            temp_filename = os.path.join(mkdtemp(), mktemp(suffix='.xlsx'))
            pyexcel_xlsx.save_data(temp_filename, self.excel_raw)
            formatter = ExcelFormatter(excel_data_file=temp_filename,
                                       excel_formatting_file=self.excel_filename,
                                       out_file=self.excel_filename)
            formatter.do_formatting()
            formatter.save()
        else:
            pyexcel_xlsx.save_data(self.excel_filename, self.excel_raw)

    @property
    def excel_raw(self):
        excel_raw = OrderedDict()

        # Create sheet self.SHEET_SETTINGS
        excel_raw[self.SHEET_SETTINGS] = list()
        for k, v in self.data['meta'][self.SHEET_SETTINGS].items():
            assert isinstance(v, str)
            excel_raw[self.SHEET_SETTINGS].append([k, v])
        excel_raw[self.SHEET_SETTINGS].append([''])

        # Create sheet self.SHEET_DECKS
        excel_raw[self.SHEET_DECKS] = list()
        source = self.data['meta'][self.SHEET_DECKS]

        v = source[list(source.keys())[0]]
        assert isinstance(v, (dict, OrderedDict))
        excel_raw[self.SHEET_DECKS].append(list(v.keys()))

        for v in source.values():
            assert isinstance(v, (dict, OrderedDict))
            excel_raw[self.SHEET_DECKS].append(list(v.values()))

        for note_type, v in self.data['data'].items():
            # Check whether there is a item in this note_type.
            # If not, do not create the sheet.
            try:
                v2 = source[list(source.keys())[0]]
            except IndexError:
                continue

            # Create sheet
            excel_raw[note_type] = list()
            source = self.data['data'][note_type]

            assert isinstance(v2, (dict, OrderedDict))
            excel_raw[note_type].append(list(v2.keys()))

            for v2 in source.values():
                assert isinstance(v2, (dict, OrderedDict))
                excel_raw[note_type].append(list(v2.values()))

        return excel_raw

    def to_excel(self):
        self.save()

    def to_sqlite(self):
        self.anki_direct.add(self.to_payload())

    def to_payload(self):
        payload = {
            'data': dict(),
            'definitions': dict()
        }

        for sheet_name, records in self.data['data'].items():
            if records:
                payload['data'][sheet_name] = list()

                # This will further be "string-formatted", so it needs to be deep-copied.
                # Currently implemented using a ReadOnlyJsonObject object.
                payload['definitions'][sheet_name] = DEFAULT_API_MODEL_DEFINITION.to_json_object()
                random_record = records[list(records.keys())[0]]
                assert isinstance(random_record, (dict, OrderedDict))
                header = list(random_record.keys())

                payload['definitions'][sheet_name]['templates'][0]['data']['qfmt'] = \
                    payload['definitions'][sheet_name]['templates'][0]['data']['qfmt'] % header[0]
                payload['definitions'][sheet_name]['templates'][0]['data']['afmt'] = \
                    payload['definitions'][sheet_name]['templates'][0]['data']['afmt'] % header[1]

                for record in records.values():
                    formatted_record = {
                        'data': record,
                        'decks': {
                            'Card 1': sheet_name
                        }
                    }

                    payload['data'][sheet_name].append(formatted_record)

        return payload
