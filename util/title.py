from pyfiglet import print_figlet

from . import term_size


def figlet(m):
    extra, title = m.groups()
    if extra == '':
        print_figlet(
            title, colors='WHITE:',
            width=term_size.columns, justify='center'
        )
    elif extra == '#':
        print_figlet(
            title, font='banner', colors='WHITE:',
            width=term_size.columns
        )
    else:
        print_figlet(title, font='3x5', colors='WHITE:',
                     width=term_size.columns)
