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
            #print(playlist)
            print()
            self.title = playlist['snippet']['title']
            self.url = 'https://www.youtube.com/playlist?list=' + playlist['id']
            self.playlist_id = playlist['id']


    def total_duration(self):


        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        # printj(playlist_videos)

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        # print(video_ids)

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        print(video_response)

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            print(duration)





if __name__ == '__main__':
    pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
    print(pl.title)
    assert pl.url == "https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"

    duration = pl.total_duration
    print(duration)
    #assert str(duration) == "1:49:52"
    #assert isinstance(duration, datetime.timedelta)
   # assert duration.total_seconds() == 6592.0

   # assert pl.show_best_video() == "https://youtu.be/cUGyMzWQcGM"