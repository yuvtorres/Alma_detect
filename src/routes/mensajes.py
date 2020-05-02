from flask import request
from src.app import app
from pymongo import MongoClient
from src.config import DB_ALMA
from bson.json_util import dumps
import json

client = MongoClient(DB_ALMA)
db=client["db_alma"]

### Module to solve messages routes

## send a new message
@app.route("/message/", methods=['POST'])
def send_messages():
    mensaje=request.get_json()
    if mensaje:
        if consulta_chat(mensaje['chat']):
            if consulta_nombre_chat(mensaje['user'],mensaje['chat']):
                res=db.mensajes.insert_one({"user":mensaje['user'],
                    "chat": mensaje['chat'],
                    "content": mensaje['content'] } )
                return  {"Success": f"The message was send with id:{res}"}

            return {"error":"Please check if the user exist and insert the user in the chat"}
        return {"error":"Please create first the chat"}
    return {"error":"please past a json object by post"}

# query all messages of <chat>
@app.route("/message/<chat>/")
def message_chat(chat):
    if consulta_chat(chat):
        mensajes=db.mensajes.find({"chat":chat},{"_id":0,"user":1, "content":1})
        mensajes='{"messages":'+dumps(mensajes)+'}'
        mensajes_j=json.loads(mensajes)
        return mensajes_j

    return {"error":f"The chat {chat} don't exist"}

# function that return True if the user is already
# in DB False on the contrary
def consulta_nombre_chat(name,chat):
    if db.usuarios.find_one({"name":name}):
        return True
    return False

def consulta_chat(chat):
    if db.chats.find_one({"chat":chat}):
        return True
    return False

