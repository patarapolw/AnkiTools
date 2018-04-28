import requests
import json


def POST(action, version=5, params=None):
    """
    For the documentation, see https://foosoft.net/projects/anki-connect/
    
    :param action:
    :param version:
    :param params:
    :return:
    """
    if params is None:
        params = dict()
    to_send = json.dumps({
        'action': action,
        'version': version,
        'params': params
    })

    r = requests.post('http://127.0.0.1:8765', data=to_send)
    return json.loads(r.text)
