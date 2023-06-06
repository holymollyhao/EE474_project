import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from utils import utils
import argparse
from utils import utils, parsing
import sys


client_credentials_manager = SpotifyClientCredentials(client_id='b6ee2c7f358c445fa81080ff478f81a4', client_secret='9651cde328304d648b76b980d961e36e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def main(m,g,h):
    mood = m # "sentimental", "trendy", "chill"
    genre = g # "jazz", "KPOP", "city pop"
    hours = h

    # for generating responses
    model = utils.set_openai()

    message_playlist =  utils.construct_message_playlist(hours=hours, mood=mood, genre=genre)
    response_playlist = utils.generate_response(model=model, message=message_playlist)

    result_path = "./playlist_results"
    filename = f"{result_path}/playlist-{mood}_genre-{genre}.txt"

    with open(filename, "w") as file:
        file.write(response_playlist)

    return filename

def audiofeature(filename):
    with open(filename, "r") as file:
        song_list = [line.strip() for line in file]

    audio_features_list = []
    for song in song_list:
        results = sp.search(q=song, limit=1) 
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            features = sp.audio_features(track['id'])[0]  

            audio_features_list.append(features)  

    return audio_features_list


def save_audio_features(audio_features_list, mood, genre):
    result_path = "./music_features_result"
    filename = f"{result_path}/audio_features_mood-{mood}_genre-{genre}.txt"

    num_songs = len(audio_features_list)

    with open(filename, 'w') as file:
        
        file.write("\nSong-wise Audio Features:\n")
        for features in audio_features_list:
            file.write(str(features) + '\n')

    return filename

# Change this part to make example evaluation result
playlist1 = main("soft and calm", "Lullaby", 1)
playlist2 = "lullaby.txt"

pl1 = audiofeature(playlist1)
pl2 = audiofeature(playlist2)

file1 = save_audio_features(pl1, "soft", "Lullaby")
file2 = save_audio_features(pl2, "humanmade_soft", "Lullaby")