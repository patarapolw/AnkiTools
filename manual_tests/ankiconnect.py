from AnkiTools import AnkiConnect

if __name__ == '__main__':
    params = {'actions': [{'action': 'deckNames'}, {'action': 'browse', 'params': {'query': 'deck:current'}}]}
    print(AnkiConnect.post('multi', params=params))
