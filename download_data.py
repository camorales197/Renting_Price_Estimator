import pandas as pd
import json
import urllib
import requests as rq
import base64
from dotenv import load_dotenv
import os


def get_oauth_token():

    url = "https://api.idealista.com/oauth/token"

    load_dotenv()
    apikey = os.environ.get("apikey")
    secret = os.environ.get("secret")
    apikey_secret = apikey + ':' + secret

    auth = str(base64.b64encode(bytes(apikey_secret, 'utf-8')))[2:][:-1]

    headers = {'Authorization' : 'Basic ' + auth,'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    params = urllib.parse.urlencode({'grant_type':'client_credentials'}) #,'scope':'read'
    content = rq.post(url,headers = headers, params=params)
    bearer_token = json.loads(content.text)['access_token']

    return bearer_token


def search_api(token, URL):
    headers = {'Content-Type': 'Content-Type: multipart/form-data;', 'Authorization' : 'Bearer ' + token}
    content = rq.post(url, headers=headers)
    print(content)
    result = json.loads(content.text)

    return result


country = 'es' #values: es, it, pt
locale = 'es' #values: es, it, pt, en, ca
language = 'es' #
max_items = '20000'
operation = 'rent'
property_type = 'homes'
order = 'distance'
center = '40.432765,-3.701102'
distance = '10000'
sort = 'desc'
bankOffer = 'false'

df_tot = pd.DataFrame()
limit = 1000

for i in range(1,limit):
    try:
        url = ('https://api.idealista.com/3.5/'+country+'/search?operation='+operation+#"&locale="+locale+
               '&maxItems='+max_items+
               '&order='+order+
               '&center='+center+
               '&distance='+distance+
               '&propertyType='+property_type+
               '&sort='+sort+
               '&numPage=%s'+
               '&language='+language) %(i)
        a = search_api(get_oauth_token(), url)
        df = pd.DataFrame.from_dict(a['elementList'])
        df_tot = pd.concat([df_tot, df])
    except:
        pass

df_tot = df_tot.reset_index()

df_tot.shape

df_tot.to_csv('data.csv', sep='\t', encoding='utf-8')
