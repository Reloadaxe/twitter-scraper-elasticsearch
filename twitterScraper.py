from twitter_scraper import query_tweets
import datetime as dt
from elasticsearch import Elasticsearch
import spacy
from geopy.geocoders import Nominatim

def findCitiesAndCountriesInText(text):
    cities = []
    nlp = spacy.load("xx_ent_wiki_sm")
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "LOC":
            cities.append(ent.text)
    return cities

def convertCityToPosition(city):
    position = None
    geolocator = Nominatim(user_agent="my-application")
    try:
        location = geolocator.geocode(city)
        if location:
            position = str(location.latitude) + "," + str(location.longitude)
    except:
        pass
    return position

def createDatabase(es):
    if not es.indices.exists(index='informations'):
        mapping = '''
        {  
            "mappings":{  
                "properties": {
                    "location": {
                        "type": "geo_point"
                    }
                }
            }
        }'''
        es.indices.create(index='informations', body=mapping)

if __name__ == '__main__':
    es = Elasticsearch()
    createDatabase(es)
    tweetsAdded = 0
    keyword = input("Quel mot ou phrase voulez vous rechercher ?\n")
    start_year = int(input("A partir de quelle date ?\nAnnée : "))
    start_month = int(input("Mois : "))
    start_day = int(input("Jour : "))
    now = input("Jusqu'à aujourd'hui ? (O/n)")
    if now.upper() != "O":
        end_year = int(input("Jusqu'à quelle date ?\nAnnée : "))
        end_month = int(input("Mois : "))
        end_day = int(input("Jour : "))
        end_date = dt.date(end_year, end_month, end_day)
    else:
        end_date = dt.date.today()
    print("Début de la recherche..")
    tweets = query_tweets(keyword + " -filter:replies filter:verified", None, dt.date(start_year, start_month, start_day), end_date)
    for tweet in tweets:
        cities = findCitiesAndCountriesInText(tweet.text)
        cityId = 0
        for city in cities:
            position = convertCityToPosition(city)
            if position:
                information = {
                    'user': tweet.screen_name + " ( " + tweet.username + " )",
                    'keyword': keyword,
                    'address': city,
                    'location': position,
                    'description': tweet.text,
                    'timestamp': tweet.timestamp,
                }
                tweetsAdded += 1
                cityId += 1
                res = es.index(index="informations", id=tweet.tweet_id + "__" + str(cityId), body=information)
    print("Number of tweets added in elasticSearch : " + str(tweetsAdded))