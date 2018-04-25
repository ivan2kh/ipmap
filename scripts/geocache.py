import csv
import http
import json
from time import sleep
import os

def download_geo(body):
    try:
        conn = http.client.HTTPConnection('ip-api.com')
        conn.request("POST", "/batch?fields=lat,lon", body)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

class GeoCache:
    def __init__(self):
        with open("data/geocache.csv") as f:
            reader = csv.reader(f, delimiter=',')
            self.cache = {row[2]: (row[0], row[1]) for row in reader}

    def update_ips(self, ips):
        missed = set()
        for ip in ips:
            if ip not in self.cache:
                missed.add(ip)

        missed = list(missed)
        count = 0
        for i in range(0, len(missed), 100):
            els = missed[i:i + 100]
            x = [{'query': i} for i in els]
            body = json.dumps(x)
            geo = download_geo(body)
            geo = json.loads(geo.decode("utf-8"))
            for index, g in enumerate(geo):
                if not 'lat' in g:
                    continue
                self.cache[els[index]] = (g['lat'], g['lon'])

            count += 1
            if count % 150 == 0:
                sleep(60)

        if len(missed):
            with open("data/geocache.csv", "a") as f:
                writer = csv.DictWriter(f, fieldnames=['lat', 'lon', 'ip'], delimiter=',')

                for ip in missed:
                    coords = self.cache.get(ip, None)
                    if coords is not None:
                        writer.writerow({'lat': coords[0], 'lon': coords[1], 'ip': ip})

    def get(self, ip):
        return self.cache.get(ip, None)
