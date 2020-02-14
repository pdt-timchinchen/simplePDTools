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

currentIncident = 0
maxIncidentNumber = 0
while True:


    r = requests.get('https://api.pagerduty.com/incidents?time_zone=UTC&sort_by=incident_number%3ADESC',headers = {
        "Accept":"application/vnd.pagerduty+json;version=2",
        "Authorization":"Token token=YOURTOKENHERE",
    })

    if r.status_code == 200:

        if currentIncident == 0:
            for incident in r.json()['incidents']:
                if incident['incident_number'] > currentIncident:
                    currentIncident=incident['incident_number']
            maxIncidentNumber = currentIncident
            print("Starting from " + str(currentIncident))
        else:
            for incident in r.json()['incidents']:
                if incident['incident_number'] > currentIncident:
                    currentIncident = incident['incident_number'] 
                    print("Send Incident " + str(currentIncident) + " to Dolphin")
                    if incident['incident_number'] > maxIncidentNumber:
                        maxIncidentNumber = incident['incident_number']
            currentIncident = maxIncidentNumber
            print("Continue from " + str(currentIncident))

    else:
        print("Failed")

    time.sleep(10)
