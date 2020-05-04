from src.app import app
from pymongo import MongoClient
from src.config import DB_ALMA
from flask import jsonify
import pandas as pd
import numpy as np
import seaborn as sns
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
            "Pos":round(df.positive.mean(),4),
            "Neg":round(df.negative.mean(),4),
            "neu":round(df.neutro.mean(),4),
            "compound":round(df.compound.mean(),4)}

    # in case the graph is True, it checks if chat as bee already
    # inserted in sentiment

    if graph:
        if db.sentiment.find_one({"chat":chat}):
            return jsonify(chat_sentiment)


    if db.sentiment.insert_one(chat_sentiment).inserted_id:
        print(f'*** write sentiments of chat {chat}')

    return {"chat":chat,
            "Pos":round(df.positive.mean(),4),
            "Neg":round(df.negative.mean(),4),
            "neu":round(df.neutro.mean(),4),
            "compound":round(df.compound.mean(),4)}


## Calculate the sentiment of all chats
@app.route("/sentiment/")
def all_sentiment():
    chats=list(db.chats.find({},{"_id":0,"chat":1}))
    sentiments=[ sentiment_chat(chat['chat'],False) for chat in chats ]
    sent_dic={chat['chat']:[chat['Neg'],chat['Pos'],chat['compound'],chat['neu']]
        for chat in sentiments}

    survey (sent_dic,['Neg','Pos','compund','neu'])
    plt.savefig('src/templates/all_sentiments.png')
    print(sent_dic['chat0'])
    return {"sentiment":sent_dic['chat0']}


## Function taked from example mapplotlib
def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, str(round(c,3)), ha='center', va='center',
                    color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    return fig, ax





