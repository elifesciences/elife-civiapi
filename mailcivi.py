#!bin/python

from __future__ import print_function
import sys, os, inspect
import argparse

pycrmfolder = os.path.realpath(
    os.path.abspath(
        os.path.join(
            os.path.split(
                inspect.getfile(inspect.currentframe()))[0],
            "python-civicrm/pythoncivicrm")))
if pycrmfolder not in sys.path:
    sys.path.insert(0, pycrmfolder)

from pythoncivicrm import CiviCRM

# using print_function
def debugmsg(*objs):
    """
    Print additional info to stderr iff the verbose flag has been enabled
    """
    if settings.verbose > 1:
        print("DEBUG: ", *objs, end='\n', file=sys.stderr)


def infomsg(*objs):
    """
    Print additional info to stderr iff the verbose flag has been enabled
    """
    if settings.verbose:
        print("INFO: ", *objs, end='\n', file=sys.stderr)


def warningmsg(*objs):
    """
    Print warning message to stderr
    """
    print("WARNING: ", *objs, end='\n', file=sys.stderr)


def errormsg(*objs):
    """
    Print error message to stderr
    """
    print("ERROR: ", *objs, end='\n', file=sys.stderr)


def getoptions():
    """
    Use the Python argparse module to read in the command line args
    """
    parser = argparse.ArgumentParser(
        prog='mailcivi',
        description='Create a new mail template in a remote CiviCRM installation.',
        usage='%(prog)s [options]'
        )
    parser.add_argument('--url', help='URL of the site', default='http://crm.example.org/crm/civicrm/ajax/rest')

    parser.add_argument('--verbose', '-v', action='count', help='print additional messages to stderr', default=0)

    args = parser.parse_args()

    return args


def main():
    global settings
    settings = getoptions()

    # http://crm.elifesciences.org/crm/sites/all/modules/civicrm/extern/
    #    rest.php??entity=Mailing&action=get&debug=1&sequential=1&json=1&api_key={yoursitekey}&key={yourkey}

    url = 'http://crm.elifesciences.org/crm'

    civicrm = CiviCRM(url, site_key=site_key, api_key=api_key, use_ssl=False)

    search_results = civicrm.get('Mailing')

    print(search_results)


try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    sys.exit(1)



