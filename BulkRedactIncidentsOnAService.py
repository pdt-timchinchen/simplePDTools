######
# To run in Python3:
# python3 -m pip install pytz
# python3 -m pip install requests
# Should also run in Default Python 2.7!
######
import requests
import datetime
import time
import pytz
import sys

#--------------------------------------------------------------------------------------------------
# EDIT THESE FOR YOUR SERVICES
defaultUser = '@pagerduty.com'
serviceID = "YOURSERVICE" #<<<<< VERY IMPORTANT DO NOT MIX WITH ANOTHER SERVICE ID
token = "YOURKEY"
PDDomain = "pdu-chinchen-auto"
# END: EDIT THESE FOR YOUR SERVICES
#--------------------------------------------------------------------------------------------------


#Set up the default headers for your environment
headers = {'Content-Type': 'application/json',  "from" : defaultUser  , "Accept": "application/vnd.pagerduty+json;version=2", 'Authorization': "Token token=" + token}
#--------------------------------------------------------------------------------------------------

offsetValue = 0
limitValue = 1

#--------------------------------------------------------------------------------------------------
while True:
    #Pagination
    options = {
        "limit": limitValue,
        "offset": offsetValue
    }

    r = requests.get('https://api.pagerduty.com/incidents?service_ids%5B%5D=' + serviceID, json=options ,headers=headers)
    #Redaction appears to be done using this: 
    #https://[YOURDOMAIN].pagerduty.com/api/v1/incidents/[INCIDENTID]/redact &  #(DELETE and needs an API key and a valid email in the header)

    for inc in r.json()["incidents"]:
        print("Redacting: " + inc["id"])
        IncidentID = inc["id"]
        delURL = "https://" + PDDomain + ".pagerduty.com/api/v1/incidents/" + IncidentID + "/redact"
        rRedact = requests.delete(delURL, headers=headers)
        rRedact.raise_for_status()
        print("Redact complete for: " + inc["id"])
        offsetValue = offsetValue + limitValue

    print ("More Incidents to redact? = " + str(r.json()["more"]))
    if r.json()["more"] == False:
            break

print("Redaction complete for ServiceID" + serviceID)
#--------------------------------------------------------------------------------------------------
