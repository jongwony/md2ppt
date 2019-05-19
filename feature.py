import os
import re
import shutil
import sys
from itertools import chain
from operator import methodcaller

from .util.code import code_glyph
from .util.getch import getch
from .util.img import iterm2_img_format
from .util.title import figlet


def transition():
    char = getch()
    if char == ':':
        char = input(':')
    os.system('clear')
    return char


def pre(m, border=True):
    lexer, code = m.groups()
    if lexer in ['gv', 'graphviz']:
        from graphviz import Source
        gv = Source(code)
        sys.stdout.write(iterm2_img_format(gv.pipe('png')))
    else:
        sys.stdout.write(code_glyph(code, lexer, border))
    sys.stdout.flush()


def images(m):
    sentence = m.group(1)
    try:
        sys.stdout.write(iterm2_img_format(sentence))
    except Exception as e:
        print(e, file=sys.stderr)
        sys.stdout.write(sentence)
    sys.stdout.flush()


def controller(ch, cur):
    if ch == 'q':
        raise StopIteration

    if ch.isdigit():
        return int(ch)

    return cur + 1


def slide_show(md):
    global term_size
    regex_domain = {
        re.compile(r'!\[.*\]\((.*?)\)'): images,
        re.compile(r'```([a-z]*)\n([\s\S]*?)\n```'): pre,
        re.compile(r'#(#{0,5}) (.*)'): figlet,
    }

    with open(md) as f:
        data = f.read()
    split_list = re.split(r'^---$', data, flags=re.M)

    os.system('clear')
    slide_idx = 0
    while slide_idx < len(split_list):
        slide = split_list[slide_idx]
        term_size = shutil.get_terminal_size()
        print(f'slide: {slide_idx}'.rjust(term_size.columns))
        matched = chain(*[re.finditer(pattern, slide)
                          for pattern in regex_domain])
        matched = sorted(matched, key=methodcaller('start'))
        idx = 0
        for m in matched:
            sys.stdout.write(slide[idx:m.start()])
            sys.stdout.flush()
            regex_domain[m.re](m)
            idx = m.end()
        sys.stdout.write(slide[idx:])
        sys.stdout.flush()
        try:
            slide_idx = controller(transition(), slide_idx)
        except StopIteration:
            break

    sys.stdout.write('END!')
    sys.stdout.flush()
    transition()
