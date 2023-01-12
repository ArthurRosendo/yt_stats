import json

from Video import Video
from YtApiWrapper import YtApiWrapper


class Channel:

    # Class variable
    api = YtApiWrapper(open("yt_api_key.txt", 'r').read())

    def __init__(self, channelId):
        self.channelId = channelId
        self.videos = list()

    def fetchAllVideos(self):
        #search_list_responses = Channel.api.getAsManyVideosOf(channel_id=self.channelId)

        # For testing: Read from file
        with open("data.json", "r") as readfile:
            search_list_responses = json.load(readfile)
        readfile.close()

        for search_list_response in search_list_responses:
            for item in search_list_response['items']:
                if type(item) is dict:
                    if 'id' in item:
                        if 'videoId' in item['id']:
                            if item['id']['videoId']:
                                video = Video(Channel.api.getVideo( item['id']['videoId'])['items'][0])
                                self.videos.append(video)
