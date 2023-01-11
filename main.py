import datetime
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Video import Video
from YtApiWrapper import YtApiWrapper


# TODO: consider moving these methods to the YtApiWrapper or some other class?
def getItems(_responses: list):
    output = list()
    for response in _responses:
        for item in response['items']:
            output.append(item)
    return output


def getVideoIds(_items: list):
    videoIds = list()
    for item in _items:
        if type(item) is dict and 'videoId' in item['id']:
            videoIds.append(item['id']['videoId'])
    return videoIds


api_key = open("yt_api_key.txt", 'r').read()
yt = YtApiWrapper(api_key)

channel_id = 'UCBURM8S4LH7cRZ0Clea9RDA'
# responses = yt.getAsManyVideosOf(channel_id)
# responses = yt.getVideo('VIDEO_ID_HERE')

# Read from file
with open("data.json", "r") as readfile:
    responses = json.load(readfile)
readfile.close()

print(responses)
video_test = Video(responses['items'][0])

# print(getItems(responses)[1])
# videos = getVideoIds(getItems(responses))

# for video in videos:
    # responses = yt.getVideo(video)
    # break # TODO: remove this

# with open("data.json", "w") as outfile:
#     json.dump(responses, outfile)
# outfile.close()
