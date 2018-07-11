import pytest
import os

from AnkiTools import AnkiConnect


def test_online():
    if os.getenv('ANKI_APP_OPENED', '0') == '1' and os.getenv('ANKICONNECT_INSTALLED', '0') == '1':
        assert AnkiConnect.is_online() is True
    else:
        assert AnkiConnect.is_online() is False


@pytest.mark.skipif(not (os.getenv('ANKI_APP_OPENED', '0') == '1' and os.getenv('ANKICONNECT_INSTALLED', '0') == '1'),
                    reason='AnkiConnect not online.')
@pytest.mark.parametrize('action_params_version, result, error', [
    (('version', ), int, None),
    (('version', dict(), 5), int, None),
    (('multi',
      {'actions': [{'action': 'deckNames'}, {'action': 'browse', 'params': {'query': 'deck:current'}}]}
      ), list, None),
    (('multi',
      {'actions': [{'action': 'deckNames'}, {'action': 'browse', 'params': {'query': 'deck:current'}}]},
      5), list, None)
])
def test_post(action_params_version, result, error):
    response = AnkiConnect.post(*action_params_version)

    if isinstance(result, type):
        assert type(response['result']) == result
    else:
        assert response['result'] == result

    assert response['error'] == error
