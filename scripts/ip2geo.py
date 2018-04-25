import http.client, urllib.request, urllib.parse, urllib.error, base64
import csv
import io
import ipaddress
from copy import deepcopy

from scripts.csv2json import csv2json
from scripts.geocache import GeoCache
from scripts.iptree import IpTree


def download_blocked_csv():
    try:
        conn = http.client.HTTPSConnection('api.antizapret.info')
        conn.request("GET", "/all.php?type=csv")
        response = conn.getresponse()
        data = response.read()
        conn.close()
        with open('data/good.csv', 'wb') as f:
            f.write(data)
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

geo_cache = GeoCache()
ip_tree = IpTree()
ips4geo=set()

# with open('data/good.csv') as csvfile:
with io.StringIO(download_blocked_csv().decode("utf-8")) as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        ips = row[3].split(',')
        for ip in ips:
            ipsplit = ip.split('/')
            w = 1
            if len(ipsplit) == 2:
                sig_bits = 32 - int(ipsplit[1])
                w = 2 ** sig_bits
                ip = ipsplit[0]

            try:
                begin = int(ipaddress.IPv4Address(ip))
                entity = {'date': row[0], 'url': row[1], 'host': row[2], 'ip': ip, 'w': w}
                end = begin + w
                ip_tree.add_interval(begin, end, entity)
                ips4geo.add(ip)
            except ipaddress.AddressValueError:
                continue

geo_cache.update_ips(ips4geo)

ip_tree.update_w()
with open('data/points.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['lat', 'lon', 'ip', 'host', 'date', 'url', 'w'])

    for i in ip_tree.get_all():
        data = i.data
        coords = geo_cache.get(data['ip'])
        if coords is None:
            continue
        data['lat'] = coords[0]
        data['lon'] = coords[1]
        writer.writerow(data)

csv2json()