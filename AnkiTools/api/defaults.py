import json
from collections import OrderedDict

from AnkiTools.tools.defaults import DEFAULT_API_PREFORMATTED_PAYLOAD


def get_default_payload(sample_params: dict,
                        add_note_template: dict=None,
                        preformatted_payload: str=str(DEFAULT_API_PREFORMATTED_PAYLOAD)):
    if add_note_template is None:
        add_note_template = dict()

    note_type = sample_params['note_type']

    assert isinstance(sample_params['data'], (dict, OrderedDict))
    headers = list(sample_params['data'].keys())
    contents = list(sample_params['data'].values())

    forward = add_note_template.get('forward', "Forward")
    backward = add_note_template.get('backward', "Backward")
    has_backward = add_note_template.get('has_backward', False)

    payload_str = preformatted_payload\
        .replace('\\\\' + 'note_type', note_type)\
        .replace('\\\\' + 'forward', forward)\
        .replace('\\\\' + 'backward', backward)

    for i, header in enumerate(headers):
        payload_str = payload_str.replace('\\\\' + 'header' + str(i), header)

    for i, content in enumerate(contents):
        payload_str = payload_str.replace('\\\\' + 'content' + str(i), content)

    payload = json.loads(payload_str, object_pairs_hook=OrderedDict)

    if not has_backward:
        payload['data'][note_type][0]['decks'].pop(backward)
        payload['definitions'][note_type]['templates'].pop()

    return payload
