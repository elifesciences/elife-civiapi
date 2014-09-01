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

import json
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


class mailtemplate:
    pass

def getoptions():
    """
    Use the Python argparse module to read in the command line args
    """
    parser = argparse.ArgumentParser(
        prog='mailcivi',
        description='Create a new mail template in a remote CiviCRM installation.',
        usage='%(prog)s [options] (--json=file|--html=file) [--text=file]'
    )
    parser.add_argument('--verbose', '-v', action='count',
                        help='Print additional messages to stderr', default=0)
    parser.add_argument('--url',
                        help='URL of the site homepage.', default='http://crm.example.org/sites/all/modules/civicrm')
    parser.add_argument('--sitekey', help='The site_key of the site you are connecting to.', default='')
    parser.add_argument('--apikey', help='The api key.', default='')
    parser.add_argument('--name', help='Name of new template.', default='mailinglist')
    parser.add_argument('--subject', help='Email subject text.', default='News')
    parser.add_argument('--from_id', help='CiviCRM Contact ID of sender.', default='1')
    inputgroup = parser.add_mutually_exclusive_group(required=True)
    inputgroup.add_argument('--json', nargs='?', type=argparse.FileType('r'),
                            dest='jsonfile',
                            help='File containing the templated email as JSON.')
    inputgroup.add_argument('--html', nargs='?', type=argparse.FileType('r'),
                            dest='htmlfile',
                            help='File containing the templated HTML to email.')
    parser.add_argument('--text', type=argparse.FileType('r'),
                        dest='textfile',
                        help='File containing the templated Text to email. If not supplied, the html version'
                             'is rendered using html2text.')

    args = parser.parse_args()

    return args


def readjson(jsontemplate):
    """
    Read the necesary input data for the mail template into the
    result, where metadata from the command line (seen in the
    global settings) overrides json-supplied data.

    :param jsontemplate: The JSON-derived input.
    :return: an object containing the data to send
    """
    result = mailtemplate()
    result.name = jsontemplate['name']
    result.subject = jsontemplate['subject']
    result.from_id = jsontemplate['from_id']
    result.html = jsontemplate['html']
    result.plain = jsontemplate['plain']
    if jsontemplate['plain']:
        result.plain = jsontemplate['plain']
    else:
        result.plain = getplaintext(result.html)

    if settings.name > "":
        result.name = settings.name
    if settings.subject > "":
        result.subject = settings.subject
    if settings.from_id > "":
        result.from_id = settings.from_id

    return result

def readlocal():
    """
    Read the necesary input data for the mail template into the
    result, where metadata from the command line (seen in the
    global settings) overrides json-supplied data.

    :param jsontemplate: The JSON-derived input.
    :return: an object containing the data to send
    """
    result = mailtemplate()
    result.name = settings.name
    result.subject = settings.subject
    result.from_id = settings.from_id
    result.html = settings.htmlfile.read()
    if settings.textfile:
        result.plain = settings.textfile.read()
    else:
        result.plain = getplaintext(result.html)

    return result

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

    if settings.htmlfile:
        template = readlocal()
    if settings.jsonfile:
        jsontemplate = json.load(settings.jsonfile)
        template = readjson(jsontemplate)

    infomsg('Using: ')
    infomsg('  URL  :', settings.url)
    infomsg('  Skey :', settings.sitekey)
    infomsg('  Akey :', settings.apikey)
    infomsg('Name   :', template.name)
    infomsg('Subject:', template.subject)
    infomsg('Creator:', template.from_id)

    civicrm = CiviCRM(settings.url, site_key=settings.sitekey, api_key=settings.apikey, use_ssl=False)

    debugmsg('Constructed object ', civicrm)

    if check_creator(civicrm, template.from_id):
        params = {
            'name': template.name,
            'subject': template.subject,
            'created_id': template.from_id,
            'body_html': template.html,
            'body_text': template.plain,
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



