import requests
import requests.exceptions


class AnkiConnect:
    URL = 'http://127.0.0.1:8765'

    @staticmethod
    def post(action, version=6, params=None):
        """
        For the documentation, see https://foosoft.net/projects/anki-connect/

        :param action:
        :param version:
        :param params:
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


if __name__ == '__main__':
    print(AnkiConnect.is_online())
