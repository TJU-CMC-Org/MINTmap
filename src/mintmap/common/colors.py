# colors.py

import sys


def _color_print(*objects, color='33', file=sys.stderr, sep=' ', end='\n'):
    print(f'\x1b[{color}m', file=file, sep='', end='')
    print(*objects, '\x1b[0m', file=file, sep=sep, end=end)


def cyan(*objects, file=sys.stderr, sep=' ', end='\n'):
    _color_print(*objects, color='36', file=file, sep=sep, end=end)


def green(*objects, file=sys.stderr, sep=' ', end='\n'):
    _color_print(*objects, color='32', file=sys.stderr, sep=sep, end=end)


def red(*objects, file=sys.stderr, sep=' ', end='\n'):
    _color_print(*objects, color='31', file=sys.stderr, sep=sep, end=end)


def yellow(*objects, file=sys.stderr, sep=' ', end='\n'):
    _color_print(*objects, color='33', file=file, sep=sep, end=end)


def color_reset():
    print('\x1b[0m', file=sys.stdout, sep='', end='')
    print('\x1b[0m', file=sys.stderr, sep='', end='')
