import os
from googleapiclient.discovery import build

YT_API_KEY = os.getenv('YT_API_KEY')


class Video:
    """Создаем и инициализируем класс Video по ID видео"""
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, video_id):
        self.video_id = video_id
        # запрос статистики видео
        try:
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                 id=video_id
                                                                 ).execute()
            empty_video = self.video_response['items'][0]
        except IndexError:
            print('По данному ID видео не существует')
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
        else:
            self.title: str = self.video_response['items'][0]['snippet']['title']   # наименование видео
            self.url: str = f"https://youtu.be/{self.video_response['items'][0]['id']}"     # ссылка на видео
            self.view_count: int = int(self.video_response['items'][0]['statistics']['viewCount'])  # количество просмотров
            self.like_count: int = int(self.video_response['items'][0]['statistics']['likeCount'])  # количество лайков

    def __str__(self):
        """Вывод наименования видео для пользователя"""
        return self.title


class PLVideo(Video):
    """Создаем и инициализируем подкласс PLVideo от Vidoe по ID видео и ID плейлиста"""
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
