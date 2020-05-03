# Alma - API for Sentiment Analysis

## Introduction 

Alma is an API for sentiment analysis in chats. It evaluate the general sentiment in the chat
using 

## Use

### Routes

#### Users

`/new_user/<name>/`	-> To add new users

`/users/`		-> To list the users

#### Chats

`/new_chat/<chat_name>/`	-> To create a new chat <chat_name>

`/chats/`			-> To list the chats

'/chats/<chat_name>/<user>/	-> To add an user <user> to the chat <chat_name>

`/chats/<chat_name>/`		-> Query of the users in <chat_name>

#### Messages

`/message/` 			-> Endpoint to send messages, the message 
				should be a POST JSON with the following 
				structure: 

	{"chat":<chat_name>, "user":<user_name>, "content":<message> }

`/message/<chat_name>/`		-> query all the messages in <chat_name>

`/message_u/<user_name>/`	-> query with the messages of <user_name>

#### Tools

`/genera_chat/`			-> Fill ramdomly the db from quotes-100.json 
				   the proccess could take time. 
				It can receive optional argument as GET params:
				- num_chats (default 20) : Number of chats to create
				- num_users (default 140) : Number of total users to distribuite
				  in the chat

`/sentiment/<chat_name>/'	-> Return the sentiment analysis of the chat <chat_name>

`/sentiment/			-> Makes the general analisys of the chats and return a json
				   with the mean values (positive, negative, neutro, content)
				   and a link with a graph

## Test it
