# from polyglot.text import Text
#
# from polyglot.detect import Detector
# pol = Text("отвратительно и унизительно", hint_language_code="ru").polarity
# print(pol)

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import csv
import sys
import json
from time import sleep

def getgeo(body):
    try:
        conn = http.client.HTTPConnection('ip-api.com')
        conn.request("POST", "/batch?fields=lat,lon", body)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

allips = []
with open('good.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in spamreader:
        ips = row[3].split(',')
        for ip in ips:
            allips.append({'date':row[0], 'url': row[1], 'host':row[2], 'ip': ip})


with open('out.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['lat', 'lon', 'ip', 'host', 'date', 'url'])

    count = 0
    for i in range(0, len(allips), 100):
        els = allips[i:i+100]
        x = [{'query': i['ip']} for i in els]
        body = json.dumps(x)
        geo = getgeo(body)
        geo = json.loads(geo.decode("utf-8") )
        for index, g in enumerate(geo):
            if not 'lat' in g:
                continue
            rec = {'lat': g['lat'], 'lon': g['lon'], 'ip': els[index]['ip'], 'host': els[index]['host'],
                   'date': els[index]['date'], 'url': els[index]['url']}
            writer.writerow(rec)
    count += 1
    if count % 150 == 0:
        sleep(60)
sys.exit()



