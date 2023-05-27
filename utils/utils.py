import os

import openai
from apiclient.discovery import build

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCSUzk-oyjszho49HWVbebIlWV47lS7zZs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def set_openai():
    OPENAI_API_KEY = "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"
    openai.api_key = OPENAI_API_KEY
    model = "gpt-3.5-turbo"
    return model

def construct_message_playlist(hours:int, mood:str, genre:str):
    query = f"give me a {hours}-h {mood} playlist of {genre}"
    prompt_for_parsing = ", without additional responses attached on the front and back, just give me a list with numbering starting from 1"
    prompt_for_parsing2 = ", in the following format: [number]. [song name] - [artist name]. for example, 1. dynamite - BTS"

    role = f"You are a music curator, who recommends music lists with consistent mood and genere"

    query += prompt_for_parsing 
    query += prompt_for_parsing2
    messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": query}
    ]
    return messages

def construct_message_image(mood:str, genre:str):
    query = f"Describe a scene where you might listen to a {mood} playlist of {genre}"
    prompt_for_parsing = ", without additional responses attached on the front and back, just give me a description of the surroundings, as descriptive as you can, but constrain your output to a maximum of 77 tokens"

    role = f"You are a assistant who generates prompts for image generation, who describes a likely scene based on the mood and genere of a music playlist"

    query += prompt_for_parsing
    messages = [
        {"role": "system", "content": role},
        {"role": "user", "content": query}
    ]
    return messages

def generate_response(model, message):
    response = openai.ChatCompletion.create(
        model=model,
        messages=message
    )
    return response['choices'][0]['message']['content']

def save_playlist_response(response_playlist, mood, genre, date_time):
    result_path = "./playlist_results"
    text_file = open(f"{result_path}/mood-{mood}_genre-{genre}_{date_time}_result.txt", "w")
    text_file.write(response_playlist)
    text_file.close

def youtube_search(query, max_results):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type="video"
    ).execute()

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            id = search_result["id"]["videoId"]

    return title, id 

def download_youtube(list_of_urls = ['https://www.youtube.com/watch?v=NaFd8ucHLuo', 'https://www.youtube.com/watch?v=WMweEpGlu_U', 'https://www.youtube.com/watch?v=4TWR90KJl84']):
    # from __future__ import unicode_literals
    import yt_dlp
    SAVE_PATH='music_dir'
    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)

    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    for (idx, url) in enumerate(list_of_urls):
        yt_dlp_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'outtmpl': SAVE_PATH + f'/track_{idx}.%(ext)s',
        }
        with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
            ydl.download([url])

    output_path_name = generate_concat_music(audio_fpath='./music_dir/')
    generate_video(audiofpath=output_path_name)


def generate_concat_music(audio_fpath=None):
    from pydub import AudioSegment
    playlist_songs = []
    for audio_file in os.listdir(audio_fpath):
        if '.mp3' in audio_file:
            playlist_songs.append(AudioSegment.from_mp3(os.path.join(audio_fpath, audio_file)))

    first_song = playlist_songs.pop(0)
    playlist = first_song

    for song in playlist_songs:
        # We don't want an abrupt stop at the end, so let's do a 10 second crossfades
        playlist = playlist.append(song, crossfade=(5 * 1000))
    playlist = playlist.fade_out(30)

    playlist_length = len(playlist) / (1000 * 60)
    output_path_name = "%s_minute_playlist.mp3" % playlist_length
    # lets save it!
    with open(output_path_name, 'wb') as out_f:
        playlist.export(out_f, format='mp3')
    return output_path_name




def generate_video(fileSaveName='debug_playlist', audiofpath='./9.7685_minute_playlist.mp3', imagefpath='./image_results/mood-chill vibe_genre-city pop_24_15:52:01_result.jpg'):
    from moviepy.editor import AudioFileClip, ImageClip
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(imagefpath)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(r'./fonts/Open_Sans/opensans_bold_italic.ttf', 350)
    msg = 'feel_like'
    _, _, w, h = draw.textbbox((0, 0), msg, font=font)
    draw.text(((im.width - w) / 2, (im.height - h) / 2), msg, font=font, fill="white")

    im.save(imagefpath)
    #
    # audio_clip = AudioFileClip(audiofpath)
    # image_clip = ImageClip(imagefpath)
    # video_clip = image_clip.set_audio(audio_clip)
    # video_clip.duration = audio_clip.duration
    # video_clip.fps = 60
    # video_clip.write_videofile(fileSaveName + '_CLIP.mp4')

