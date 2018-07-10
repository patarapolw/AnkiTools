class AnkiContentVerify:
    def __init__(self, ids=None):
        if ids is None:
            ids = {
                'decks': dict()
            }
        self.ids = ids

    def missing_decks(self):
        deck_dirs = set()
        for deck in self.ids['decks'].values():
            deck_dirs.add(tuple(deck['name'].split('::')))

        new_deck_names = set()
        for deck_dir in deck_dirs:
            for i in range(1, len(deck_dir)):
                super_deck_dir = tuple(deck_dir[:i])
                if super_deck_dir not in deck_dirs:
                    new_deck_names.add('::'.join(super_deck_dir))

        return new_deck_names
