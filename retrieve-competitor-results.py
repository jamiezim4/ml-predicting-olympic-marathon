import csv
import requests
import json
import dateparser
from datetime import datetime

f_in = open("competitors.csv", "r")
csvFile_in = csv.DictReader(f_in)

f_out = open("individual-performances.csv", "w")
fields = ['id', 'iaafId', 'firstName', 'lastName', 'countryCode', 'countryName', 'birthDate',
'performanceDate', 'competition', 'venueCountry', 'place', 'eventId', 'competitionId', 'timeResult']
csvFile_out = csv.DictWriter(f_out, fieldnames=fields)
csvFile_out.writeheader()

payload = "{\"query\":\"query GetSingleCompetitorAllTimePersonalTop10($id: Int, $urlSlug: String, $allTimePersonalTop10Discipline: Int) {\\n  getSingleCompetitorAllTimePersonalTop10(id: $id, urlSlug: $urlSlug, allTimePersonalTop10Discipline: $allTimePersonalTop10Discipline) {\\n    parameters {\\n      allTimePersonalTop10Discipline\\n      __typename\\n    }\\n    disciplines {\\n      id\\n      name\\n      __typename\\n    }\\n    results {\\n      discipline\\n      date\\n      competition\\n      country\\n      category\\n      race\\n      place\\n      result\\n      wind\\n      drop\\n      withWind\\n      withDrop\\n      score\\n      records\\n      remark\\n      eventId\\n      competitionId\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\",\"variables\":{\"allTimePersonalTop10Discipline\":\"%s\",\"id\":%s}}"
url = "https://graphql-prod-4612.prod.aws.worldathletics.org/graphql"
headers = {
  'X-Api-Key': 'da2-v55cdwh6kbfpdociwqcrzmbaiy',
  'Content-Type': 'application/json'
}

discipline_id = "10229534"
i = 0
for athlete in csvFile_in:
    athlete_id = athlete['id']
    response = requests.post(url, headers=headers, data=payload % (discipline_id, athlete_id))
    if (not response.status_code == 200):
        print("athlete %s %s could not be found" % (athlete_id, athlete['firstName'], athlete['lastName']))
        continue
    try: 
        raceResults = response.json()['data']['getSingleCompetitorAllTimePersonalTop10']['results']
        print("athlete %s %s has competed in %d races" % (athlete['firstName'], athlete['lastName'], len(raceResults)))
        for performance in raceResults:
            athlete1 = athlete.copy()
            performanceDate = dateparser.parse(performance['date'])
            perform = {
                'performanceDate': performanceDate.strftime("%Y-%m-%d"),
                'competition': performance['competition'], 
                'venueCountry': performance['country'], 
                'place': performance['place'].strip('.'),
                'eventId': performance['eventId'],
                'competitionId': performance['competitionId'],
                'timeResult': performance['result']
            }
            athlete1.update(perform)
            csvFile_out.writerow(athlete1)
    except TypeError:
        print("athlete %s %s %s type error" % (athlete_id, athlete['firstName'], athlete['lastName']))
    except Exception as e:
        print("athlete %s %s %s retrieval error, %s" % (athlete_id, athlete['firstName'], athlete['lastName'], e))
    i += 1
    
    
f_in.close()
f_out.close()