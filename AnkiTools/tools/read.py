import os
import zipfile
import sqlite3
import json
import pprint
import shutil
from collections import OrderedDict
import re

from AnkiTools.tools import const


class readAnki2:
    def __init__(self, path_to_file):
        with sqlite3.connect(path_to_file) as conn:
            cursor = conn.execute('SELECT models, decks FROM col')
            self.models = []
            self.decks = []
            for row in cursor:
                models = json.loads(row[0])
                for mid, v in models.items():
                    fieldNames = []
                    for flds in v['flds']:
                        fieldNames.append(flds['name'])

                    templateNames = []
                    for tmpls in v['tmpls']:
                        templateNames.append(tmpls['name'])

                    self.models.append({
                        'mid': mid,
                        'name': v['name'],
                        'fields': fieldNames,
                        'templates': templateNames

                    })

                decks = json.loads(row[1])
                for did, v in decks.items():
                    self.decks.append({
                        'did': did,
                        'name': v['name']
                    })

            self.notes = []
            cursor = conn.execute('SELECT id, mid, flds, tags FROM notes')
            for row in cursor:
                nid = str(row[0])
                mid = str(row[1])
                content = row[2].split('\x1f')
                tags = row[3].split(' ')
                self.notes.append({
                    'nid': nid,
                    'mid': mid,
                    'content': content,
                    'tags': tags
                })

            self.cards = []
            cursor = conn.execute('SELECT id, nid, did, ord FROM cards')
            for row in cursor:
                cid = str(row[0])
                nid = str(row[1])
                did = str(row[2])
                ord = row[3]
                self.cards.append({
                    'cid': cid,
                    'nid': nid,
                    'did': did,
                    'ord': ord
                })

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def loadQuery(self):
        self.cardQuery = []
        for card in self.cards:
            query = {
                'cid': card['cid'],
                'note': self.nidToNote(card['nid']),
                'deck': self.didToDeck(card['did']),
                'ord': card['ord'],
            }
            query['model'] = self.midToModel(query['note']['mid'])
            self.cardQuery.append(query)

    def nidToNote(self, nid):
        for note in self.notes:
            if nid == note['nid']:
                return note
        return dict()

    def didToDeck(self, did):
        for deck in self.decks:
            if did == deck['did']:
                return deck
        return dict()

    def midToModel(self, mid):
        for model in self.models:
            if model['mid'] == mid:
                return model
        return dict()

    def cidToCard(self, cid):
        for card in self.cards:
            if card['cid'] == cid:
                return card
        return dict()

    def searchFieldIdByMid(self, mid, fieldName):
        model = self.midToModel(mid)
        return model['fields'].index(fieldName)

    def getDecks(self, regex):
        for deck in self.decks:
            if re.match(regex, deck['name']) is not None:
                yield deck

    def getNotesByField(self, model_id, field_number, regex):
        for note in self.notes:
            if note['mid'] == model_id:
                if re.match(regex, note['content'][field_number]) is not None:
                    yield note

    def getCardQuery(self, regex, params):
        for cardQuery in self.cardQuery:
            query = cardQuery[params['type']][params['key']]
            if type(query) is list:
                query = cardQuery[params['type']][params['key']][params['i']]
            if re.match(regex, query) is not None:
                yield cardQuery


class readApkg(readAnki2):
    def __init__(self, path_to_file):
        with zipfile.ZipFile(path_to_file, 'r') as zp:
            zp.extract(const.database, const.temp_dir)

        path_to_file = os.path.join(const.temp_dir, const.database)
        super().__init__(path_to_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        shutil.rmtree(const.temp_dir)


if __name__ == '__main__':
    pass
