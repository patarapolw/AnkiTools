import os
import zipfile
import sqlite3
import json
import shutil

from tools import const, create, read


class editApkg:
    def __init__(self, path_to_file, output=''):
        with zipfile.ZipFile(path_to_file, 'r') as zp:
            zp.extractall(const.temp_dir)
        if output != '':
            self.output = output
        else:
            self.output = path_to_file

        self.db = read.readApkg(path_to_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.save()
        shutil.rmtree(const.temp_dir)

    def save(self, output=''):
        if output != '':
            self.output = output
        with zipfile.ZipFile(self.output, 'w') as zp:
            for root, dirs, files in os.walk(const.temp_dir):
                for filename in files:
                    zp.write(os.path.join(root, filename))

    def updateModels(self, models):
        with sqlite3.connect(const.database_path) as conn:
            for model in models:
                cursor = conn.execute('SELECT models FROM col')
                editor = json.loads(list(cursor)[0][0])
                editor[models['mid']]['name'] = model['name']

                for i, field in enumerate(model['fields']):
                    try:
                        editor[models['mid']]['flds'][i]['name'] = field
                    except KeyError:
                        editor[models['mid']] = create.newModel(model)

                for i, template in enumerate(model['templates']):
                    try:
                        editor[models['mid']]['tmpls'][i]['name'] = template
                    except KeyError:
                        editor[models['mid']] = create.newModel(model)

                full_model = json.dumps(editor)
                conn.execute('UPDATE col SET models=?', (full_model, ))

    def updateDecks(self, decks):
        with sqlite3.connect(const.database_path) as conn:
            for deck in decks:
                cursor = conn.execute('SELECT decks FROM col')
                editor = json.loads(list(cursor)[0][0])
                try:
                    editor[deck['did']]['name'] = deck['name']
                except KeyError:
                    editor[deck['did']] = create.newDeck(deck)

                full_deck = json.dumps(editor)
                conn.execute('UPDATE col SET decks=?', (full_deck, ))

    def updateNotes(self, notes):
        with sqlite3.connect(const.database_path) as conn:
            for note in notes:
                cursor = conn.execute('SELECT * FROM notes WHERE id=?', (note['nid'], ))
                if cursor.fetchone() is None:
                    conn.executemany('INSERT INTO notes VALUES (?)', create.newNote(note))
                else:
                    conn.execute('UPDATE notes SET mid=?, flds=? WHERE id=?',
                                 (note['mid'], note['content'].join('\x1f'), note['nid']))


    def updateCards(self, cards):
        with sqlite3.connect(const.database_path) as conn:
            for card in cards:
                cursor = conn.execute('SELECT * FROM notes WHERE id=?', (card['id'],))
                if cursor.fetchone() is None:
                    conn.executemany('INSERT INTO notes VALUES (?)', create.newCard(card))
                else:
                    conn.execute('UPDATE cards SET nid=?, did=?, ord=? WHERE id=?',
                                 (card['nid'], card['did'], card['ord'], card['cid']))

    def updateHumanNotes(self, humanNotes):
        for humanNote in humanNotes:
            model_name = humanNote['model name']
            fields, data = self.contentToFieldsAndData(humanNote['content'])

            mid = self.checkModels(model_name, fields)
            self.checkNotes(mid, fields, data)

    def updateHumanCards(self, humanCards):
        for humanCard in humanCards:
            deck_name = humanCard['deck name']
            model_name = humanCard['model name']
            template_name = humanCard['template']
            fields, data = self.contentToFieldsAndData(humanCard['content'])

            mid = self.checkModels(model_name, fields, template_name)
            self.checkNotes(mid, fields, data, template_name)

    def inPreExistingData(self, mid, data):
        for note in self.db.notes:
            if note['mid'] == mid:
                note['content'] = data
                return True
        return False

    @staticmethod
    def contentToFieldsAndData(content):
        fields = []
        data = []
        for field, datum in content.items():
            fields.append(field)
            data.append(datum)

        return fields, data

    def checkModels(self, model_name, fields, templateName=''):
        for dbModel in self.db.models:
            if dbModel['name'] == model_name:
                mid = dbModel['mid']
                return mid

        mid = create.intTime(1000)
        if templateName == '':
            templateName = 'Card1'
        self.db.models.append({
            'mid': mid,
            'name': model_name,
            'fields': fields,
            'templates': [templateName]
        })

        return mid

    def checkNotes(self, mid, fields, data, templateName='Card1'):
        if mid == None:
            mid = create.intTime(1000)
        if not self.inPreExistingData(mid, data):
            self.checkModels(self.midToModelName(mid), fields, templateName)
            self.db.notes.append({
                'nid': create.intTime(),
                'mid': mid,
                'contents': data
            })

    def midToModelName(self, mid):
        for model in self.db.models:
            print(model)
            if model['mid'] == mid:
                return model['name']
        return ''
