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

NagiosUp = True
url = "https://events.pagerduty.com/v2/enqueue"

while True:

    #The URL to ping: -
    r = requests.get('http://www.timchinchen.co.uk/')

    #If it doesn't return a successful HTTP Reponse then fire a PagerDuty Event. In this case use a DeDup Key
    #You can fire multiple events against the same key, in this example I've added logic to prevent multiple sends - but not really needed!
    if r.status_code != 200:

        if NagiosUp:

            print("No response - Sending Alert")

            headers = {'Content-Type': 'application/json'}
            payload = {
                    "payload": {
                        "summary": "Heartbeat failed",
                        "source": "Heartbeat",
                        "severity": "critical",
                        "class": "hearbeat"
                    },
                    "routing_key": "PD KEY",
                    "dedup_key": "NAGIOSHEARTBEAT",
                    "event_action": "trigger",
                    "client": "Heartbeat"
                    }
                    
            r = requests.post(url, json=payload, headers=headers)
            r.raise_for_status()
            dedupKey = str(r.json()['dedup_key'])
            print("  Status: " + str(r.json()['status']) + " Key: " + dedupKey)

            NagiosUp = False

        print("No response - Still Down")


    else:

        if NagiosUp !=True:

            print("Nagios Up - Resolving Alert")

            headers = {'Content-Type': 'application/json'}
            payload = {
                    "payload": {
                        "summary": "Heartbeat failed",
                        "source": "Heartbeat",
                        "severity": "critical",
                        "class": "hearbeat"
                    },
                    "routing_key": "PD KEY",
                    "dedup_key": "NAGIOSHEARTBEAT",
                    "event_action": "resolve",
                    "client": "Heartbeat"
                    }

            r = requests.post(url, json=payload, headers=headers)
            r.raise_for_status()
            dedupKey = str(r.json()['dedup_key'])
            print("  Status: " + str(r.json()['status']) + " Key: " + dedupKey)

            NagiosUp = True

        print("Response from Nagios")

    time.sleep(60)
