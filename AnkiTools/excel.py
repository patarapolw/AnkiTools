import pyexcel_export

from collections import OrderedDict, namedtuple
import json
import logging
from pathlib import Path
from datetime import datetime

from AnkiTools.api.app import AnkiDirect
from AnkiTools.tools.defaults import DEFAULT_API_MODEL_DEFINITION

CardTuple = namedtuple('CardTuple', ['card_id', 'note_id', 'deck_name', 'template_name', 'template_order'])


class AnkiExcelSync:
    def __init__(self, excel_filename: str, anki_database: str, read_only: bool=False):
        self.anki_direct = AnkiDirect(anki_database=anki_database)
        self.excel_filename = Path(excel_filename)
        self.read_only = read_only

        self.created = ''
        if self.excel_filename.exists():
            self.data = self.load_excel()
        else:
            self.data = self.new_data()
            self.load_anki_direct()
            self.created = datetime.now().isoformat()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def new_data(self):
        data = {
            '_models': dict(),
            '_decks': dict(),
            'data': OrderedDict()
        }

        return data

    def load_anki_direct(self):
        # Getting templates
        for model_id, model in self.anki_direct.models.items():
            field_pairs = [(fld['ord'], fld['name']) for fld in model['flds']]
            fields_list = [x[1] for x in sorted(field_pairs)]

            sample_params = {
                'note_type': model['name'],
                'data': OrderedDict.fromkeys(fields_list, ''),
            }

            templates_list = [[template['name'],
                               template['qfmt'],
                               template['afmt']]
                              for template in model['tmpls']]

            self.data['_models'][model_id] = OrderedDict(id=model_id,
                                                         name=model['name'],
                                                         fields_list=json.dumps(fields_list),
                                                         templates_list=templates_list)

        # Getting card distribution
        for card_id, card in self.anki_direct.cards.items():
            model_id = str(self.anki_direct.notes[str(card['nid'])]['mid'])

            record = CardTuple(
                card_id=card_id,
                note_id=card['nid'],
                deck_name=self.anki_direct.decks[str(card['did'])]['name'],
                template_name=self.anki_direct.models[model_id]['tmpls'][card['ord']]['name'],
                template_order=card['ord']
            )
            self.data['_decks'][str(card['id'])] = record._asdict()

        # Getting sheet names
        for model_id, model in self.anki_direct.models.items():
            sheet_name = model['name']
            logging.info('Creating sheet {}'.format(sheet_name))

            # Writing header
            header = ['id']
            field_pairs = [(fld['ord'], fld['name']) for fld in model['flds']]
            header.extend([x[1] for x in sorted(field_pairs)])
            header.append('Tags')

            model['header'] = header

        # Getting sheet contents
        for note_id, note in self.anki_direct.notes.items():
            sheet_name = self.anki_direct.models[str(note['mid'])]['name']
            header = self.anki_direct.models[str(note['mid'])]['header']

            # Writing record
            logging.info('Creating note {} - {}'.format(note_id,
                                                        json.dumps(note['formatted_flds'], ensure_ascii=False)))

            record = [note_id]
            record.extend(note['formatted_flds'])
            record.append(note['tags'])
            self.data['data'].setdefault(sheet_name, dict())[note_id] = OrderedDict(zip(header, record))

    # def load_excel(self):
    #     data = dict()
    #     raw, _ = pyexcel_export.get_data(self.excel_filename)
    #
    #     data['meta'] = dict()
    #     try:
    #         data['meta']['meta'] = OrderedDict()
    #         i = 0
    #         for row in raw['_meta']:
    #             i += 1
    #             if not row or not row[0]:
    #                 break
    #
    #             data['meta']['meta'][row[0]] = row[1]
    #
    #         j = 0
    #         for row in raw['_meta'][i:]:
    #             if not row:
    #                 break
    #             while not row[0]:
    #                 continue
    #             j += 1
    #
    #         header, *records = raw['_meta'][i+j:]
    #
    #     except (KeyError, IndexError) as e:
    #         print(e)
    #
    #     try:
    #         data['meta']['decks'] = dict()
    #         header, *records = raw.pop(self.SHEET_DECKS)
    #         for record in records:
    #             data['meta'][self.SHEET_DECKS][record[0]] = OrderedDict(zip(header, record))
    #     except (KeyError, IndexError) as e:
    #         print(e)
    #
    #     data['data'] = OrderedDict()
    #     for note_type, values in raw.items():
    #         header, *records = values
    #         data['data'][note_type] = dict()
    #         for record in records:
    #             data['data'][note_type][record[0]] = OrderedDict(zip(header, record))
    #
    #     return data

    def close(self):
        # if not self.read_only:
        #     self.save()
        pass

    def save(self):
        pyexcel_export.save_data(self.excel_filename, data=self.excel_raw, retain_meta=True,
                                 created=self.created, modified=datetime.now().isoformat())

    @property
    def excel_raw(self):
        excel_raw = OrderedDict()

        # Create sheet _templates
        source = self.data['_models']
        excel_raw['_models'] = [['id', 'name', 'fields', 'template_name', 'qfmt', 'afmt']]

        for v in source.values():
            for v2 in v['templates_list']:
                record = list(v.values())[:-1]
                record.extend(v2)
                excel_raw['_models'].append(record)

        # Create sheet _decks
        source = self.data['_decks']

        v = source[list(source.keys())[0]]
        assert isinstance(v, (dict, OrderedDict))

        excel_raw['_decks'] = list()
        excel_raw['_decks'].append(list(v.keys()))

        for v in source.values():
            assert isinstance(v, (dict, OrderedDict))
            excel_raw['_decks'].append([str(x) for x in v.values()])

        for note_type, v in self.data['data'].items():
            # Check whether there is a item in this note_type.
            # If not, do not create the sheet.
            source = self.data['data'][note_type]

            try:
                v2 = source[list(source.keys())[0]]
            except IndexError:
                continue

            # Create sheet
            excel_raw[note_type] = list()

            assert isinstance(v2, (dict, OrderedDict))
            excel_raw[note_type].append(list(v2.keys()))

            for v2 in source.values():
                assert isinstance(v2, (dict, OrderedDict))
                excel_raw[note_type].append([str(x) for x in v2.values()])

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
