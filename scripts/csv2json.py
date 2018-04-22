import csv
import json

all = []
with open('ips.json', 'w') as outfile:
    with open('points.csv') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', fieldnames=['lat', 'lon', 'ip', 'host', 'date', 'url', 'w'])
        # for row in spamreader:
        #     print(row)
        all = [{'lat': row['lat'], 'lon': row['lon'], 'w': row['w']} for row in csvreader]
        json.dump(all, outfile)
