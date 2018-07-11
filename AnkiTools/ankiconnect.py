import requests
import requests.exceptions


class AnkiConnect:
    URL = 'http://127.0.0.1:8765'

    def __init__(self):
        # assert self.is_online(), \
        #     'AnkiConnect is not installed, or Anki app is not open.'  # Does not work with @staticmethod
        pass

    @staticmethod
    def post(action, params=None, version=6):
        """
        For the documentation, see https://foosoft.net/projects/anki-connect/

        :param str action:
        :param dict params:
        :param int version:
        :return:
        """
        if params is None:
            params = dict()
        to_send = {
            'action': action,
            'version': version,
            'params': params
        }

        r = requests.post(AnkiConnect.URL, json=to_send)
        return r.json()

    @staticmethod
    def is_online():
        try:
            requests.head(AnkiConnect.URL)
        except requests.exceptions.ConnectionError:
            return False

        return True
