# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import random
import string

_base91_extra_chars = "!#$%&()*+,-./:;<=>?@[]^_`{|}~"


def base62(num, extra=""):
    s = string; table = s.ascii_letters + s.digits + extra
    buf = ""
    while num:
        num, i = divmod(num, len(table))
        buf = table[i] + buf
    return buf


def base91(num):
    # all printable characters minus quotes, backslash and separators
    return base62(num, _base91_extra_chars)


def guid64():
    "Return a base91-encoded 64bit random number."
    return base91(random.randint(0, 2**64-1))


# increment a guid by one, for note type conflicts
def incGuid(guid):
    return _incGuid(guid[::-1])[::-1]


def _incGuid(guid):
    s = string; table = s.ascii_letters + s.digits + _base91_extra_chars
    idx = table.index(guid[0])
    if idx + 1 == len(table):
        # overflow
        guid = table[0] + _incGuid(guid[1:])
    else:
        guid = table[idx+1] + guid[1:]
    return guid
