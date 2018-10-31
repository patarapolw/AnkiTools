import json
from json.decoder import JSONDecodeError
import sqlite3
from collections import OrderedDict
from tempfile import mkdtemp
import os
import re
from datetime import datetime
import random

from .path import get_collection_path
from .read import read_anki_table


def get_representative_json(file_input=None,
                            formatted=False, annotate_is_json=False,
                            sampling_substitution_regex=('(.+)', '\\1_sample'),
                            do_not_sample=('sqlite_stat1', ),
                            sampling_limits=None):
    """
    :param None|str file_input:
    :param bool formatted:
    :param bool annotate_is_json:
    :param tuple sampling_substitution_regex: to shorten string by one, try ('(.+).{1}', '\\1') or ('(.+)s', '\\1')
    :param list|tuple do_not_sample:
    :param None|dict sampling_limits:
    :return:
    """
    if file_input is None:
        file_input = get_collection_path()

    source = file_input

    if sampling_limits is None:
        sampling_limits = {
            'notes': 10,
            'cards': 10
        }

    if os.path.splitext(file_input)[1] == '.apkg':
        from AnkiTools.convert import anki_convert

        tempdir = mkdtemp()
        temp_anki2 = os.path.join(tempdir, 'temp.anki2')
        anki_convert(file_input, out_file=temp_anki2)
        file_input = temp_anki2

    output_json = OrderedDict(
        _meta=OrderedDict(
            generated=datetime.fromtimestamp(datetime.now().timestamp()).isoformat(),
            source=os.path.abspath(source),
            data=OrderedDict()
        )
    )

    with sqlite3.connect(file_input) as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for row in cursor:
            table_name = row[0]
            key = table_name

            output = list(read_anki_table(conn, table_name))

            if table_name not in output_json['_meta']['data'].keys():
                output_json['_meta']['data'][table_name] = OrderedDict()

            output_json['_meta']['data'][table_name]['number_of_entries'] = len(output)

            if len(output) >= 1:
                if len(output) > 1:
                    if table_name in do_not_sample:
                        output_json[key] = output
                    else:
                        re_match, re_replace = sampling_substitution_regex
                        key = re.sub(re_match, re_replace, key)
                        output_json[key] = random.sample(output, sampling_limits.get(table_name, 10))
                else:
                    output_json[key] = output[0]

                if formatted:
                    to_format = output_json[key]
                    if isinstance(output_json[key], (dict, OrderedDict)):
                        _format_representative_json(to_format, annotate_is_json)
                    else:
                        for item in to_format:
                            _format_representative_json(item, annotate_is_json)
            else:
                output_json[key] = None

    return output_json


def _format_representative_json(to_format, annotate_is_json: bool):
    for k, v in to_format.items():
        if v is not None:
            try:
                json_object = json.loads(v, object_pairs_hook=OrderedDict)
                if annotate_is_json:
                    to_format[k] = {
                        'is_json': True,
                        'data': json_object
                    }
                else:
                    to_format[k] = json_object
            except (TypeError, JSONDecodeError):
                pass

    return to_format
