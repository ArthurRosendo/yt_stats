import datetime
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Channel import Channel
from Video import Video
from YtApiWrapper import YtApiWrapper

channel_id = 'CHANNEL-ID-HERE'
channel_test = Channel(channel_id)
channel_test.fetchAllVideos()

# Read from file
#with open("data.json", "r") as readfile:
#    responses = json.load(readfile)
#readfile.close()


#with open("data.json", "w") as outfile:
#    json.dump(responses, outfile)
#outfile.close()
