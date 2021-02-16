import pandas as pd
import requests
from pathlib import Path

df = pd.read_csv(r'cats.csv', encoding='UTF-8', sep=';')

print(df.columns)


df['suffix'] = df['webformatURL'].apply(lambda x: Path(x).suffix)
df['filename'] = df['id'].map(str) + df['suffix']

counter = 500
for picture in df['webformatURL']:
    name = df.loc[ df['webformatURL'] == picture, 'filename'].values[0]
    filepath = 'images/' + name
    current_response = requests.get(picture)
    with open(filepath, 'wb') as ff:
        ff.write(current_response.content)
    counter -= 1
    print(f'{name} is download! {counter} left.')

