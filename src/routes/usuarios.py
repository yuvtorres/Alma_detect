from src.app import app
from pymongo import MongoClient
from src.config import DB_ALMA
from bson.json_util import dumps
import json

client = MongoClient(DB_ALMA)
db=client["db_alma"]

# makes the query of all users
@app.route("/users/")
def get_usuarios():
    usuarios=db.usuarios.find( { } ,{"_id":0,"name":1})
    usuarios='{"users":'+dumps(usuarios)+'}'
    usuarios_j=json.loads(usuarios)
    return usuarios_j

# insert new user
@app.route("/new_user/<name>/")
def insert_user(name):
    if len(name)<30:
        if consulta_nombre(name):
            return {"error":"Name already in use"}

        usuario_nuevo=db.usuarios.insert_one({"name":name}).inserted_id
        return {"success":f"the user {name} was created"}
    return {"error":"The name can have maximum 30 characters"}

# function that return True if the user is already
# in DB False on the contrary
def consulta_nombre(name):
    if db.usuarios.find_one({"name":name}):
        return True
    return False

