import csv
import json

all = []
with open('ips.json', 'w') as outfile:
    with open('points.csv') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', fieldnames=['lat', 'lon', 'ip', 'host', 'date', 'url'])
        # for row in spamreader:
        #     print(row)
        all = [{'latitude': row['lat'], 'longitude': row['lon']} for row in spamreader]
        json.dump(all, outfile)
