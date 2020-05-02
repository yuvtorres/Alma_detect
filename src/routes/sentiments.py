from src.app import app
from pymongo import MongoClient
from src.config import DB_ALMA
from bson.json_util import dumps
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

client = MongoClient(DB_ALMA)
db=client["db_alma"]
sia=SentimentIntensityAnalyzer()
 
### Module to solve sentiments routes

## calculate the sentiments of a chat
@app.route("/sentiment/<chat>/")
def sentiment_chat(chat):
    mensajes=db.mensajes.find({"chat":chat},{"_id":0,"user":1,"content":1})
    j_mensajes=json.loads(dumps(mensajes)[1:-1])
    print(sia.polarity_scores(j_mensajes['content']))
    return j_mensajes


