from chat_downloader import ChatDownloader

from VideoStats import VideoStats
from YtApiWrapper import YtApiWrapper


class Video:

    api = YtApiWrapper(open("yt_api_key.txt", 'r').read())


    def __init__(self, _videoItem):
        ''' Constructor for video that takes a response of kind youtube#video'''

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

        self.chat = None

    def getThumbnailUrl(self, _videoItem):
        '''Returns url of the widest resolution thumbnail'''
        widest = 0
        widest_key = None
        for key in _videoItem['snippet']['thumbnails'].keys():
            current_key_width = _videoItem['snippet']['thumbnails'][key]['width']
            if current_key_width > widest:
                widest = current_key_width
                widest_key = key
        return _videoItem['snippet']['thumbnails'][widest_key]['url']

    def retrieveChat(self):
        ''' Downloads chat for past broadcasts'''
        if self.chat is None:
            print("Downloading chat for " + self.title + "...")
            chat_downloader = ChatDownloader()
            #Note: this doens't require API calls
            self.chat = chat_downloader.get_chat(url=f"https://youtube.com/watch?v="+self.id, message_types=['text_message', 'paid_message', 'membership_item', 'paid_sticker','sponsorships_gift_purchase_announcement'])
            print("Finished downloading")
        return self.chat