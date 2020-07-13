from urllib.request import urlopen
from requests import Session
from bs4 import BeautifulSoup
import time


class SONG:
    def __init__(self):
        self.title = ''
        self.photo = ''


def song_data(url, url_photo, default_photo):
    song = SONG()
    song.title = song_title(url)

    song.photo = song_photo(url_photo, default_photo)

    return song


def song_title(url):
    radio_session = Session()
    radio = radio_session.get(url, headers={'Icy-MetaData': '1'}, stream=True)
    metaint = int(radio.headers['Icy-metaint'])
    stream = radio.raw
    stream.read(metaint)
    meta_byte = stream.read(1)
    meta_length = ord(meta_byte) * 16

    meta_data = stream.read(meta_length).rstrip(b'\0').decode("utf-8")

    stream_title = str(meta_data).split("='")[1].split("';")[0]

    return stream_title


def song_photo(url_photo, default_photo):  # ISKANJE SLIKE ##########
    track_cover = ''
    html = urlopen(url_photo)
    bs = BeautifulSoup(html, 'html.parser')
    track_cover = bs.find('img', class_="music-track-cover")['src']

    if track_cover == '':  # Če ne najde URL-ja slike,  navadno med menjavo pesmi postavi default
        track_cover = default_photo

    return track_cover
