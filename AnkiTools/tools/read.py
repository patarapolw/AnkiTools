import os
import zipfile
import sqlite3
import json
import pprint
import shutil
from collections import OrderedDict

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
            cursor = conn.execute('SELECT id, mid, flds FROM notes')
            for row in cursor:
                nid = str(row[0])
                mid = str(row[1])
                content = row[2].split('\x1f')
                self.notes.append({
                    'nid': nid,
                    'mid': mid,
                    'content': content
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

    def searchModelById(self, mid):
        for model in self.models:
            if model['mid'] == mid:
                return model
        return dict()

    def searchFieldIdByMid(self, mid, fieldName):
        model = self.searchModelById(mid)
        return model['fields'].index(fieldName)

    def searchDeckById(self, did):
        for deck in self.decks:
            if deck['did'] == did:
                return deck
        return dict()

    def searchNoteById(self, nid):
        for note in self.notes:
            if note['nid'] == nid:
                return note
        return dict()

    def searchCardById(self, cid):
        for card in self.cards:
            if card['cid'] == cid:
                return card
        return dict()

    def findNotes(self, fieldName, value):
        results = []
        for note in self.notes:
            fieldId = self.searchFieldIdByMid(note['mid'], fieldName)
            if fieldId != -1:
                if note['content'][fieldId] == value:
                    result = {
                        'model name': '',
                        'content': OrderedDict(),
                    }

                    model = self.searchModelById(note['mid'])
                    result['model name'] = model['name']

                    fields = model['fields']
                    note = self.searchNoteById(note['nid'])
                    data = note['content']
                    for i, field in enumerate(fields):
                        result['content'][field] = data[i]

                    results.append(result)

        return results

    def findCards(self, fieldName, value):
        results = []
        for card in self.cards:
            note = self.searchNoteById(card['nid'])
            fieldId = self.searchFieldIdByMid(note['mid'], fieldName)
            if fieldId != -1:
                note = self.searchNoteById(card['nid'])
                if note['content'][fieldId] == value:
                    result = {
                        'deck name': '',
                        'model name': '',
                        'template': '',
                        'content': OrderedDict(),
                    }

                    deck = self.searchDeckById(card['did'])
                    result['deck name'] = deck['name']

                    model = self.searchModelById(note['mid'])
                    result['model name'] = model['name']

                    result['template'] = model['templates'][card['ord']]

                    fields = model['fields']
                    data = note['content']
                    for i, field in enumerate(fields):
                        result['content'][field] = data[i]

                    results.append(result)

        return results


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
    os.chdir('..')

    with readApkg(os.path.join('apkg','Chinese_Sentences_and_audio_spoon_fed.apkg')) as anki:
        print(pprint.pformat(anki.findNotes('Pinyin','Nǐ hǎo!')))
        print(pprint.pformat(anki.findCards('Pinyin', 'Nǐ hǎo!')))
