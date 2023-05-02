from src.mixin import Path


class Video(Path):

    def __init__(self, video_id):
        self.video_id = video_id
        self.service = self.get_videos

        self.channelId = self.service()['items'][0]['snippet']['channelId']
        self.title = self.service()['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/channel/{self.video_id}'
        self.video_count = int(self.service()['items'][0]['statistics']['viewCount'])
        self.like_count = int(self.service()['items'][0]['statistics']['likeCount'])

    def get_videos(self) -> None:
        """Выводит в консоль информацию о канале"""
        channel_info = self.response.videos().list(id=self.video_id, part='snippet,statistics').execute()
        return channel_info

    def __repr__(self):
        return f'[this class name: {self.__class__.__name__}]''\n'\
               f'[channelId: {self.channelId}]''\n'\
               f'[title: {self.title}]''\n'\
               f'[url: {self.url}]''\n'\
               f'[video_count: {self.video_count}]''\n'\
               f'[like_count: {self.like_count}]'

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id


