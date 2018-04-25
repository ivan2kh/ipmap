import csv
import json


def csv2json():
    with open('static/data/ips.json', 'w') as outfile:
        with open('data/points.csv') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',', fieldnames=['lat', 'lon', 'ip', 'host', 'date', 'url', 'w'])
            # for row in spamreader:
            #     print(row)
            all_rows = [{'lat': row['lat'], 'lon': row['lon'], 'w': row['w']} for row in csvreader]
            json.dump(all_rows, outfile)
