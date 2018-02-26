import os
from AnkiTools.tools import edit
from collections import OrderedDict

with edit.editApkg(os.path.join('apkg', 'Chinese.apkg')) as anki:
    # anki.updateModels({
    #                     'mid': model_id,
    #                     'name': model_name,
    #                     'fields': list_of_field_names,
    #                     'templates': list_of_template_names
    #
    #                 })
    #
    # anki.updateDecks({
    #                     'did': deck_id,
    #                     'name': deck_name
    #                 })
    #
    # anki.updateNotes({
    #                     'nid': note_id,
    #                     'mid': model_id,
    #                     'content': list_of_field_contents.join('\x1f')
    #                 })
    #
    # anki.updateCards({
    #                     'cid': card_id,
    #                     'nid': note_id,
    #                     'did': deck_id,
    #                     'ord': order_in_list_of_template_names
    #                 })
    pass
