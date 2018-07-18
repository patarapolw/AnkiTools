import pyexcel_xlsx

import os
from collections import OrderedDict
import namedlist as nl
import simplejson as json
from simplejson.decoder import JSONDecodeError
import logging
from pathlib import Path

from AnkiTools.api.app import AnkiDirect
from AnkiTools.api.defaults import get_default_payload
from AnkiTools.tools.defaults import DEFAULT_API_MODEL_DEFINITION
from AnkiTools.serialize import EnumEncoder, enum_hook

from .export import ExcelExport
from .params import (AnkiTuple, CardsInDeckTuple, ModelTuple, TemplateTuple)

info_logger = logging.getLogger('info')
record_logger = logging.getLogger('record')
debugger_logger = logging.getLogger('debug')


class AnkiExcelSync:
    def __init__(self, excel_filename, anki_database, read_only: bool=False):
        """

        :param str|Path excel_filename:
        :param str|Path anki_database:
        :param read_only:
        """
        if not isinstance(excel_filename, Path):
            excel_filename = Path(excel_filename)

        self.anki_direct = AnkiDirect(anki_database=anki_database)
        self.excel_filename = excel_filename
        self.read_only = read_only

        if os.path.exists(excel_filename):
            self.data = self.load_from_excel
        else:
            self.data = AnkiTuple()
            self.load_from_anki_direct()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def load_from_anki_direct(self):
        # Getting card distribution
        cards_iter = self.anki_direct.cards
        notes_iter = self.anki_direct.notes
        decks_dict = OrderedDict(self.anki_direct.decks_dict_iter)
        models_dict = OrderedDict(self.anki_direct.models_dict_iter)

        note_id_to_model_id = dict()
        for note in notes_iter:
            note_id_to_model_id[str(note.id)] = note.mid

        for card in cards_iter:
            record = CardsInDeckTuple(
                card_id=card.id,
                note_id=card.nid,
                deck_name=decks_dict[str(card.did)].name,
                template_name=models_dict[str(note_id_to_model_id[str(card.nid)])].tmpls[card.ord].name,
                order=card.ord
            )
            self.data.decks[str(card.id)] = record

        for model_id, model_record in models_dict.items():
            sheet_name = model_dict['name']
            info_logger.info('Creating sheet {}'.format(sheet_name))

            # Writing header
            header = ['id']
            field_pairs = [(fld['ord'], fld['name']) for fld in model_dict['flds']]
            fields_list = [x[1] for x in sorted(field_pairs)]
            header.extend(fields_list)
            header.append('Tags')

            model_dict['header'] = header

            sample_params = {
                'note_type': sheet_name,
                'data': OrderedDict.fromkeys(fields_list, ''),
            }
            default_payload = get_default_payload(sample_params)
            templates_list = [TemplateTuple(name=template['name'],
                                            qfmt=template['data']['qfmt'],
                                            afmt=template['data']['afmt'])
                              for template in default_payload['definitions'][sheet_name]['templates']]

            self.data.models[str(model_id)] = ModelTuple(id=model_id,
                                                         name=model_dict['name'],
                                                         fields_list=fields_list,
                                                         templates_list=templates_list)

        # Getting sheet contents
        notes_iter = self.anki_direct.notes
        for note in notes_iter:
            sheet_name = models_dict[str(note['mid'])]['name']
            header = models_dict[str(note['mid'])]['header']

            # Writing record
            info_logger.info('Creating note {} - {}'.format(note['id'],
                                                        json.dumps(note['formatted_flds'], ensure_ascii=False)))

            record = [note['id']]
            record.extend(note['formatted_flds'])
            record.append(note['tags'])

            if sheet_name not in self.data.notes.keys():
                self.data.notes[sheet_name] = OrderedDict()

            self.data.notes[sheet_name][str(note['id'])] = OrderedDict(zip(header, record))

    @property
    def load_from_excel(self):
        raw = pyexcel_xlsx.get_data(str(self.excel_filename.absolute()))
        anki_tuple = AnkiTuple()

        if '.settings' in raw.keys():
            # Load params
            i = 0
            for i, row in enumerate(raw['.settings']):
                if not row or not row[0]:
                    break
                anki_tuple.params._replace(**{row[0]: self.load(row[1])})

            while not self.valid_row(raw['.settings'], i):
                i += 1

                if i > len(raw['.settings']):
                    break

            if raw['.settings'][i-1] and raw['.settings'][i-1][0] == '# Models':
                # Load models
                header = [header_item for header_item in raw['.settings'][i] if header_item]
                while self.valid_row(raw['.settings'], i):
                    # By default, zip is zip_shortest.
                    anki_tuple.models[raw['.settings'][i][0]] = ModelTuple(**dict(zip(header, raw['.settings'][i])))
                    i += 1

                while not self.valid_row(raw['.settings'], i):
                    i += 1

                    if i > len(raw['.settings']):
                        break

            # Load decks
            header = [header_item for header_item in raw['.settings'][i] if header_item]
            while self.valid_row(raw['.settings'], i):
                record = dict(zip(header, raw['.settings'][i]))
                anki_tuple.decks[raw['.settings'][i][0]] = CardsInDeckTuple(**record)
                i += 1

                if i >= len(raw['.settings']):
                    break

            raw.pop('.settings')

        # Load notes
        for note_type, values in raw.items():
            header = [to_camel_case(header_item) for header_item in raw[note_type][0]]
            note_type_record = nl.namedlist(to_camel_case(note_type), header, default='')
            i = 1
            while self.valid_row(raw[note_type], i):
                if note_type not in anki_tuple.notes.keys():
                    anki_tuple.notes[note_type] = OrderedDict()

                anki_tuple.notes[note_type][raw[note_type][i][0]] = note_type_record(**dict(zip(header, raw[note_type][i])))
                i += 1
                if i >= len(raw[note_type]):
                    break

        return anki_tuple

    def close(self):
        if not self.read_only:
            self.save()

    def save(self):
        ExcelExport(raw_excel_data=self.excel_raw,
                    out_file=self.excel_filename,
                    excel_formatting_file=self.excel_filename).save()

    @property
    def excel_raw(self):
        excel_raw = OrderedDict()

        # Create sheet ".settings" and append Params.
        excel_raw['.settings'] = list()
        for k, v in self.data.params._asdict().items():
            excel_raw['.settings'].append([k, self.dump(v)])

        excel_raw['.settings'].append([''])

        # Append Models to ".settings"
        source = self.data.models
        if len(source) > 0:
            model = list(source.values())[0]
            assert isinstance(model, ModelTuple)
            excel_raw['.settings'].append(['# Models'])
            excel_raw['.settings'].append(model._fields)

            for model in source.values():
                excel_raw['.settings'].append([self.dump(cell) for cell in model])

        excel_raw['.settings'].append([''])

        # Append Decks to ".settings"
        source = self.data.decks
        if len(source) > 0:
            deck = list(source.values())[0]
            assert isinstance(deck, CardsInDeckTuple)
            excel_raw['.settings'].append(['# Decks'])
            excel_raw['.settings'].append(deck._fields)

            for deck in source.values():
                excel_raw['.settings'].append([self.dump(cell) for cell in deck])

        excel_raw['.settings'].append([''])

        for note_type, note_dict in self.data.notes.items():
            # Check whether there is a item in this note_type.
            # If not, do not create the sheet.
            source = self.data.notes[note_type]
            if len(source) > 0:
                note = list(source.values())[0]
                excel_raw[note_type] = list()

                assert hasattr(note, '_asdict'), \
                    "Note {} is not of Record type.".format(note['id'])
                excel_raw[note_type].append(note._fields)

                for note in source.values():
                    assert hasattr(note, '_asdict'), \
                        "Note {} is not of Record type.".format(note['id'])

                    excel_raw[note_type].append([self.dump(cell) for cell in note])

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

        for sheet_name, records in self.data.notes.items():
            if records:
                payload['data'][sheet_name] = list()

                # This will further be "string-formatted", so it needs to be deep-copied.
                # Currently implemented using a ReadOnlyJsonObject object.
                payload['definitions'][sheet_name] = DEFAULT_API_MODEL_DEFINITION.to_json_object()

                random_record = records[list(records.keys())[0]]
                assert hasattr(random_record, '_asdict')
                header = random_record._fields

                payload['definitions'][sheet_name]['templates'][0]['data']['qfmt'] = \
                    payload['definitions'][sheet_name]['templates'][0]['data']['qfmt'] % header[0]
                payload['definitions'][sheet_name]['templates'][0]['data']['afmt'] = \
                    payload['definitions'][sheet_name]['templates'][0]['data']['afmt'] % header[1]

                for record in records.values():
                    formatted_record = {
                        'data': record._asdict(),
                        'decks': {
                            'Card 1': sheet_name
                        }
                    }

                    payload['data'][sheet_name].append(formatted_record)

        return payload

    @staticmethod
    def dump(cell):
        if isinstance(cell, int):
            return cell
        elif isinstance(cell, str):
            return cell.replace('\n', ' ')
        else:
            try:
                return json.dumps(cell, cls=EnumEncoder, ensure_ascii=False)
            except TypeError:
                return json.dumps(cell, cls=EnumEncoder)

    @staticmethod
    def load(cell):
        if isinstance(cell, str):
            try:
                return json.loads(cell, object_hook=enum_hook, object_pairs_hook=OrderedDict)
            except JSONDecodeError:
                pass

        return cell

    @staticmethod
    def valid_row(sheet, i):
        return i < len(sheet) and sheet[i] and sheet[i][0] and not str(sheet[i][0]).startswith('#')


def to_camel_case(unformatted: str):
    if unformatted == 'id':
        return unformatted
    else:
        return ''.join([fragment.title() for fragment in unformatted.replace('_', ' ').split(' ')])
