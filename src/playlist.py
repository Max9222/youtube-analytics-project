from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import datetime
import isodate

load_dotenv()

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:

    def __init__(self, channel_id):
        """Инициализируем id плейлиста и имеет следующие публичные атрибуты:
        - название плейлиста
        - ссылку на плейлист"""

        self.channel_id = channel_id

        playlists = youtube.playlists().list(id=channel_id, part='contentDetails,snippet', maxResults=50).execute()
        #print(playlists)

        for playlist in playlists['items']:
            self.title = playlist['snippet']['title']
            self.url = 'https://www.youtube.com/playlist?list=' + playlist['id']
            self.playlist_id = playlist['id']

        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        # получить все id видеороликов из плейлиста

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_ids = video_ids
        self.__video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()


    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста (обращение как к свойству, использовать `@property`)"""
        tm = datetime.timedelta(minutes=0)
        for video in self.__video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            tm += duration

        return tm


    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        m = []
        l = []
        for video_id in self.video_ids:
            #print(video_id)
            video_response = youtube.videos().list(id=video_id,
                                               part='snippet,statistics,contentDetails,topicDetails').execute()


            like_count = video_response['items'][0]['statistics']['likeCount']
            video_title = video_response['items'][0]['snippet']['title']
            m.append(video_id)
            l.append(like_count)

        max_v = max(l)
        num = l.index(max_v)
        return f'https://youtu.be/{m[num]}'






#if __name__ == '__main__':
    #pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
    #print(pl.title)
    #assert pl.url == "https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"

    #duration = pl.total_duration

    #print(str(duration))
    #assert str(duration) == "1:49:52"
    #assert isinstance(duration, datetime.timedelta)
    #assert duration.total_seconds() == 6592.0
    #dur = pl.show_best_video()
    #print(dur)
    #assert pl.show_best_video() == "https://youtu.be/cUGyMzWQcGM"