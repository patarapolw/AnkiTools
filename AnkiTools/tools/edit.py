import os
import zipfile
import sqlite3
import json
import shutil

from AnkiTools.tools import const, read, create


class editAnki2:
    def __init__(self, path_to_file, output=''):
        if output != '':
            self.output = output
        else:
            self.output = path_to_file

        self.anki2 = path_to_file
        self.db = read.readAnki2(path_to_file)

    def updateModels(self, models):
        with sqlite3.connect(self.anki2) as conn:
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
        with sqlite3.connect(self.anki2) as conn:
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
        with sqlite3.connect(self.anki2) as conn:
            for note in notes:
                cursor = conn.execute('SELECT * FROM notes WHERE id=?', (note['nid'], ))
                if cursor.fetchone() is None:
                    conn.executemany('INSERT INTO notes VALUES (?)', create.newNote(note))
                else:
                    conn.execute('UPDATE notes SET mid=?, flds=?, tags=? WHERE id=?',
                                 (note['mid'], note['content'].join('\x1f'), note['tags'].join(' '),
                                  note['nid']))

    def updateCards(self, cards):
        with sqlite3.connect(self.anki2) as conn:
            for card in cards:
                cursor = conn.execute('SELECT * FROM notes WHERE id=?', (card['id'],))
                if cursor.fetchone() is None:
                    conn.executemany('INSERT INTO notes VALUES (?)', create.newCard(card))
                else:
                    conn.execute('UPDATE cards SET nid=?, did=?, ord=? WHERE id=?',
                                 (card['nid'], card['did'], card['ord'], card['cid']))

    def updateCardQueries(self, cardQueries):
        with sqlite3.connect(self.anki2) as conn:
            for cardQuery in cardQueries:
                note = cardQuery.pop('note')
                deck = cardQuery.pop('deck')
                cardQuery['nid'] = note['nid']
                cardQuery['did'] = deck['did']
                self.updateNotes([note])
                self.updateDecks([deck])
                self.updateCards([cardQuery])

    def export(self, output=''):
        if output == '':
            output = os.path.splitext(self.output)[0] + '.apkg'
        with zipfile.ZipFile(output, 'w') as zp:
            zp.write(self.anki2)


class editApkg(editAnki2):
    def __init__(self, path_to_file, output=''):
        with zipfile.ZipFile(path_to_file, 'r') as zp:
            zp.extractall(const.temp_dir)
        self.path_to_file = os.path.join(const.temp_dir, const.database)

        super().__init__(self.path_to_file, output)

    def close(self, output=''):
        self.save()
        shutil.rmtree(const.temp_dir)

    def save(self, output=''):
        if output == '':
            output = self.path_to_file
        with zipfile.ZipFile(self.output, 'w') as zp:
            for root, dirs, files in os.walk(const.temp_dir):
                for filename in files:
                    zp.write(os.path.join(root, filename))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
