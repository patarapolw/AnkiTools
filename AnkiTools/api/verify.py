class AnkiContentVerify:
    def __init__(self, anki_content):
        self.anki_content = anki_content

    def missing_decks(self):
        deck_dirs = set()
        for deck in self.anki_content['decks'].values():
            deck_dirs.add(tuple(deck['name'].split('::')))

        new_deck_names = set()
        for deck_dir in deck_dirs:
            for i in range(1, len(deck_dir)):
                super_deck_dir = tuple(deck_dir[:i])
                if super_deck_dir not in deck_dirs:
                    new_deck_names.add('::'.join(super_deck_dir))

        return new_deck_names

    def get_model_id(self, model_name):
        for model_id, model in self.anki_content['models'].items():
            if model['name'] == model_name:
                return model_id

        return None

    def check_header(self, header, model_id):
        for header_item in header:
            if header_item not in (fld['name'] for fld in self.anki_content['models'][model_id]['flds']):
                return False

        return True

    def check_card_sides(self, card_sides, model_id):
        for card_side in card_sides:
            if card_side not in (tmpl['name'] for tmpl in self.anki_content['models'][model_id]['tmpls']):
                return False

        return True

    @staticmethod
    def check_qfmt_afmt(card_side_format, header):
        def has_field(qfmt_afmt):
            for header_item in header:
                if ("{{%s}}" % header_item) in qfmt_afmt:
                    return True

            return False

        if not has_field(card_side_format['qfmt']):
            return False
        if not has_field(card_side_format['afmt']):
            return False

        return True

    def verify_add_info(self, add_info):
        missing_models_requirement = dict()
        for model_name, notes in add_info['data'].items():
            model_id = self.get_model_id(model_name)
            if model_id is None:
                try:
                    if model_name not in add_info['definitions'].keys():
                        return False
                except KeyError as e:
                    print(e)
                    return False

                missing_models_requirement[model_name] = {
                    'header': set(),
                    'card_sides': set()
                }

                if model_name not in add_info['definitions'].keys():
                    return False
            for note in notes:
                if model_id is not None:
                    if not self.check_header(note['data'].keys(), model_id):
                        return False
                    if not self.check_card_sides(note['decks'].keys(), model_id):
                        return False
                else:
                    missing_models_requirement[model_name]['header'].update(note['data'].keys())
                    missing_models_requirement[model_name]['card_sides'].update(note['decks'].keys())

        if len(missing_models_requirement) > 0:
            for model_name, model_template in add_info['definitions'].items():
                for card_template in model_template['templates']:
                    if not self.check_qfmt_afmt(card_template['data'],
                                           missing_models_requirement[model_name]['header']):
                        return False
                    if card_template['name'] not in missing_models_requirement[model_name]['card_sides']:
                        return False

        return True
