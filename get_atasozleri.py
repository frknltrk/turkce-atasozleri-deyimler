# https://tr.wiktionary.org/wiki/Kategori:Türkçe_atasözleri
# https://tr.wiktionary.org/wiki/Kategori:Türkçe_deyimler

# https://tr.wiktionary.org/wiki/%C3%96zel:ApiHelp
# https://mediawiki.org/wiki/API:Categorymembers/tr#Python
# https://mediawiki.org/wiki/API:Parsing_wikitext/tr#Python
# https://tr.wiktionary.org/w/api.php?action=query&list=categorymembers&cmtitle=Kategori:Türkçe_atasözleri&cmlimit=20

import pandas as pd
import requests
import os

S = requests.Session()

URL = "https://tr.wiktionary.org/w/api.php"
    
PARAMS_1 = {
    "action": "query",
    "cmtitle": "Kategori:Türkçe_atasözleri",
    "cmlimit": "max",
    "list": "categorymembers",
    "format": "json"
}

pages = []

while True:
    R = S.get(url=URL, params=PARAMS_1)
    data = R.json()

    pages.extend(data['query']['categorymembers'])

    try:
        PARAMS_1['cmcontinue'] = data['continue']['cmcontinue']
    except KeyError:
        break
        
#print(len(pages))

PARAMS_2 = {
    "action": "parse",
    "pageid": "0",
    "prop": "wikitext", 
    "format": "json"
}

all_pages = []

for i,p in enumerate(pages):
    PARAMS_2['pageid'] = p['pageid']
    R = S.get(url=URL, params=PARAMS_2)
    data = R.json()['parse']
    all_pages.append(data)
    print(f'{i+1}/{len(pages)}')

print("CSV tablosu yaratılıyor...")

df = pd.DataFrame(all_pages)
df.to_csv(f'atasozleri.csv')

print("Bitti.")
