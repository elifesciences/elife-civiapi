#!/bin/sh

$type="vor"
if [ "$1" = "poa" -o "$1" = "vor" ] ; then
  type=$1
fi
today=$(date +'%Y-%m-%d')

CIVICRM=http://example.org/crm/sites/all/modules/civicrm
JOURNAL=http://example.org/elife/content_alerts_json/content_alerts_$type/$today
SITEKEY=REDACTED
APIKEY=REDACTED
MAILCIVI=/usr/local/bin/mailcivi/mailcivi.py

$MAILCIVI --civicrm=$CIVICRM --url="$JOURNAL" --sitekey="$SITEKEY" --apikey="$APIKEY"
