# ---------------------------------------------------------------------------------------------------------
# ENV & Import Config
from dotenv import load_dotenv
load_dotenv(verbose=True)
from pathlib import Path
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

from tqdm import tqdm
from pyyoutube import Api
import tweepy
import os
import sys
import bitly_api
import pprint
import time
import pymongo
sys.path.append(".")
client = pymongo.MongoClient(os.getenv('MONGO_DB_CONNECTION_STRING'))

from models.processedData import ProcessedData
from models.channelData import ChannelData
from models.style import Style
from models.woeidLocations import WoeidLocations
from models.locationTrends import LocationTrends

videoData = None
channelContent = None
processedData = []
processedChannelDataID = None

print('\n------------------------------------------')
print(sys.version, sys.platform, sys.executable)
print('\n\nInitalised\n')

def getDataFromMongoDB(find, collection):
  db = client[os.getenv('MONGO_DB_DATABASENAME')]
  return db[collection].find_one(find)

def saveDataToMongoDB(data, collection):
  db = client[os.getenv('MONGO_DB_DATABASENAME')]
  posts = db[collection]

  if (collection == 'youtubeDATA'):
    prevData = db[collection].find_one({ "channelName": data['channelName'] })
    if (prevData):
      return prevData['_id']

  return posts.insert_one(data).inserted_id

def fetchYoutubeData():
  global videoData
  global processedChannelDataID
  
  if videoData is None:
    try:
      print(Style['green'], '- Gathering youtube channel data...')

      api = Api(api_key=os.getenv('YOUTUBE_DATA_API_KEY'))
      channelById = api.get_channel_info(channel_id=os.getenv('YOUTUBE_CHANNEL_ID'))

      print('- Fetched youtube channel data...\n')
      print('- Gathering youtube video data...')

      channelUploadsPlaylistId = channelById.items[0].contentDetails.relatedPlaylists.uploads
      allChannelVideos = api.get_playlist_items(
        playlist_id=channelUploadsPlaylistId, 
        count=30, 
        limit=30
      )

      print('- Fetched youtube video data...\n')
      print('- Storing youtube video data...')
      videoData = allChannelVideos.items
      print('- Completed storing youtube video data...\n')

      print('- Storing youtube channel data...')

      processedChannelDataID = saveDataToMongoDB(
        {
          "thumbnail": channelById.items[0].snippet.thumbnails.high.url,
          "channelName": channelById.items[0].snippet.title,
          "channelDescription": channelById.items[0].snippet.description,
          "keywords": channelById.items[0].brandingSettings.channel.keywords.split()
        },
        "youtubeDATA"
      )

      print('- Completed storing youtube channel data...')
    except:
      print(Style['red'], '- An exception occurred\n' + Style['white'])
    else:
      print('- Completed gathering youtube data... \n' + Style['white'])

def processYoutubeData():
  global videoData
  global processedData
  if len(processedData) == 0:
    try:
      loop = tqdm(total=len(videoData), position=0, leave=False)

      for video in videoData:
        loop.set_description('- Processing video data...')
        connection = bitly_api.Connection(access_token=os.getenv('BITLY_API_ACCESS_TOKEN'))
        shortVideoUrl = connection.shorten('https://www.youtube.com/watch?v={0}'.format(video.contentDetails.videoId))
        
        processedData.append(
          ProcessedData(
            videoUrl=shortVideoUrl['url'],
            videoTitle=video.snippet.channelTitle,
            videoDescription=video.snippet.description,
          )
        )
        loop.update(1)
      loop.close()
    except:
      print(Style['red'], "- An exception occurred" + Style['white'])
    else:
      print(Style['green'], '- Finished Processing data...\n' + Style['white'])
  
def twitterBot():
  global processedChannelData
  global processedData

  def twitterAuthenticate():
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_KEY'), os.getenv('ACCESS_SECRET'))
    return tweepy.API(auth)

  api = twitterAuthenticate()

  def computeBestTrendingAreas():
    countryLoop = tqdm(total=len(WoeidLocations.keys()), position=0, leave=False)
    locationTrends = LocationTrends()

    def calcTimeDifference(epoch):
        timeA = round(time.time(), 2)
        timeB = round(epoch, 2)
        return int(timeB - timeA)

    for key in WoeidLocations.keys():
      countryLoop.set_description('- Started fetching trending country data for the {0}...'.format(key))
      currentRates = api.rate_limit_status(resources='trends')['resources']['trends']['/trends/place']

      def getLoactionData():
        for location in WoeidLocations[key]:
          locationTrends.setData(api.trends_place(id=location['id']), key)

      if currentRates['remaining'] >= len(WoeidLocations[key]): 
        getLoactionData()
      else:
        timeRemainingInSeconds = calcTimeDifference(currentRates['reset'])
        timeRunDownLoop = tqdm(total = timeRemainingInSeconds, position=0, leave=False)
        timeRunDownLoop.set_description('- API limit reached, please wait {0} minutes and it will finish the request...'.format(round(timeRemainingInSeconds / 60, 2)))

        while calcTimeDifference(currentRates['reset']) != 0:
          time.sleep(1)
          timeRunDownLoop.update(1)
        timeRunDownLoop.close()
        getLoactionData()

      countryLoop.update(1)
    countryLoop.close()

    print(Style['green'], '- Finished fetching trending data...\n')

    def buildBestTargetTrends():
      # Need to process all the city data to gather the most trafficked hashtags

      # Need to compaire keywords build up from the youtube channel data to work out which is the most relevent hashtags in the computed lists

      # Return top 10 hashtags based on that result
      return []
      
    return buildBestTargetTrends()

  def buildTweet(locationTrendsData):
    # build tweet from returned hashtags and youtube content
    return

  def sendTweet():
    global processedChannelDataID
    global getDataFromMongoDB

    youtubeData = getDataFromMongoDB({ "_id": processedChannelDataID }, "youtubeDATA")
    pprint.pprint(youtubeData)
    api.update_status(youtubeData['channelName'])
    return

  # locationTrendsData = computeBestTrendingAreas()
  # buildTweet(locationTrendsData)
  buildTweet('')
  sendTweet()

# --------------------
# Main Runner
fetchYoutubeData()
processYoutubeData()
twitterBot()