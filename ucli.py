#!/usr/bin/env python

import os
import re
import sys
from termcolor import colored


def header(text, *on_same_line, color='blue',
           end=os.linesep, with_newline=False):
    if with_newline:
        print()
    print(colored(text, color), *on_same_line, end=end)


def info(*args, **kwargs):
    header(*args, **kwargs, color='green')


def highlight(text):
    return colored(text, 'yellow')


def inline_prompt(prompt, prefill=False):
    if not prefill:
        header(prompt, end='')
        return input()
    from readline import set_startup_hook, insert_text
    set_startup_hook(lambda: insert_text(prefill))
    try:
        return input(colored(prompt, 'blue'))
    finally:
        set_startup_hook()


def gen_to_list(generator, limit=5):
    return [g for i, g in enumerate(generator, 1) if i <= limit]


def get_field(field, default='', prefill=False, necessary=False):
    _default = '' if default == '' else f' (default: {default})'
    _header = f'{field.title()}{_default}: '
    _field = inline_prompt(_header, prefill)
    if necessary and not _field:
        info(f'It is necessary to enter the {field}')
        return get_field(field, default, prefill, necessary)
    return _field or default


OPTIONS_REGEX = re.compile(r'(\[.*?\])')


def print_options(options):
    print(' ', OPTIONS_REGEX.sub(highlight(r'\1'), options))


def print_candidates(candidates, capitalize=True):
    for i, candidate in enumerate(candidates, 1):
        _i = f'[{i}]'
        candidate = str(candidate).title() if capitalize else candidate
        print(f'  {highlight(_i) if i == 1 else _i} {candidate}')


def parse_selection(candidates, actions={}, message='Select an option'):
    selection = inline_prompt(f'{message}: ')

    if not selection:
        if candidates is None:
            return True
        return candidates[0]

    elif (selection.isdigit() and 0 < int(selection) < len(candidates) + 1):
        return candidates[int(selection) - 1]

    elif selection in actions:
        try:
            # Try to call function
            return actions[selection]()
        except TypeError:
            # Means that is a tuple
            function, *args = actions[selection]
            return function(*args)

    elif selection in ['s', 'S']:
        return

    elif selection in ['q', 'Q']:
        drop('Interrupted by user')

    else:
        return parse_selection('Invalid selection. Try again')


def drop(message=None, with_code=1):
    if message is None:
        info('-' * 5)
    else:
        info(f'{message}{os.linesep}{"-" * len(message)}')
    print_options('Press [RETURN] to exit')
    input()
    sys.exit(with_code)
