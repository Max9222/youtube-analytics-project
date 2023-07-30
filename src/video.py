from googleapiclient.discovery import build
from dotenv import load_dotenv
import os


load_dotenv()

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

class Video:
    def __init__(self, video_id):
        """Реализуем инициализацию реальными данными следующих атрибутов экземпляра класса `Video`:
        - id видео
        - название видео
        - ссылка на видео
        - количество просмотров
        - количество лайков"""

        self.video_id = video_id

        video_response = youtube.videos().list(id=video_id, part='snippet,statistics,contentDetails,topicDetails').execute()

        self.video_title = video_response['items'][0]['snippet']['title']
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']
        self.comment_count = video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        """Печатает название Видео"""
        return f'{self.video_title}'

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """Реализуем инициализацию реальными данными следующих атрибутов экземпляра класса `PLVideo`:
        - id видео
        - название видео
        - ссылка на видео
        - количество просмотров
        - количество лайков
        - id плейлиста"""
        super().__init__(video_id)
        self.playlist_id = playlist_id


video1 = Video('AWX4JnAnjBE')
video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')

print1 = str(video1)
print2 = str(video2)
print(print1)
print(print2)
