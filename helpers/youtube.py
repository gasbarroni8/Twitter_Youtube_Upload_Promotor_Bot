from helpers.consoleMessages import successMessage
from helpers.consoleMessages import errorMessage
from helpers.mongo import saveDataToMongoDB
from helpers.mongo import getDataFromMongoDB
from helpers.mongo import updateDataFromMongoDB
from pyyoutube import Api
from tqdm import tqdm
import bitly_api
import time
import os

def fetchYoutubeData():
  processedChannelDataID = None

  try:
    successMessage('- Gathering youtube channel & video data...')

    api = Api(api_key=os.getenv('YOUTUBE_DATA_API_KEY'))
    channelById = api.get_channel_info(channel_id=os.getenv('YOUTUBE_CHANNEL_ID'))

    successMessage('- Fetched youtube channel & video data...')

    uploadsPlaylistId = channelById.items[0].contentDetails.relatedPlaylists.uploads
    allChannelVideos = api.get_playlist_items(playlist_id=uploadsPlaylistId, count=30, limit=30)
    successMessage('- Constructing youtube channel & video data...')

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
        "keywords": channelById.items[0].brandingSettings.channel.keywords.split(),
        "resetAt": round(time.time())
      },
      "youtubeChannelData"
    )
    saveDataToMongoDB(
      { 
        "_id": processedChannelDataID, 
        "channelName": channelById.items[0].snippet.title, 
        "videos": processedData ,
        "resetAt": round(time.time()),
        "hasBeenProcessed": False
      }, 
      "youtubeVideoData"
    )
    successMessage('- Completed storing youtube video & channel data...')
  except:
    errorMessage('- An exception occurred')
  else:
    successMessage('- Completed youtube data step... ')

  return processedChannelDataID

def processYoutubeData(processedChannelDataID):
  successMessage('- Processing youtube data step... ')
  fetchedData = getDataFromMongoDB({ "_id": processedChannelDataID }, "youtubeVideoData")

  if len(fetchedData['videos']) > 0:
    try:
      loop = tqdm(total=len(fetchedData['videos']), position=0, leave=False)
      processedData = []

      for video in fetchedData['videos']:
        loop.set_description('- Processing video data...')
        connection = bitly_api.Connection(access_token=os.getenv('BITLY_API_ACCESS_TOKEN'))
        shortVideoUrl = connection.shorten('https://www.youtube.com/watch?v={0}'.format(video['videoUrl']))
        
        processedData.append({
          "videoUrl": shortVideoUrl['url'],
          "videoTitle": video['videoTitle'],
          "videoDescription": video['videoDescription'],
        })
        loop.update(1)
      loop.close()

      fetchedData['processedVideos'] = processedData
      updateDataFromMongoDB(fetchedData, { "_id": processedChannelDataID }, 'youtubeVideoData')
    except:
      errorMessage("- An exception occurred")
    else:
      successMessage('- Finished Processing data...')