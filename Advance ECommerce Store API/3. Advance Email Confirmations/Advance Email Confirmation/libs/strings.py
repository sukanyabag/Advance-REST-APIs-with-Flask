'''
libs.strings

By default, uses 'en-gb.json' file inside the 'strings' top level folder.

If language changes, set 'libs.strings.default_locale' and run 'libs.strings.refresh()'.

Terminology-

1. Caching - Temporarily storing a piece of data that is being used multiple times ,
so it doesn't need to be regenerated or retrieved many times. It increases performance of application.
'''

import json

default_locale = "en-gb"
cached_strings = {}


def refresh():
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def get_text(name):
    return cached_strings[name]


