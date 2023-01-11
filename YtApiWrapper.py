import json
import os.path

from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from googleapiclient.errors import HttpError


class YtApiWrapper:

    # region Quota management vars
    PATH_FILE_TOKEN = "search_token.json"
    PATH_FILE_QUOTA = "current_quota.txt"
    current_quota = 0
    QUOTA_MAX = 10000
    QUOTA_SEARCH = 100
    QUOTA_VIDEO_LIST = 1
    # endregion

    def __init__(self, _api_key):
        self.api_key = _api_key  # open("yt_api_key.txt", 'r').read()
        self.service = build('youtube', 'v3', developerKey=self.api_key)
        YtApiWrapper.readQuotaFile()
        self.nextSearchTokens = dict()  # key: channelId, value: token
        self.readFileSearchToken()

    # region Utility
    def resetSearchTokenForChannel(self, channel_id):
        self.nextSearchTokens[channel_id] = None
    #endregion

    def updateSearchTokenForChannel(self,_channel_id,_token):
        self.nextSearchTokens[_channel_id] = _token
        
    def updateFileSearchToken(self):
        with open(YtApiWrapper.PATH_FILE_TOKEN, "w") as outfile:
            json.dump(self.nextSearchTokens, outfile)
        outfile.close()

    def readFileSearchToken(self):
        if os.path.exists(YtApiWrapper.PATH_FILE_TOKEN):
            with open(YtApiWrapper.PATH_FILE_TOKEN, "r") as readfile:
                self.nextSearchTokens = json.load(readfile)
            readfile.close()
        else:
            self.nextSearchTokens = dict()
            self.updateFileSearchToken()

    #region Main functionality
    def getAsManyVideosOf(self, channel_id):
        """ Search for as many videos from the specified channel as the quota allows it from newest to oldest, starting from the last page that it stopped at """
        responses = list()
        next_page_token = self.nextSearchTokens.get(channel_id) if not None else None
        try:
            while True:
                if self.consumeQuota(YtApiWrapper.QUOTA_SEARCH):
                    request = self.service.search().list(part='snippet', channelId=channel_id, order="date", safeSearch="none", maxResults=50, pageToken=next_page_token)
                    response = request.execute()
                    responses.append(response)
                    next_page_token = response.get('nextPageToken')
                    self.updateSearchTokenForChannel(channel_id, next_page_token)
                    if not next_page_token:  # No more pages
                        self.resetSearchTokenForChannel(channel_id)
                        break
                else:
                    print("Could not consume API.")
                    break # Quit the loop if it can't consume
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        return responses

    def getVideo(self, video_id):
        """Get information of the specific video"""
        response = None
        try:
            if YtApiWrapper.consumeQuota(YtApiWrapper.QUOTA_VIDEO_LIST):
                request = self.service.videos().list(part='snippet,statistics,contentDetails,liveStreamingDetails', id=video_id)
                response = request.execute()
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        return response
    #endregion

    #region QUOTA

    @staticmethod
    def consumeQuota(value: int):
        if value == 0:
            # Don't update the file if value is 0 - otherwise it messes with the quota reset
            return True

        #Consume and update the file if you have enough
        if YtApiWrapper.current_quota >= value > 0:
            YtApiWrapper.current_quota -= value
            YtApiWrapper.updateQuotaFile()
            return True
        else:
            print("Current quota is less than the API cost for an API operation")
            return False

    @staticmethod
    def readQuotaFile():
        try:
            quota_file = open(YtApiWrapper.PATH_FILE_QUOTA, 'r')
            split_file = quota_file.read().split(',')
            quota_file.close()

            #FIXME: This is not the correct way for checking for a quota refresh - should check if it past midnight PST/PDT
            last_time = datetime.strptime(split_file[0], "%Y-%m-%d %H:%M:%S.%f")
            last_time = last_time.replace(tzinfo=timezone.utc)
            now = datetime.now(tz=timezone.utc)
            if now - timedelta(hours=24) <= last_time <= now:
                # Read the quota; the quota has not reset.
                YtApiWrapper.current_quota = int(split_file[1])
            else:
                # 24h has past since last call - Quota has reset, update the file accordingly
                YtApiWrapper.current_quota = YtApiWrapper.QUOTA_MAX
                YtApiWrapper.updateQuotaFile()
        except FileNotFoundError:
            # File does not exist - create file
            YtApiWrapper.current_quota = YtApiWrapper.QUOTA_MAX
            YtApiWrapper.updateQuotaFile()

    @staticmethod
    def updateQuotaFile():
        YtApiWrapper.quota_file = open(YtApiWrapper.PATH_FILE_QUOTA, 'w')
        YtApiWrapper.quota_file.write(str(datetime.now()) + ',' + str(YtApiWrapper.current_quota))
        YtApiWrapper.quota_file.close()

    #endregion