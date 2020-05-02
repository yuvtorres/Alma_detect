from flask import request
from src.app import app
from src.config import DB_ALMA,PORT,SERV_ALMA
import requests
import random
import json
from pymongo import MongoClient

from src.helpers.errorHandler import errorHandler, Error404

# Connect to Mongo DB
client = MongoClient(DB_ALMA,PORT)
db = client['db_alma']

# Open the json file with chats
with open('data/quotes-100-en.json') as f:
    file_data = json.load(f)

# Main function, generates the chats
@app.route("/genera_chat/", methods=['GET'])
@errorHandler
def genera_chats_y_users():
    # receive the optional params
    num_chats=request.args.get('num_chats')
    if not num_chats:
        num_chats=20

    num_users=request.args.get('num_users')
    if not num_users:
        num_users=140

    # Fill the user collection in db alma
    if not genera_users(num_users):
        return {"Error":"Error generating users please contact the admin" }
    # Fill the chats collection in db alma
    if not genera_chat(num_chats,num_users):
         return {"Error":"Error generating chats please contact the admin" }

    # Fill the message collection in db alma
    num_mensajes=20*num_users*num_chats

    if not genera_message(num_mensajes):
          return {"Error":"Error generating messages please contact the admin" }

    return {"Sucess": f" {num_chats}  were created with {num_users} users"}

# Function that generate the user, fill the collection "users"
def genera_users(num_users):
    users=[user for user in file_data.keys()]
    if num_users>len(users):
        return { "error" : f"The number of users exceed the maximum of {len(users)}"}

    users_bd = random.sample(users,num_users)
    res=[requests.get(SERV_ALMA+'/new_user/'+user+'/').status_code for user in users_bd]
    
    if res.count(200)==len(users_bd):
        print('*** users added to the DB successfully ***')
        return True
    else:
        print('*** problems when it was tried to create users ***')
        print(type(res[1]),len(users_bd))
        return False


# Function that generate the chats, fill the collection "chats"
def genera_chat(num_chats,num_users): 
    n_u_average=int(num_users/num_chats)
    if n_u_average<5:
        num_chats=int(num_users/5)
        print(f"the average number of user is set to 5 and the groups to {num_chats}")
        n_u_average=5
    # generates a distribution of user randomly between the chats
    num_user_chats=[random.randrange(n_u_average-3,n_u_average+3,1) for i in range(num_chats-1)]

    num_user_chats.append(num_users-sum(num_user_chats))

    if not validate_nuc(num_user_chats,num_users,num_chats):
        return {"error": "error generating the chats"}

   # fill the collection of chats
    res=[requests.get(SERV_ALMA+'/new_chat/chat'+str(i)+'/').status_code for i in range(num_chats)]

    if res.count(200)==num_chats:
        print('*** chats successfully created ***')
    else:
        print('*** problems when it was tried to create chats ***')
        return False

    # get the users in DB
    users=list( db.usuarios.find( {} , {"_id":0,"name":1} ).limit(num_users) )
    print(f'*** We are going to distibuite {len(users)} users ***')

    # Fill chats with users
    n_chat=0
    n_usuario=0
    while users !=[]:
        users_add=users[0:num_user_chats[n_chat]] # User to be added
        n_usuario+=len(users_add)
        users=users[num_user_chats[n_chat]:] # update the list of user
        res=[requests.get(SERV_ALMA+'/chats/chat'+str(n_chat)+'/'+user['name']+'/'
            ).status_code for user in users_add]

        if res.count(200)<len(users_add):
            return {"error":f"It was not possible to add users to chat{n_chat}"}

        n_chat+=1
    return True

# function to validate if the users was well distributed
def validate_nuc(nuc,num_users,num_chats):
    if sum(nuc)!=num_users:
        print(f"**** Group dont sum num_users:{num_users}")
        print(nuc)
        return False

    if min(nuc)<2:
        print("**** Group less than 2")
        return False

    if len(nuc)!=num_chats:
        print("**** Diffents num_chats")
        return False

    return True


def genera_message(num_mensajes):
    k=0
    while k < num_mensajes:
        result = list(db.chats.aggregate([  { '$sample': { 'size': 1  } } ] ) )
        chat=result[0]['chat']
        usuario=result[ 0 ][ 'users' ][ random.randint(0, len(result[0]['users'])-1 ) ]
        mensajes=file_data[usuario] 
        mensaje=mensajes[random.randint(0,len(mensajes)-1)]
        d_mensaje={"chat":chat,"user":usuario,"content":mensaje}
        res=requests.post(SERV_ALMA+'/message/',json=d_mensaje)

    return True


