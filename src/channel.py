import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    title_channel = "youtube"
    prefix_channel = "v3"

    def __init__(self, channel_id: str, api_key: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = api_key
        self.response = build(self.title_channel, self.prefix_channel, developerKey=api_key)
        self.channel_info = self.response.channels().list(id=channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))


