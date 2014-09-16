import json
from lettuce import *

import "../mailcivi.py"

class TestSettings:
    pass

@step(u'Given I have a CiviCRM URL of "(http[^"]*)"')
def given_i_have_a_civicrm_url_of(step, url):
    world.url = url


@step(u'And I have a Site Key and API Key loaded')
def and_i_have_a_site_key_and_api_key_loaded(step):
    f = open('apikeys.json', 'r')
    assert f, "Cannot open file apikeys.json: " +\
              "create it  with: { \"apikey\": \"redacted\", \"sitekey\": \"redacted\" }"
    keys = json.load(f)
    f.close()
    world.settings = TestSettings()
    world.settings.sitekey = keys['sitekey']
    world.settings.apikey = keys['apikey']


@step(u'Then I can make a connection to CiviCRM')
def then_i_can_make_a_connection_to_civicrm(step):
    global settings
    settings = world.settings
    world.civicrm = connect_to_civi()
    assert world.civicrm, "Connecting to CiviCRM"


@step(u'Then I can check to see if user "([0-9]+)" exists')
def then_i_can_check_to_see_if_userid_exists(step, userid):
    check_creator_exists(world.civicrm, userid)
