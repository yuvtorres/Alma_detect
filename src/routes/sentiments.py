from src.app import app
from pymongo import MongoClient
from src.config import DB_ALMA
from bson.json_util import dumps
from flask import jsonify
import pandas as pd
import numpy as np
import seaborn as sns
import json
import nltk
import matplotlib.pyplot as plt

sns.set(style="darkgrid")

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

client = MongoClient(DB_ALMA)
db=client["db_alma"]
sia=SentimentIntensityAnalyzer()
 
### Module to solve sentiments routes

## calculate the sentiments of a chat
@app.route("/sentiment/<chat>/")
def sentiment_chat(chat,graph=True):
    mensajes=list( db.mensajes.find({"chat":chat},
        {"_id":0,"user":1,"content":1}) )

    polarity = [ sia.polarity_scores(mensaje['content']) for mensaje in mensajes]

    positive=[ele['pos'] for ele in polarity]

    negative=[ele['neg'] for ele in polarity]

    neutro=[ele['neu'] for ele in polarity]

    compound=[ele['compound'] for ele in polarity]
    d={"positive":positive,"negative":negative,"neutro":neutro,
            "compound":compound}
    df=pd.DataFrame(data=d)
    df= df.replace(0, np.NaN)

    # Create the graph
    if graph:
        f, axes = plt.subplots(1, 2, figsize=(6, 4), sharex=True)
        sns.distplot(df.positive, kde=False, rug=True, color="b", ax=axes[0])
        sns.distplot(df.negative, kde=False, rug=True, color="r", ax=axes[1])

        plt.savefig('src/templates/sentiment.png')

    # Write in sentiment colletion
    chat_sentiment={"chat":chat,
            "Pos":df.positive.mean(),
            "Neg":df.negative.mean(),
            "neu":df.neutro.mean(),
            "compound":df.compound.mean()}

    # in case the graph is True, it checks if chat as bee already
    # inserted in sentiment

    if graph:
        if db.sentiment.find_one({"chat":chat}):
            return jsonify(chat_sentiment)


    if db.sentiment.insert_one(chat_sentiment).inserted_id:
        print(f'*** write sentiments of chat {chat}')

    return {"chat":chat,
            "Pos":df.positive.mean(),
            "Neg":df.negative.mean(),
            "neu":df.neutro.mean(),
            "compound":df.compound.mean()}


