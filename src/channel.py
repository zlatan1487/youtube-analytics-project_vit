import json
import os

import googleapiclient
from googleapiclient.discovery import build
from src.mixin import Path


class Channel(Path):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.service = Channel.get_service()

        # получаем информацию о канале
        video_response = self.service.channels().list(
            part='snippet,statistics',
            id=self.__channel_id
        ).execute()

        channel = video_response['items'][0]
        self.title = channel['snippet']['title']
        self.description = channel['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = int(channel['statistics']['subscriberCount'])
        self.video_count = int(channel['statistics']['videoCount'])
        self.view_count = int(channel['statistics']['viewCount'])

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале"""
        channel_info = self.response.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel_info, indent=2, ensure_ascii=False))

    def __repr__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    @classmethod
    def get_service(cls):
        """получаем объект для работы с API вне класса"""
        resource = googleapiclient.discovery.build('youtube', 'v3', developerKey=cls.api_key)
        return resource

    def to_json(self, filename):
        """создаем и сохраняем в файл значения атрибутов экземпляра Channel"""
        data = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.video_count
        }

        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        return self.__channel_id
