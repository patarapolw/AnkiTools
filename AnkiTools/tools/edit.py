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
            cursor = conn.execute('SELECT models FROM col')
            editor = json.loads(list(cursor)[0][0])
            for model in models:
                model.setdefault('mid', create.intTime(1000))
                try:
                    editor[model['mid']]['name'] = model['name']
                    for i, field in enumerate(model['fields']):
                        try:
                            editor[model['mid']]['flds'][i]['name'] = field
                        except IndexError:
                            editor[model['mid']]['flds'].append(create.newField(field))
                    for i, template in enumerate(model['templates']):
                        try:
                            editor[model['mid']]['tmpls'][i]['name'] = template
                        except IndexError:
                            editor[model['mid']]['tmpls'].append(create.newTemplate(template))
                except KeyError:
                    editor[model['mid']] = create.newModel(model)

            full_models = json.dumps(editor)
            conn.execute('UPDATE col SET models=?', (full_models, ))

    def updateDecks(self, decks):
        with sqlite3.connect(self.anki2) as conn:
            cursor = conn.execute('SELECT decks FROM col')
            editor = json.loads(list(cursor)[0][0])
            for deck in decks:
                deck.setdefault('did', create.intTime(1000))
                try:
                    editor[deck['did']]['name'] = deck['name']
                except KeyError:
                    editor[deck['did']] = create.newDeck(deck)

            full_decks = json.dumps(editor)
            conn.execute('UPDATE col SET decks=?', (full_decks, ))

    def updateNotes(self, notes):
        with sqlite3.connect(self.anki2) as conn:
            for note in notes:
                note.setdefault('nid', create.intTime(1000))
                # mid must be supplied, otherwise, use updateCardQueries
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
                card.setdefault('cid', create.intTime(1000))
                card.setdefault('ord', 0)
                # nid, did must be supplied, otherwise, use updateCardQueries
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
                model = cardQuery.pop('model')

                note.setdefault('nid', create.intTime(1000))
                cardQuery['nid'] = note['nid']
                deck.setdefault('did', create.intTime(1000))
                cardQuery['did'] = deck['did']

                model.setdefault('mid', create.intTime(1000))
                note['mid'] = model['mid']

                self.updateNotes([note])
                self.updateDecks([deck])
                self.updateModels([model])
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
        with zipfile.ZipFile(output, 'w') as zp:
            for root, dirs, files in os.walk(const.temp_dir):
                for filename in files:
                    zp.write(os.path.join(root, filename))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
