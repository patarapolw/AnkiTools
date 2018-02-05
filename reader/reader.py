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
            cursor = conn.execute('SELECT models FROM col')
            self.models = []
            for i, row in enumerate(cursor):
                models = json.loads(row[0])

                for k,v in models.items():
                    fieldnames = []
                    for flds in v['flds']:
                        fieldnames.append(flds['name'])
                    model = {
                        'mid': k,
                        'name': v['name'],
                        'fields': fieldnames
                    }
                self.models.append(model)

            self.notes = dict()
            cursor = conn.execute('SELECT mid, flds FROM notes')
            for row in cursor:
                mid = str(row[0])
                for model_number, model in enumerate(self.models):
                    if model['mid'] == mid:
                        model_name = model['name']
                        break

                content = dict()
                for i, fieldcontent in enumerate(row[1].split('\x1f')):
                    content[self.models[model_number]['fields'][i]] = fieldcontent

                if model_name not in self.notes.keys():
                    self.notes[model_name] = [content]
                else:
                    self.notes[model_name] += [content]

            self.cards = dict()
            cursor = conn.execute('SELECT mid, flds FROM notes')
            for row in cursor:
                mid = str(row[0])
                for model_number, model in enumerate(self.models):
                    if model['mid'] == mid:
                        model_name = model['name']
                        break

                content = dict()
                for i, fieldcontent in enumerate(row[1].split('\x1f')):
                    content[self.models[model_number]['fields'][i]] = fieldcontent

                if model_name not in self.data.keys():
                    self.data[model_name] = [content]
                else:
                    self.data[model_name] += [content]

        os.remove('collection.anki2')

    def findNote(self, params):
        result = dict()
        for k, v in params.items():
            for model_name, records in self.notes.items():
                for record in records:
                    if record[k] == v:
                        if model_name not in result.keys():
                            result[model_name] = [record]
                        else:
                            result[model_name] += [record]

        return result


if __name__ == '__main__':
    os.chdir('.')

    anki = readApkg(os.path.join('sample','Chinese_Sentences_and_audio_spoon_fed.apkg'))
    print(pprint.pformat(anki.findNote({'Hanzi': '比起出门，我更喜欢待在家。'})))