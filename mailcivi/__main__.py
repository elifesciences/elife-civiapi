#!bin/python
# Script to read an email template, either directly or as a JSON bundle,
# and send that bundle to a CiviCRM instance running remotely. JSON bundle
# data can be read from a local file or from a web service via a supplied
# URL.
#
# Written: August 2014 Ruth Ivimey-Cook
#

from __future__ import print_function
import sys
import os
import argparse
import json
import html2text
import requests

# basedir points to the parent dir of mailcivi, and pythoncivicrm
# is installed alongside mailcivi.
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, os.path.join(basedir, 'python-civicrm'))

from pythoncivicrm import (CiviCRM, CivicrmError)


def debugmsg(settings, *objs):
    """
    Print additional info to stderr iff the verbose flag has been enabled
    """
    if settings.verbose > 1:
        print("DEBUG: ", *objs, end='\n', file=sys.stderr)


def infomsg(settings, *objs):
    """
    Print additional info to stderr iff the verbose flag has been enabled
    """
    if settings.verbose:
        print("INFO: ", *objs, end='\n', file=sys.stderr)


def warningmsg(settings, *objs):
    """
    Print warning message to stderr
    """
    print("WARNING: ", *objs, end='\n', file=sys.stderr)


def errormsg(settings, *objs):
    """
    Print error message to stderr
    """
    print("ERROR: ", *objs, end='\n', file=sys.stderr)


class CiviMailTemplate:
    """
    Mail template object, filled out by readjson() and readlocal(),
    to hold the intermediate form of the input email.
    """
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
    parser.add_argument('--verbose', '-v',
                        action='count',
                        help='Print additional messages to stderr',
                        default=0)
    parser.add_argument('--civicrm',
                        help='URL of the CiviCRM module on the destination site.',
                        default='http://crm.example.org/sites/all/modules/civicrm')
    parser.add_argument('--sitekey',
                        help='The CiviCRM site_key of the site you are connecting to.',
                        default='')
    parser.add_argument('--apikey',
                        help='The CiviCRM api key.',
                        default='')
    parser.add_argument('--name',
                        help='Name of new mail template. Overrides a name specified by file.')
    parser.add_argument('--subject',
                        help='Email subject text. Overrides a subject specified by file.')
    parser.add_argument('--from_id',
                        help='CiviCRM Contact ID of sender.')
    inputgroup = parser.add_mutually_exclusive_group(required=True)
    inputgroup.add_argument('--json', nargs='?',
                            type=argparse.FileType('r'),
                            dest='jsonfile',
                            help='File containing the templated email as JSON.')
    inputgroup.add_argument('--url', nargs='?',
                            dest='jsonurl',
                            help='URL from which to fetch the templated email as JSON.')
    inputgroup.add_argument('--html', nargs='?',
                            type=argparse.FileType('r'),
                            dest='htmlfile',
                            help='File containing the templated HTML to email.')
    parser.add_argument('--text',
                        type=argparse.FileType('r'),
                        dest='textfile',
                        help='File containing the templated Text to email. If'
                             ' not supplied, the html version is rendered using'
                             ' html2text.')
    args = parser.parse_args()

    return args


def readjson(settings, jsontemplate):
    """
    Read the necesary input data for the mail template into the
    result, where metadata from the command line (seen in the
    global settings) overrides json-supplied data.

    :param jsontemplate: The JSON-derived input.
    :return: an object containing the data to send
    """
    result = CiviMailTemplate()
    result.name = jsontemplate['name']
    result.subject = jsontemplate['subject']
    result.from_id = jsontemplate['from_id']
    result.html = jsontemplate['html']
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


def readlocal(settings):
    """
    Read the necesary input data for the mail template into the
    result, where metadata from the command line (seen in the
    global settings) overrides json-supplied data.

    :param jsontemplate: The JSON-derived input.
    :return: an object containing the data to send
    """
    result = CiviMailTemplate()
    result.name = settings.name
    result.subject = settings.subject
    result.from_id = settings.from_id
    result.html = settings.htmlfile.read()
    if settings.textfile:
        result.plain = settings.textfile.read()
    else:
        result.plain = getplaintext(result.html)

    return result


def fetch_url(jsonurl):
    """
    Read a JSON template for the email by fetching the URL provided.

    :param jsonurl: A URL that resolves to return application/json data.
    :return: The returned JSON content, or the null-json '{}'
    """
    r = requests.get(jsonurl)
    if r.status_code == 200 and r.headers['content-type'].startswith('application/json'):
        # Should be this instead? return r.text.encode('utf8')
        return r.text
    else:
        raise Exception('Failed to fetch JSON: ' + str(r.status_code))


