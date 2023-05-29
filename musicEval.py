import pandas as pd
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from utils import utils

client_credentials_manager = SpotifyClientCredentials(client_id='b6ee2c7f358c445fa81080ff478f81a4', client_secret='9651cde328304d648b76b980d961e36e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def eval(title):

    song_list = utils.read_playlist(mood, genre, date_time)

    for song in song_list:
        results = sp.search(q=song, limit=1) 
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            features = sp.audio_features(track['id'])[0]  

            audio_features_list.append(features)  

    utils.save_audio_features(audio_features_list, mood, genre, date_time)