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
import time
sys.path.append(".")

from models.style import Style
from models.woeidLocations import WoeidLocations
from models.locationTrends import LocationTrends
from helpers.mongo import saveDataToMongoDB
from helpers.mongo import getDataFromMongoDB
from helpers.timeDifference import timeDifference
from helpers.twitterRetryPolicy import twitterRetryPolicy
from helpers.consoleMessages import successMessage
from helpers.consoleMessages import errorMessage

processedChannelDataID = None

print('\n------------------------------------------')
print(sys.version, sys.platform, sys.executable)
print('\n\nInitalised\n')

def fetchYoutubeData():
  global processedChannelDataID

  try:
    successMessage('- Gathering youtube channel & video data...')

    api = Api(api_key=os.getenv('YOUTUBE_DATA_API_KEY'))
    channelById = api.get_channel_info(channel_id=os.getenv('YOUTUBE_CHANNEL_ID'))

    successMessage('- Fetched youtube channel & video data...\n')

    channelUploadsPlaylistId = channelById.items[0].contentDetails.relatedPlaylists.uploads
    allChannelVideos = api.get_playlist_items(
      playlist_id=channelUploadsPlaylistId, 
      count=30, 
      limit=30
    )

    successMessage('- Constructing youtube channel & video data...\n')
    
    processedData = []
    for video in allChannelVideos.items:
      processedData.append({
        "videoUrl": video.contentDetails.videoId,
        "videoTitle":video.snippet.channelTitle,
        "videoDescription": video.snippet.description,
      })

    successMessage('- Storing youtube video & channel data...')

    processedChannelDataID = saveDataToMongoDB(
      {
        "thumbnail": channelById.items[0].snippet.thumbnails.high.url,
        "channelName": channelById.items[0].snippet.title,
        "channelDescription": channelById.items[0].snippet.description,
        "keywords": channelById.items[0].brandingSettings.channel.keywords.split()
      },
      "youtubeChannelData"
    )
    saveDataToMongoDB({ "_id": processedChannelDataID, "videos": processedData }, "youtubeVideoData")
    
    successMessage('- Completed storing youtube video & channel data...\n')
  except:
    errorMessage('- An exception occurred\n')
  else:
    successMessage('- Completed youtube data step... \n')

# def processYoutubeData():
#   global videoData
#   global processedData
#   if len(processedData) == 0:
#     try:
#       loop = tqdm(total=len(videoData), position=0, leave=False)

#       for video in videoData:
#         loop.set_description('- Processing video data...')
#         connection = bitly_api.Connection(access_token=os.getenv('BITLY_API_ACCESS_TOKEN'))
#         shortVideoUrl = connection.shorten('https://www.youtube.com/watch?v={0}'.format(video.contentDetails.videoId))
        
#         processedData.append(
#           ProcessedData(
#             videoUrl=shortVideoUrl['url'],
#             videoTitle=video.snippet.channelTitle,
#             videoDescription=video.snippet.description,
#           )
#         )
#         loop.update(1)
#       loop.close()
#     except:
#       print(Style['red'], "- An exception occurred" + Style['white'])
#     else:
#       print(Style['green'], '- Finished Processing data...\n' + Style['white'])
  
def twitterBot():
  def twitterAuthenticate():
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_KEY'), os.getenv('ACCESS_SECRET'))
    return tweepy.API(auth)

  api = twitterAuthenticate()

  def computeBestTrendingAreas():
    countryLoop = tqdm(total=len(WoeidLocations.keys()), position=0, leave=False)
    locationTrends = LocationTrends()

    for key in WoeidLocations.keys():
      countryLoop.set_description('- Started fetching trending country data for the {0}...'.format(key))
      currentRates = api.rate_limit_status(resources='trends')['resources']['trends']['/trends/place']

      def getLoactionData():
        for location in WoeidLocations[key]:
          locationTrends.setData(api.trends_place(id=location['id']), key)

      if currentRates['remaining'] >= len(WoeidLocations[key]): 
        getLoactionData()
      else:
        twitterRetryPolicy(currentRates['reset'])
        getLoactionData()

      countryLoop.update(1)
    countryLoop.close()

    successMessage('- Finished fetching trending data...\n')

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

    youtubeData = getDataFromMongoDB({ "_id": processedChannelDataID }, "youtubeChannelData")
    api.update_status(youtubeData['channelName'])
    return

  locationTrendsData = computeBestTrendingAreas()
  # buildTweet(locationTrendsData)
  buildTweet('')
  sendTweet()

# --------------------
# Main Runner
fetchYoutubeData()
# processYoutubeData()
twitterBot()