def getplaintext(html):
    """
    Return a reasonable plain-text version of the HTML input.

    :param html: string containing HTML input text.
    :return: string containing plain-text equivalent.
    """
    return html2text.html2text(html)


def connect_to_civi(settings):
    """
    Create a new CiviCRM object from the values in 'settings'.
    :return:
    """
    civicrm = CiviCRM(settings.civicrm, site_key=settings.sitekey,
                      api_key=settings.apikey, use_ssl=False)
    return civicrm


def check_creator_exists(settings, civicrm, creator_id):
    """
    Check that creator_id is a valid CiviCRM user.

    :param civicrm: Object used to talk to the CiviCRM api.
    :param creator_id: A Civicrm userid.
    :return: Boolean - True if the userid exists in CiviCRM as a user.
    """
    params = {
        u'contact_id': creator_id,
    }
    contactresults = civicrm.get(u'Contact', **params)
    if len(contactresults) == 1:
        debugmsg(settings, u'Creator is object ', contactresults[0])
        if contactresults[0][u'contact_id'] == creator_id:
            infomsg(settings, u'Creator is ', contactresults[0][u'sort_name'])
            return True
        else:
            warningmsg(settings, u'Creator id did not match : ' +
                       contactresults[0][u'contact_id'] + u' <> ' + creator_id)
            return False
    else:
        warningmsg(settings, u'Creator id was not found in CiviCRM.')
        return False


def create_template(settings, civicrm, template):
    """
    Send the email defined by the template to the CiviCRM instance.

    :param civicrm: Object defining a CiviCRM instance.
    :param template: Array defining the template mail.
    """
    params = {
        u'name': template.name,
        u'subject': template.subject,
        u'created_id': template.from_id,
        u'body_html': template.html,
        u'body_text': template.plain,
        u'url_tracking': u'1',
    }
    try:
        results = civicrm.create(u'Mailing', **params)
        debugmsg(settings, u'Returned Mailing object ', results[0])
        infomsg(settings, u'Template Created on:', results[0]['created_date'])

        # CiviCRM defaults to creating a MailingJob record, which is not
        # wanted: this code deletes it again.
        if len(results[0]['api.mailing_job.create']['values']) == 1:
            delete_mailingjob(settings, civicrm, results[0]['api.mailing_job.create']['values'][0]['id'])

        return True

    except CivicrmError as e:
        print(u'Mail template creation failed: ' + e.message)
        return False


def delete_mailingjob(settings, civicrm, jobid):
    """
    Send the email defined by the template to the CiviCRM instance.

    :param civicrm: Object defining a CiviCRM instance.
    :param jobid: The mailing job ID to delete.
    """
    try:
        results = civicrm.delete(u'MailingJob', jobid, True)
        debugmsg(settings, u'Returned object ', results)
        infomsg(settings, u'Deleted:', jobid)
        return True

    except CivicrmError as e:
        print(u'Mailing job deletion failed: ' + e.message)
        return False


def mailcivi():
    """
    Parse the command line args to determine where the mail template
    is coming from, fetch it, and send it on to the CiviCRM instance
    using the supplied URL and keys.

    Returns the integer code to shell:
        0 for success,
        1 for parameter problem,
        2 for internal error.
    """
    settings = getoptions()

    # There is a hierarchy of input sources: local HTML files are preferred,
    # then a local JSON file, then a JSON URL. However this should not
    # be important because 'getoptions()' considers the three sources to be
    # mutually exclusive.
    template = None
    try:
        if settings.htmlfile:
            template = readlocal(settings)
        elif settings.jsonfile:
            jsontemplate = json.load(settings, settings.jsonfile)
            template = readjson(settings, jsontemplate)
        elif settings.jsonurl:
            jsontemplate = json.loads(fetch_url(settings.jsonurl))
            template = readjson(settings, jsontemplate)
    except Exception as e:
        print(e.message)
        return 2

    infomsg(settings, 'Using URL :', settings.civicrm)
    infomsg(settings, 'Name      :', template.name)
    infomsg(settings, 'Subject   :', template.subject)
    infomsg(settings, 'Creator   :', template.from_id)

    civicrm = connect_to_civi(settings)
    if check_creator_exists(settings, civicrm, template.from_id):
        if create_template(settings, civicrm, template):
            return 0

    return 1


def main():                 # needed for console script
    sys.exit(mailcivi())


if __name__ == "__main__":
    sys.exit(main())
