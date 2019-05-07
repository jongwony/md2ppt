from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from . import term_size


def code_highlight(code, lexer):
    try:
        if not lexer:
            lexer = guess_lexer(code)
        else:
            lexer = get_lexer_by_name(lexer)
    except ClassNotFound:
        lexer = TextLexer()

    return highlight(code, lexer, Terminal256Formatter())


def code_glyph(code, lexer=None, border=True):
    hl_code = code_highlight(code, lexer)
    if border:
        header = "\u2554" + '\u2550' * (term_size.columns - 2) + '\u2557\n'
        footer = "\u255A" + '\u2550' * (term_size.columns - 2) + '\u255D\n'
        wall = '\u2551'
    else:
        header = footer = ''
        wall = ' '

    hl_box = '\n'.join(
        f"{wall} {sentence}" + ' ' * (
                term_size.columns - len(origin) - 3) + f"{wall}"
        for sentence, origin in
        zip(hl_code.rstrip().split('\n'), code.rstrip().split('\n'))
    )
    return f'{header}{hl_box}{footer}'
