import json
import os
from googleapiclient.discovery import build

YT_API_KEY = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.title = self.channel['items'][0]['snippet']['title']  # название канала
        self.description = self.channel['items'][0]['snippet']['description']  # описание канала
        self.url = f"https://www.youtube.com/channel/{self.channel['items'][0]['id']}"  # ссылка на канал
        self.subscribers = int(self.channel['items'][0]['statistics']['subscriberCount'])  # количество подписчиков
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])  # количество видео на канале
        self.view_count = int(self.channel['items'][0]['statistics']['viewCount'])  # общее количество просмотров

    def __str__(self):
        """Возвращает название и ссылку на канал: <название_канала> (<ссылка_на_канал>)"""
        return f"{self.title} ({self.url})"

    """
    Магические методы для сложения, вычитания и сравнения 2 каналов между собой.
    Все операции сравниваются по количеству подписчиков.
    """
    def __add__(self, other):
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        return self.subscribers - other.subscribers

    def __lt__(self, other):
        return self.subscribers < other.subscribers

    def __le__(self, other):
        return self.subscribers <= other.subscribers

    def __gt__(self, other):
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        return self.subscribers >= other.subscribers

    def __eq__(self, other):
        return self.subscribers == other.subscribers

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return print(channel)

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, file_name):
        """Метод, сохраняющий в файл значения атрибутов экземпляра `Channel`"""
        new_dict = {
            'id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'subscribers': self.subscribers,
            'video count': self.video_count,
            'view count': self.view_count
        }

        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(new_dict, file, ensure_ascii=False)
