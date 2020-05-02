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

`/message/` 			-> Endpoint to send messages, the message should be a POST JSON
				with the following structure: {"chat":<chat_name>, "user":<user_name>, "content":<message> }

`/message/<chat_name>`		-> query all the messages in <chat_name>

#### Tools

`/genera_chat/`			-> Fill ramdomly the db from quotes-100.json 


## Test it
