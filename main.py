import datetime
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from YtApiWrapper import YtApiWrapper

api_key = open("yt_api_key.txt", 'r').read()
yt = YtApiWrapper(api_key)

channel_id = 'ID HERE'
responses = yt.getAsManyVideosOf(channel_id)

#responses = yt.getVideo('VIDEO_ID_HERE')

with open("data.json", "w") as outfile:
    json.dump(responses, outfile)
outfile.close()

