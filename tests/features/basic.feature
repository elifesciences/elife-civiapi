Feature: Basic Connectivity
  In order to send email templates
  As the user
  I need to be able to communicate with CiviCRM

  Scenario: Initial connection
    Given I have a CiviCRM URL of "http://crm.elifesciences.org/crm/sites/all/modules/civicrm"
    And I have a Site Key and API Key loaded
    Then I can make a connection to CiviCRM

  Scenario: Checking for a User
    Given I have a CiviCRM URL of "http://crm.elifesciences.org/crm/sites/all/modules/civicrm"
    And I have a Site Key and API Key loaded
    Then I can check to see if user "1" exists
