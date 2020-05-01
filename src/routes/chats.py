from src.app import app
from pymongo import MongoClient
from src.config import DB_ALMA
from bson.json_util import dumps
import json

client = MongoClient(DB_ALMA)
db=client["db_alma"]

### Module of the chats funcionalities

## makes the query of all chats
@app.route("/chats/")
def get_chats():
    chats=db.chats.find( { } ,{"_id":0,"chat":1})
    chats='{"chats":'+dumps(chats)+'}'
    chats_j=json.loads(chats)
    return chats_j

## insert new chat
@app.route("/new_chat/<name>/")
def insert_chat(name):
    if len(name)<30:
        if consulta_nombre(name):
            return {"error":"Name already in use"}

        chat_nuevo=db.chats.insert_one({"chat":name},{"users":[]}).inserted_id
        return {"success":f"the chat {name} was created"}
    return {"error":"The name can have maximum 30 characters"}

#  -- > function that return True if the chat is already
# in DB False on the contrary
def consulta_nombre(name):
    if db.chats.find_one({"chat":name}):
        return True
    return False

## insert an user to a chat
@app.route("/chats/<chat>/<user>/")
def insert_chat_user(chat,user):
    if consulta_nombre(chat):
        if consulta_nombre_user(user):
            if db.chats.find_one({"chat":chat,"users":user}):
                return {"Error":"The user is already in the chat"}
            
            chat_id=db.chats.find_one({"chat":chat})
            db.chats.update_one(
                    {"_id":chat_id['_id']},
                    {"$push": { "users": user } }
                               )
            return { "result":
                    f" The user: {user}, was added to {chat}"}


        return {"Error":"The user has not been created, please use /new_user/<name>/ to create it "}

    return {"Error":"The chat has not been created, please use /new_chat/<chat>/"}


# --> Function that consult if a name of user exist
def consulta_nombre_user(name):
    if db.usuarios.find_one({"name":name}):
        return True
    return False


## query the users of <chat_name>
@app.route("/chats/<chat>/")
def get_users_from_chat(chat):
    if consulta_nombre(chat):
        users=db.chats.find({"chat":chat},{"_id":0,"users":1})
        users='{"users":'+dumps(users)+'}'
        users_j=json.loads(users)
        return users_j

    return {"error":"The chat has not been created"}

