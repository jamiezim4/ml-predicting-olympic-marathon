import requests
import json

payload = "{\"query\":\"query SearchAthletes($eventId: Int!, $countryCode: String, $disciplineCode: String, $sexCode: String, $searchValue: String){\\n  searchAthletes(eventId: $eventId, countryCode: $countryCode, disciplineCode: $disciplineCode, sexCode: $sexCode, searchValue: $searchValue) {\\n   id\\n    iaafId\\n    firstName\\n    lastName\\n    sexCode\\n    countryCode\\n    birthDate\\n    birthPlace\\n    birthPlaceCountryName\\n    disciplines {\\n      id\\n      updatedOn\\n      hash\\n      name\\n      typeCode\\n      typeName\\n      typeOrder\\n      order\\n      isRoad\\n      isCombined\\n      isOutdoor\\n      isValidIAAF\\n      nameUrlSlug\\n      typeNameUrlSlug\\n      __typename\\n    }\\n    competitionEntries {\\n      id\\n      eventId\\n      eventId_WA\\n      updatedOn\\n      hash\\n      sexCode\\n      countryCode\\n      countryName\\n      competitorId\\n      discipline {\\n        id\\n        updatedOn\\n        hash\\n        name\\n        typeCode\\n        typeName\\n        typeOrder\\n        order\\n        isRoad\\n        isCombined\\n        isOutdoor\\n        isWind\\n        isRelay\\n        isValidIAAF\\n        nameUrlSlug\\n        typeNameUrlSlug\\n        __typename\\n      }\\n      __typename\\n    }\\n  __typename\\n  }\\n}\\n\",\"variables\":{\"eventId\":\"7087\",\"disciplineCode\":\"MAR\",\"sexCode\":\"W\"}}"
url = "https://graphql-prod-4612.prod.aws.worldathletics.org/graphql"
headers = {
  'X-Api-Key': 'da2-v55cdwh6kbfpdociwqcrzmbaiy',
  'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)
if (not response.status_code == 200):
    print("Olympic Marathon competitors could not be found")

f_out = open('runners.json', 'w')
f_out.write(json.dumps(response.json()))