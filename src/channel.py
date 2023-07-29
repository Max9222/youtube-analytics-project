from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import json


load_dotenv()

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)



class Channel:

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализирует
        - id канала
        - название канала
        - описание канала
        - ссылка на канал
        - количество подписчиков
        - количество видео
        - общее количество просмотров
        """
        self.channel_id = channel_id

        channel_id = self.channel_id
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.channel_description = channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/' + channel['items'][0]['snippet']['customUrl']
        self.number_of_subscribers = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.quantity_all_views = channel['items'][0]['statistics']['videoCount']

    def __str__(self):
        """Возвращает название и ссылку на канал по шаблону <название_канала> (<ссылка_на_канал>)"""
        return f'{self.title}({self.url})'

    def __add__(self, other):
        """Сложение количества подписчиков двух каналов."""

        return f'{(int(self.number_of_subscribers) + int(other.number_of_subscribers))}'


    def __sub__(self, other):

        """Разница в количестве подписчиков двух каналов."""
        return f'{(int(self.number_of_subscribers) - int(other.number_of_subscribers))}'


    def __gt__(self, other):

        """Определяет поведение оператора больше, >."""
        return self.number_of_subscribers > other.number_of_subscribers

    def __lt__(self, other):

        """Определяет поведение оператора меньше, <."""
        return self.number_of_subscribers < other.number_of_subscribers

    def __ge__(self, other):

        """Определяет поведение оператора больше или равно, >=."""
        return self.number_of_subscribers >= other.number_of_subscribers


    def __le__(self, other):

        """Определяет поведение оператора меньше или равно, <=."""
        return self.number_of_subscribers <= other.number_of_subscribers

    def __ge__(self, other):

        """Определяет поведение оператора равенства, ==."""
        return self.number_of_subscribers == other.number_of_subscribers

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return print(channel)


    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)


    def to_json(self, filename):
        """ Сохраняет в файл значения атрибутов экземпляра Channel"""
        with open(filename, 'w') as f:
            json.dump(dir(self.get_service()), f, indent=2, ensure_ascii=False)



