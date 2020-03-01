# twitter-scraper-elasticsearch

## Pré-requis

kibana, elasticsearch, python3 ( avec pip )

## Installation

```bash
git clone "https://github.com/Reloadaxe/twitter-scraper-elasticsearch.git"
cd twitter-scraper-elasticsearch

python3 -m pip install -r requirements.txt

python3 -m spacy download xx_ent_wiki_sm
```

## Utilisation

Lancer les serveurs elasticsearch et kibana.

Importer le fichier 'kibana_map_save.ndjson' dans kibana ( urlKibana/app/kibana#/management/kibana/objects?_g=() )

Pour ajouter des tweets :

```bash
python3 twitterScraper.py
```

Puis suivre les indications