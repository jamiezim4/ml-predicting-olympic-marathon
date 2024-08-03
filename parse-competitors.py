import json
import csv

f_in = open("runners.json", "r")
data = json.load(f_in)

fields = ['id', 'iaafId', 'firstName', 'lastName', 'countryCode', 'countryName', 'birthDate']

# writing to csv file
f_out = open("competitors.csv", 'w')
writer = csv.DictWriter(f_out, fieldnames=fields)
writer.writeheader()

for athlete in data['data']['searchAthletes']:
    witer.writerow({
        'id': athlete['id'],
        'iaafId': athlete['iaafId'],
        'firstName': athlete['firstName'], 
        'lastName': athlete['lastName'], 
        'countryCode': athlete['countryCode'],
        'countryName': athlete['countryName'],
        'birthDate': athlete['birthDate'].split('T')[0]
        })

f_in.close()
f_out.close()