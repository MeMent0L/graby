#!/usr/bin/python

import sys
import urllib2
import json
import re
from tabulate import tabulate

def get_position(json):
    try:
        return int(json['position'])
    except KeyError:
        return 1000

count = 1200
currency = "usd"
url = "http://coinmarketcap.northpole.ro/api/v5/all.json"
headers = ["Ticker","Name","Market Cap","Price","Available Supply","Volume 24h","Change 7h"]

if len(sys.argv) == 2:
        count = int(sys.argv[1])


data = urllib2.urlopen(url).read()
data = json.loads(data)['markets']
data.sort(key=get_position)
btc_price = float(data[0]['price'][currency])

table = []
text_output = []

for d in data[0:1]:
    volume = float(d['volume24']['btc'])*btc_price
    d_name=re.sub(r'.*\n', "", d['name']).strip() 
    table.append([d['symbol'],d_name,d['marketCap'][currency],d['price'][currency],d['marketCap']['btc'],volume,d['change7h'][currency]])

currency = "btc"
for d in data[1:count]:
        try:
            volume = float(d['volume24']['btc'])*btc_price
        except:
            volume = 0
        
        d_name=re.sub(r'.*\n', "", d['name']).strip()   
        table.append([d['symbol'],d_name,d['marketCap'][currency],d['price'][currency],d['marketCap']['btc'],volume,d['change7h'][currency]])

        #text_output.append(str(([d['symbol'],",",d['name'],",",d['marketCap'][currency],",",d['price'][currency],",",d['marketCap']['btc'],volume,",",d['change7h'][currency],"/n"]))

print table

#f = open("ccdata.txt", "w")
#f.write(tabulate(table,headers,numalign="left",stralign="left",floatfmt=".8f"))

