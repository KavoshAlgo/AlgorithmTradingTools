proxies = {}
count = 1
with open("Webshare_250_ proxies.txt", "r")as infile:
    for line in infile.readlines():
        items = line.replace("\n", "").split(":")
        proxies["proxy%s" % count] = {
            "order_count": 0,
            "cancel_count": 0,
            "proxies": {
                "http": "http://%s:%s@%s:%s" % (items[2], items[3], items[0], items[1]),
                "https": "http://%s:%s@%s:%s" % (items[2], items[3], items[0], items[1])
            },
            "ip_address": items[0],
            "orders_times": [],
            "cancel_times": []
        }
        count += 1
import json
with open('proxies', 'w+')as outfile:
    json.dump(proxies, outfile)
print(dict(list(proxies.items())[96:97]))
print(len(dict(list(proxies.items())[96:97])))