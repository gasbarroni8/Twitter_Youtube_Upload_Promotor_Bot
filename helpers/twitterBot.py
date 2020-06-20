from helpers.consoleMessages import successMessage
from helpers.consoleMessages import errorMessage
from helpers.mongo import getDataFromMongoDB
from helpers.twitterRetryPolicy import twitterRetryPolicy

from models.woeidLocations import WoeidLocations
from models.locationTrends import LocationTrends

from tqdm import tqdm
import tweepy
import os

def twitterBot(processedChannelDataID):
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

    successMessage('- Finished fetching trending data...')
    successMessage('- Storing location trend data')

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
    youtubeData = getDataFromMongoDB({ "_id": processedChannelDataID }, "youtubeChannelData")
    api.update_status(youtubeData['channelName'])
    return

  buildTweet(computeBestTrendingAreas())
  sendTweet()