#!/bin/bash

source .env
LOCALDBURI=$DB_ALMA
echo "WARNING!!! REMOTE DATA WILL BE DESTROYED"
echo "Copy from $DB_ALMA/db_alma"
echo "Paste your MongoDBAtlas URI:"
read REMOTEDBURI
echo "Sync data from $LOCALDBURI to $REMOTEDBURI"

mongodump --uri $LOCALDBURI
mongorestore --uri $REMOTEDBURI --drop
