import isodate

from src.mixin import Path
from datetime import timedelta


class PlayList(Path):
    """класс `PlayList`"""
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_title()
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

        self.content = self.get_content()

    def get_title(self):
        # метод возвращает название плейлиста
        playlist_response = self.response.playlists().list(part="contentDetails,snippet", id=self.playlist_id).execute()
        return playlist_response['items'][0]['snippet']['title']

    def get_content(self):
        # метод возвращает информацию о плейлисте
        playlist_videos = self.response.playlistItems().list(playlistId=self.playlist_id, part='contentDetails', maxResults=50).execute()

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # вывести длительности видеороликов из плейлиста
        video_response = self.response.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()
        return video_response

    @property
    def total_duration(self):
        """
        `total_duration` возвращает объект класса `datetime.timedelta` с
        суммарной длительность плейлиста
        """
        total_duration = timedelta()
        for video in self.content['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """
        `show_best_video()` возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        video_ids = [int(video['statistics']['likeCount']) for video in self.content['items']]
        max_value = max(video_ids)
        link = ''.join([video['id'] for video in self.content['items'] if int(video['statistics']['likeCount']) == max_value])
        return f'https://youtu.be/{link}'

