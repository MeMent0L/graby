import sys
import requests
import json

def get_position(json):
    try:
        return int(json['position'])
    except KeyError:
        return 1000

count = 1200

# Getting data directly from Coinmarketcap API as of 18/11/2017

url = "https://api.coinmarketcap.com/v1/ticker/?limit=1200"

headers = ["Ticker","Name","Market Cap [USD]","Price [USD]","Price [BTC]","Available Supply","Max Supply",\
"Volume 24h [USD]","Change 1h", "Change 24h", "Change 7d"]

API_tickers_list=['symbol','market_cap_usd','price_usd','price_btc','available_supply','max_supply',\
'24h_volume_usd','percent_change_1h','percent_change_24h','percent_change_7d']

if len(sys.argv) == 2:
        count = int(sys.argv[1])

data = requests.get(url).text
data = json.loads(data)
data.sort(key=get_position)

table = []
text_output = []

for d in data[0:count]:

        d_name=re.sub(r'.*\n', "", d['name']).strip()

        for tickers in API_tickers_list:
            if d[tickers] is None:
                d[tickers] = 'n/a'

        table.append([d['symbol'],d_name,d['market_cap_usd'],d['price_usd'],d['price_btc'],d['available_supply'],d['max_supply'],\
        d['24h_volume_usd'],d['percent_change_1h'],d['percent_change_24h'],d['percent_change_7d']])

        #text_output.append(str(([d['symbol'],",",d['name'],",",d['marketCap'][currency],",",d['price'][currency],",",d['marketCap']['btc'],volume,",",d['change7h'][currency],"/n"]))

output_table = ','.join(headers) + "\n"

for lines in table:
    output_table += ','.join(lines) +"\n"


f = open("ccdata.txt", "w")
f.write(output_table)
