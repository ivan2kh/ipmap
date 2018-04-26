import csv
import json
from collections import Counter


def csv2json():
    points = Counter()
    with open('data/points.csv') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', fieldnames=['lat', 'lon', 'ip', 'host', 'date', 'url', 'w'])
        # for row in spamreader:
        #     print(row)
        for row in csvreader:
            coord = (row['lat'], row['lon'])
            points[coord] += int(row['w'])

    with open('static/data/ips.json', 'w') as outfile:
        outfile.write("data = ")
        all_rows = [{'lat': coord[0], 'lon': coord[1], 'w': w} for coord, w in points.items()]
        json.dump(all_rows, outfile)


if __name__ == '__main__':
    csv2json()