import os
from googleapiclient.discovery import build
from datetime import timedelta
import isodate

YT_API_KEY = os.getenv('YT_API_KEY')


class PlayList:
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        # Получаем данные о плейлисте
        self.playlist = self.youtube.playlists().list(id=self.playlist_id, part='contentDetails,snippet').execute()
        # Получаем данные о видео в плейлисте
        self.playlist_items = self.youtube.playlistItems().list(part="contentDetails",
                                                                playlistId=self.playlist_id).execute()
        # Записываем ID видео в список
        video_list = [video['contentDetails']['videoId'] for video in self.playlist_items['items']]
        # Получаем данные видео по ID
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(video_list)).execute()

        self.title = self.playlist['items'][0]['snippet']['title']  # название плейлиста
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'  # ссылка на плейлист
        self.__total_duration = timedelta()

    @property
    def total_duration(self):
        """Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""
        total_time = timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            total_time += isodate.parse_duration(iso_8601_duration)
        self.__total_duration = total_time
        return self.__total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        max_likes = 0
        most_popular = 0
        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > max_likes:
                most_popular = video['id']
                max_likes = int(video['statistics']['likeCount'])

        return f"https://youtu.be/{most_popular}"
