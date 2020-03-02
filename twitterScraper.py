from twitterscraper import query_tweets
import datetime as dt
from elasticsearch import Elasticsearch
import spacy
from geopy.geocoders import Nominatim

class TextColors:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    reset = '\033[0m'

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
    start_date = dt.date(start_year, start_month, start_day)
    print(TextColors.green + "Début de la recherche de '"+keyword+"' du " + str(start_date) + " au " + str(end_date) + TextColors.reset)
    tweets = query_tweets(keyword + " -filter:replies filter:verified", None, start_date, end_date)
    print(TextColors.green + "Tous les tweets ont été récupérés\nDébut de l'insertion dans elasticsearch.." + TextColors.reset)
    tweetsDone = 1
    for tweet in tweets:
        print(TextColors.yellow + str(tweetsDone) + " / " + str(len(tweets)) + TextColors.reset)
        cities = findCitiesAndCountriesInText(tweet.text)
        if not cities:
            print(TextColors.red + "Aucune ville trouvée" + TextColors.reset)
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
            else:
                print(TextColors.red + "Aucune position trouvée pour '"+city+"'" + TextColors.reset)
        tweetsDone += 1
    print(TextColors.green + "Nombre de tweets ajoutés dans ElasticSearch : " + str(tweetsAdded) + TextColors.reset)