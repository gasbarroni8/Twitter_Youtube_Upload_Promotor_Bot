# ---------------------------------------------------------------------------------------------------------
# ENV & Import Config
from dotenv import load_dotenv
load_dotenv(verbose=True)
from pathlib import Path
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

import sys
sys.path.append(".")

from helpers.youtube import fetchYoutubeData
from helpers.youtube import processYoutubeData
from helpers.twitterBot import twitterBot

print('\n\n------------------------------------------------------------------------------------')
print(sys.version, sys.platform, sys.executable)
print('\n\nInitalised\n')

# --------------------
# Main Runner
processedChannelDataID = fetchYoutubeData()
processYoutubeData(processedChannelDataID)
twitterBot(processedChannelDataID)