from src.mixin import Path
from googleapiclient.errors import HttpError


class Video(Path):
    def __init__(self, video_id):
        self.video_id = video_id
        self.service = self.get_videos()

        try:
            video_info = self.service['items'][0]
            self.channelId = video_info['snippet']['channelId']
            self.title = video_info['snippet']['title']
            self.url = f'https://www.youtube.com/channel/{self.video_id}'
            self.video_count = int(video_info['statistics']['viewCount'])
            self.like_count = int(video_info['statistics']['likeCount'])
        except (HttpError, IndexError):
            self.channelId = None
            self.title = None
            self.url = None
            self.video_count = None
            self.like_count = None

    def get_videos(self):
        """Returns channel information."""
        channel_info = self.response.videos().list(id=self.video_id, part='snippet,statistics').execute()
        return channel_info

    def __repr__(self):
        return (
            f'[this class name: {self.__class__.__name__}]\n'
            f'[channelId: {self.channelId}]\n'
            f'[title: {self.title}]\n'
            f'[url: {self.url}]\n'
            f'[video_count: {self.video_count}]\n'
            f'[like_count: {self.like_count}]'
        )

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id


