elife-civiapi
=============

Code for using the CiviCRM api

Virtualenv
----------
This project can be used with virtualenv:

```
  cd <path containing mailcivi.py>
  virtualenv .
```

Requirements
------------
You will need to install the following packages:

```
  pip install html2text
  pip install requests
  pip install json
```
  
The package python-civicrm is provided as a git subproject link which should
be fetched if needed from git@github.com:rivimey/python-civicrm.git
Note that the subproject is called "pythonCivicrm", not "python-civicrm".

Usage
-----
This is a shell script, to be used from the command line. For example:

```
  bin/python mailcivi.py --sitekey={key} --apikey={key} \
      --name "Test mailing" --subject "My First Mailing" --from_id 1
      --civicrm=http://crm.example.org/sites/all/modules/civicrm \
      --html=file.html
```

where file.html is a file containing html text for the mail template body.

The email template will be created on the CiviCRM server and can be found
by checking the 'Drafts' area and sent from there.

Documentation
-------------
There is a 'man' page for mailcivi in the docs directory. For recent versions
of 'man' it can be read using `man docs/mailcivi.man`. Alternatively the
file mailcivi.man must be made available in the 'man path', refer to the
man tool for details.

Tests
-----
There are tests created using `lettuce` in the tests folder:

```
  cd tests
  lettuce
```
