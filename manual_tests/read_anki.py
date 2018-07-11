from AnkiTools import AnkiDirect


def get_data():
    with AnkiDirect() as api:
        data = api.data

    return data


def get_notes(limit=10):
    with AnkiDirect() as api:
        data = list(api.notes)[:limit]

    return data


def get_cards(limit=10):
    with AnkiDirect() as api:
        data = list(api.cards)[:limit]

    return data


def get_models():
    with AnkiDirect() as api:
        data = api.models_dict

    return data


def get_decks():
    with AnkiDirect() as api:
        data = api.decks_dict

    return data


if __name__ == '__main__':
    print(get_decks())
