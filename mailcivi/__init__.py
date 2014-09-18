"""
Mailcivi command line tool
"""

import sys

def main(): # needed for console script
    if __package__ == '':
        # To be able to run 'python mailcivi-0.9/mailcivi':
        import os.path
        path = os.path.dirname(os.path.dirname(__file__))
        sys.path[0:0] = [path]
    sys.exit(mailcivi.main())

if __name__ == "__main__":
    sys.exit(main())
