from datetime import datetime, timezone


class VideoStats:

    def __init__(self, videoId, viewCount, likeCount, favoriteCount, commentCount, _datetime:datetime=None):
        if _datetime is None:
            self.setDatetimeNow()
        else:
            self.datetime = _datetime
        self.videoId = videoId
        self.viewCount = viewCount
        self.likeCount = likeCount
        self.favoriteCount = favoriteCount
        self.commentCount = commentCount

    def setDatetimeNow(self):
        self.datetime = datetime.now(timezone.utc)
