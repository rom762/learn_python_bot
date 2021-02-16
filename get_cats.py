import credentials
import json
import pandas as pd
from pprint import pprint
import requests

PIXABAY_API_KEY = credentials.PIXABAY_API_KEY
BASE_URL = 'https://pixabay.com/api/'


page = 1
per_page = 100
params = {
    'key': PIXABAY_API_KEY,
    'q': 'cats',
    'category': 'animals',
    'safesearch': True,
    'per_page': per_page,
    'page': page
}

df = pd.DataFrame()
while (page * per_page) < 501:
    print(page)
    response = requests.get(BASE_URL, params=params)
    tmp = pd.DataFrame.from_dict(response.json()['hits'])
    df = pd.concat([df, tmp])
    page += 1

df.to_csv('cats.csv', encoding='UTF-8', sep=';', index='index')

# parsed = json.load(data)
# pprint(parsed)
