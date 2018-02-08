import requests
import json


def POST(action, version=5, params={}):
    to_send = json.dumps({
        'action': action,
        'version': version,
        'params': params
    })

    r = requests.post('http://127.0.0.1:8765', data=to_send)
    return json.loads(r.text)['result']


if __name__ == '__main__':
    print(POST('deckNames'))