#!bin/python

from __future__ import print_function
import sys
import os
import inspect
import argparse
import html2text

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
        usage='%(prog)s [options] [htmlfile] [textfile]'
    )
    parser.add_argument('--url',
                        help='URL of the site homepage.', default='http://crm.example.org/sites/all/modules/civicrm')
    parser.add_argument('--sitekey', help='The site_key of the site you are connecting to.', default='')
    parser.add_argument('--apikey', help='The api key.', default='')
    parser.add_argument('--name', help='Name of new template.', default='mailinglist')
    parser.add_argument('--subject', help='Email subject text.', default='News')
    parser.add_argument('--from_id', help='CiviCRM Contact ID of sender.', default='1')
    parser.add_argument('htmlfile', nargs='?', type=argparse.FileType('r'),
                        help='File containing the templated HTML to email. If not supplied, read from stdin.',
                        default=sys.stdin)
    parser.add_argument('textfile', nargs='?', type=argparse.FileType('r'),
                        help='File containing the templated Text to email. If not supplied, the html version'
                             'is rendered using html2text.',
                        default=None)
    parser.add_argument('--verbose', '-v', action='count',
                        help='Print additional messages to stderr', default=0)

    args = parser.parse_args()

    return args


def getplaintext(html):
    return html2text.html2text(html)

def check_creator(civicrm, creator_id):
    params = {
        'contact_id': creator_id,
    }
    contactresults = civicrm.get('Contact', **params)
    debugmsg('Owner is object ', contactresults)
    if len(contactresults) == 1:
        if (contactresults[0]['contact_id'] == creator_id):
            infomsg('Creator is ', contactresults[0]['sort_name'])
        else:
            warningmsg('Creator id did not match.')
            return False
    else:
        warningmsg('Creator id was not found.')
        return False

    return True


def main():
    global settings
    settings = getoptions()

    htmltemplate = settings.htmlfile.read()
    plaintext = getplaintext(htmltemplate)

    infomsg('Using: ')
    infomsg('  URL  :', settings.url)
    infomsg('  Skey :', settings.sitekey)
    infomsg('  Akey :', settings.apikey)
    infomsg('Name   :', settings.name)
    infomsg('Subject:', settings.subject)
    infomsg('Creator:', settings.from_id)

    civicrm = CiviCRM(settings.url, site_key=settings.sitekey, api_key=settings.apikey, use_ssl=False)

    debugmsg('Constructed object ', civicrm)

    if check_creator(civicrm, settings.from_id):
        params = {
            'name': settings.name,
            'subject': settings.subject,
            'created_id': settings.from_id,
            'body_html': htmltemplate,
            'body_text': plaintext,
            'url_tracking': '1',
        }
        results = civicrm.create('Mailing', **params)
        infomsg('Returned object ', results)


try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print("Interrupted\n")
    sys.exit(1)



