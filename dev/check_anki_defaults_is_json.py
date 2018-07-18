import simplejson as json
from collections import OrderedDict


def get_is_json():
    is_json = OrderedDict()
    with open('defaults_formatted.json') as f:
        defaults = json.load(f, object_pairs_hook=OrderedDict)
    for table_name, table_dict in defaults.items():
        is_json[table_name] = OrderedDict()
        if table_dict is None:
            continue

        for header_item, v in table_dict.items():
            try:
                if v['is_json'] is True:
                    is_json[table_name][header_item] = True
                else:
                    is_json[table_name][header_item] = False
            except TypeError:
                is_json[table_name][header_item] = False

    return is_json


if __name__ == '__main__':
    print(json.dumps(get_is_json(), indent=2))
