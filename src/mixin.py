import os
from googleapiclient.discovery import build


class Path:
    """Класс миксин, хранит api канала и запрос к сайту"""

    api_key: str = os.getenv('YOUTUBE_API')
    response = build('youtube', 'v3', developerKey=api_key)
