import re


def collapse_json(text, list_length=4):
    for length in range(list_length):
        re_pattern = r'\[' + (r'\s*(.+)\s*,' * length)[:-1] + r'\]'
        re_repl = r'[' + ''.join(r'\{}, '.format(i+1) for i in range(length))[:-2] + r']'

        text = re.sub(re_pattern, re_repl, text, re.DEBUG)

    return text
