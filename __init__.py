from .feature import slide_show


def main(args=None):
    if args:
        slide_show(args[0])
