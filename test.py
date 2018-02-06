import os
from tools import edit
from collections import OrderedDict

with edit.editApkg(os.path.join('sample','Chinese_Sentences_and_audio_spoon_fed.apkg')) as anki:
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
    humanNotes = [{'content': OrderedDict([('English', 'Hello!'),
                              ('Pinyin', 'Nǐ hǎo!'),
                              ('Hanzi', '你好！'),
                              ('Audio', '[sound:tmp1cctcn.mp3]')]),
                   'model name': 'MarkAudio-787e4'}]
    anki.updateHumanNotes(humanNotes)

    humanCards = [{'content': OrderedDict([('English', 'Hello!'),
                              ('Pinyin', 'Nǐ hǎo!'),
                              ('Hanzi', '你好！'),
                              ('Audio', '[sound:tmp1cctcn.mp3]')]),
                   'deck name': 'SpoonFedChinese',
                   'model name': 'MarkAudio-787e4',
                   'template': 'Card 1'},
                  {'content': OrderedDict([('English', 'Hello!'),
                                           ('Pinyin', 'Nǐ hǎo!'),
                                           ('Hanzi', '你好！'),
                                           ('Audio', '[sound:tmp1cctcn.mp3]')]),
                   'deck name': 'SpoonFedChinese',
                   'model name': 'MarkAudio-787e4',
                   'template': 'Card 2'}]
    anki.updateHumanCards(humanCards)
