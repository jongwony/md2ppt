import sys

from . import main

if __name__ == '__main__':
    try:
        sys.exit(main([sys.argv[1]]))
    except (KeyboardInterrupt, SystemExit):
        print('끗')
