import json

from AnkiTools import AnkiDirect


if __name__ == '__main__':
    with open('payload.json') as f:
        AnkiDirect().add(json.load(f))
