  
import time
from tqdm import tqdm
from models.style import Style
from helpers.timeDifference import timeDifference

def twitterRetryPolicy(rateNumber):
    print(Style['white'])
    timeRemainingInSeconds = timeDifference(rateNumber)
    timeRunDownLoop = tqdm(total = timeRemainingInSeconds, position=0, leave=False)
    timeRunDownLoop.set_description(
      '- API limit reached, please wait {0} minutes and it will finish the request...'.format(round(timeRemainingInSeconds / 60, 2)))

    while timeRemainingInSeconds != 0:
      time.sleep(1)
      timeRunDownLoop.update(1)
    timeRunDownLoop.close()
    print(Style['green'])