import os
import pymongo
client = pymongo.MongoClient(os.getenv('MONGO_DB_CONNECTION_STRING'))

def getDataFromMongoDB(find, collection):
  db = client[os.getenv('MONGO_DB_DATABASENAME')]
  return db[collection].find_one(find)

def saveDataToMongoDB(data, collection):
  db = client[os.getenv('MONGO_DB_DATABASENAME')]

  if (collection == 'youtubeChannelDATA'):
    prevData = db[collection].find_one({ "channelName": data['channelName'] })
    if (prevData):
      return prevData['_id']
    
  posts = db[collection]
  return posts.insert_one(data).inserted_id