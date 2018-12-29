#!/usr/bin/python

import sys
import requests
import json
import pandas as pd

count = 2122
currency = 'BTC'

###################################################################################

### TO BE UPDATED WITH PERSONAL API KEY (line 25)
### MORE INFO HERE: https://pro.coinmarketcap.com/signup 

###################################################################################


coins_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap' \
            + '&start=1&limit='+ str(count) + '&convert=' + str(currency)
            # + '&start=1&limit='+ str(count) + '&cryptocurrency_type=tokens&convert=' + str(currency)

btc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC&convert=USD'

header={'X-CMC_PRO_API_KEY':'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}

coins_data = requests.get(coins_url,headers=header).json()
btc_data = requests.get(btc_url,headers=header).json()

df = pd.DataFrame([btc_data['data']['BTC']],columns=btc_data['data']['BTC'].keys())

count = len(coins_data['data'])

for i in range(count-1):
    df = df.append(coins_data['data'][i+1],ignore_index=True )

df2 = df.quote.apply(pd.Series)
df3 = df2.USD.apply(pd.Series)
df4 = df2.BTC.apply(pd.Series)
df4 = df4.iloc[1:count]
df_quote = pd.concat([df3.iloc[[0]], df4], ignore_index=True)

df_platform = df.platform.apply(pd.Series)

df_base = df[df.columns.difference(['quote', 'platform'])]

frames = [df_base, df_quote, df_platform]
processed_df = pd.concat(frames, axis=1)

processed_df.to_csv('ccdata.csv')
