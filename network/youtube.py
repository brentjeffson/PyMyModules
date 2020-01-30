from bs4 import BeautifulSoup
from apiclient.discovery import build 
import os
import logging
import re
import json
from datetime import datetime
from pprint import pprint

DEVELOPER_KEY = "AIzaSyB1ZqcZ4ULI-XtuF5hKdhX6cLWDy1jdoVE" 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

logging.basicConfig(filename=f'youtube_{datetime.now().strftime("%m-%d-%Y")}.log', level=logging.DEBUG,
    format='[%(levelname)s]:%(asctime)s:%(module)s->def:%(funcName)s->line:%(lineno)d-> %(message)s')

class Item():
    DEFAULT = 'default'
    HIGH = 'high'
    MEDIUM = 'medium'

    def __init__(self, uid, title, thumbnails):
        self._uid = uid
        self._title = title
        self._thumbnails = thumbnails

    @property
    def id(self):
        return self._uid

    @property
    def title(self):
        return self._title

    @property
    def thumbnails(self):
        return self._thumbnails

class Video(Item):
    '''Object Containing Meta For A Youtube Video'''
    BASE_URL = 'https://www.youtube.com/'
    WATCH_API = 'watch'

    def __init__(self, uid, title, thumbnails):
        super().__init__(uid, title, thumbnails)

    def __str__(self):
        return self.url

    @property 
    def url(self):
        return f'{Video.BASE_URL}{Video.WATCH_API}?v={self._uid}'


class Channel(Item):
    '''Object Containing Meta For A Channel'''

    def __init__(self, uid, title, description, thumbnails):
        super().__init__(uid, title, thumbnails)
        self._description = description
        
    def __str__(self):
        return self._title

    @property
    def description(self):
        return self._description


class Playlist(Item):
    '''Object Containing Meta For a Playlist'''

    def __init__(self, uid, title, thumbnails, channel):
        super().__init__(uid, title, thumbnails)
        self._channel = channel

    @property
    def channel(self):
        return self._channel

class Searched():
    VIDEO = 'youtube#video'
    PLAYLIST = 'youtube#playlist'
    CHANNEL = 'youtube#channel'

    def __init__(self, videos=None, playlists=None, channels=None):
        self._videos = videos
        self._playlists = playlists
        self._channels = channels

    def from_response(response):
        items = response.get('items', [])
        
        if len(items) == 0:
            logging.info('No Response: Given Response Does Not Contain Anything')
            return None
        if type(response) != type({}):
            logging.info('Invalid Response Object: Given Response Is Not Of Type `dict`')
            return None

        logging.debug(f'Processing: Initializing. Length of Response -> {len(response)}')
        videos = []
        playlists = []
        channels = []

        logging.debug(f'Processing: Starting.')
        for item in items:
            if item['id']['kind'] == Searched.VIDEO:
                videos.append(Video(
                    item['id']['videoId'],
                    item['snippet']['title'],
                    item['snippet']['thumbnails'],
                ))
            elif item['id']['kind'] == Searched.PLAYLIST:
                playlists.append(Playlist(
                    item['id']['playlistId'],
                    item['snippet']['title'],
                    item['snippet']['thumbnails'],
                    Channel(
                        item['snippet']['channelId'],
                        item['snippet']['channelTitle'],
                        item['snippet']['description'],
                        item['snippet']['thumbnails'],
                    )
                ))
            elif item['id']['kind'] == Searched.CHANNEL:
                channels.append(Channel(
                    item['id']['channelId'],
                    item['snippet']['channelTitle'],
                    item['snippet']['description'],
                    item['snippet']['thumbnails'],
                ))
            else:
                logging.info('Unknown Type: Cannot identify item type.')

        logging.debug(f'Processing: Complete. Videos({len(videos)}) - Playlists({len(playlists)}) - Channels({len(channels)})')
        return Searched(videos, playlists, channels)

    @property
    def videos(self):
        return self._videos

    @property
    def playlists(self):
        return self._playlist

    @property
    def channels(self):
        return self._channels

class Youtube:

    @staticmethod
    def search(session, keyword):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        response = youtube.search().list(
            q=keyword,
            part='id, snippet',
            maxResults = 25
        ).execute()
        pprint(response)
        print(type(response))
        return Searched.from_response(response)

    @staticmethod
    def get_sources(html, parser='html.parser'):
        '''Parses Youtube html to get available video sources
        Args:
            html (str): Youtube html to be parsed
            parser (:obj:`str`, optional): Parser to be used by BeautifulSoup to parse the html. Defaults to `html.parser`

        Returns:
            video_info (list[dict]): List of video sources with meta
        ''' 
        # parses html to a BeautifulSoup object
        soup = BeautifulSoup(html, parser)

        # find script containing video informations
        player_script_tag = soup.select("div#player script:nth-of-type(2)")
        
        # find the sources using regex
        pattern = r'formats\\":(.+)(}]|}]}),\\"(playerAds|dashManifestUrl)'
        searched = re.search(pattern, player_script_tag[0].text)

        # do some cleaning
        src = searched.groups()[0]
        clean_src = src.replace("\\u0026", "&").replace('\\', '')#.replace('[{', '').replace('}}]', '')

        # split cleaned src
        url_info = []
        for index, p in enumerate(re.split("},{", clean_src)):   
            
            # remove excess closing tags
            if index == 0: 
                p = p.replace("[{", "")
            elif index == len(re.split("},{", clean_src))-1:
                p = p.replace("}]}", "")
        
            codecs_value = re.search(r"codecs=\"([\w,\s.\-?_]+)\"", p).groups()[0]
            new_str = re.sub(r'codecs=".+"",', f"codecs={codecs_value}\",", p)
            
            # convert to dictionary, add to list           
            url_info.append(json.loads("{" + new_str + "}"))
        return url_info




