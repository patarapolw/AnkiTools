import os
import zipfile
import sqlite3
import json
import pprint


class readApkg:
    def __init__(self, path_to_file):
        with zipfile.ZipFile(path_to_file, 'r') as zp:
            zp.extract('collection.anki2', '.')

        with sqlite3.connect(os.path.join('collection.anki2')) as conn:
            cursor = conn.execute('SELECT models, decks FROM col')
            self.models = []
            self.decks = []
            for row in cursor:
                models = json.loads(row[0])
                for mid, v in models.items():
                    fieldnames = []
                    for flds in v['flds']:
                        fieldnames.append(flds['name'])
                    self.models.append({
                        'id': mid,
                        'name': v['name'],
                        'fields': fieldnames
                    })

                decks = json.loads(row[1])
                for did, v in decks.items():
                    self.decks.append({
                        'id': did,
                        'name': v['name']
                    })

            self.notes = []
            cursor = conn.execute('SELECT id, mid, flds FROM notes')
            for row in cursor:
                nid = str(row[0])
                mid = str(row[1])
                model_name = ''
                model_number = -1
                for model_number, model in enumerate(self.models):
                    if model['id'] == mid:
                        model_name = model['name']
                        break

                content = dict()
                for i, fieldcontent in enumerate(row[2].split('\x1f')):
                    content[self.models[model_number]['fields'][i]] = fieldcontent

                self.notes.append({
                    'id': nid,
                    'model_name': model_name,
                    'content': content
                })

            self.cards = []
            cursor = conn.execute('SELECT id, nid, did FROM cards')
            for row in cursor:
                cid = str(row[0])
                nid = str(row[1])
                note_content = []
                for note_number, note in enumerate(self.notes):
                    if note['id'] == nid:
                        note_content = note['content']
                        break

                did = str(row[2])
                deck_name = ''
                for deck in self.decks:
                    if deck['id'] == did:
                        deck_name = deck['name']
                        break

                self.cards.append({
                    'id': cid,
                    'note_id': nid,
                    'note_content': note_content,
                    'deck_id': did,
                    'deck_name': deck_name
                })

        os.remove('collection.anki2')

    def findNote(self, params):
        result = dict()
        for k, v in params.items():
            for note in self.notes:
                model_name = note['model_name']
                if note['content'][k] == v:
                    if model_name not in result.keys():
                        result[model_name] = [note['content']]
                    else:
                        result[model_name] += [note['content']]

        return result

    def findCard(self, params):
        pass


if __name__ == '__main__':
    os.chdir('.')

    anki = readApkg(os.path.join('sample','Chinese_Sentences_and_audio_spoon_fed.apkg'))
    print(pprint.pformat(anki.findNote({'Hanzi': '比起出门，我更喜欢待在家。'})))