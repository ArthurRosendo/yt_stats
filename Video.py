from VideoStats import VideoStats


class Video:
    def validateResponse(self, _videoItem):
        if 'kind' in _videoItem:
            if _videoItem['kind'] != 'youtube#video':
                raise Exception("Invalid argument for Video, provided response is not of kind 'youtube#video'. If you inserted a search response please pass just the part of the response that corresponds to the video item.")
        else:
            raise Exception("Was not able to find 'kind' in response, provided argument is likely not a valid Youtube Data Api response")

    def __init__(self, _videoItem):

        self.validateResponse(_videoItem)

        self.id = _videoItem['id']
        self.channel_id = _videoItem['snippet']['channelId']
        self.title = _videoItem['snippet']['title']
        self.publish_date = _videoItem['snippet']['publishedAt']
        self.description = _videoItem['snippet']['description']
        self.thumbnail_url = self.getThumbnailUrl(_videoItem)
        # TODO: verify if this verification is necessary
        if 'defaultAudioLanguage' in _videoItem['snippet']:
            self.default_audio_language = _videoItem['snippet']['defaultAudioLanguage']
        else:
            self.default_audio_language = None
        self.licensed_content = _videoItem['contentDetails']['licensedContent']
        self.contentRating = _videoItem['contentDetails']['contentRating']

        self.stats = list()
        current_stats = VideoStats(self.id, _videoItem['statistics']['viewCount'], _videoItem['statistics']['likeCount'], _videoItem['statistics']['favoriteCount'], _videoItem['statistics']['commentCount'])
        self.stats = self.stats.append(current_stats)

    def getThumbnailUrl(self, _videoItem):
        widest = 0
        widest_key = None
        for key in _videoItem['snippet']['thumbnails'].keys():
            current_key_width = _videoItem['snippet']['thumbnails'][key]['width']
            if current_key_width > widest:
                widest = current_key_width
                widest_key = key
        return _videoItem['snippet']['thumbnails'][widest_key]['url']
