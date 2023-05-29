import os

import openai
import os, sys, time, random
import http.client as httplib
import httplib2

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCSUzk-oyjszho49HWVbebIlWV47lS7zZs"
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

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

def generate_youtube_credentials(auth_token):
    from googleapiclient.discovery import build
    from oauth2client import client, GOOGLE_TOKEN_URI
    # Obtain the token using chrome.identity.getAuthToken
    token = auth_token
    # Create credentials from the token
    credentials = client.AccessTokenCredentials(access_token=token, user_agent="pythonclient")
    # credentials.refresh(httplib2.Http())

    # Build the YouTube service with authorized credentials
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube

def youtube_search(youtube, query, max_results):
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type="video",
        regionCode="KR",
        videoCategoryId="10"
    ).execute()

    if (len(search_response.get("items", [])) == 0):
        return 0, 0
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            id = search_result["id"]["videoId"]

    return title, id

class PlayslistVideoGenerator():
    def __init__(self, list_of_urls, cover_imgpath='./image_results/mood-chill vibe_genre-city pop_24_15:52:01_result.jpg', save_path='./music_dir', save_audio_path='./audio_dir'):
        self.list_of_urls = list_of_urls
        self.cover_imgpath = cover_imgpath
        self.save_path = save_path
        self.save_audio_path = save_audio_path
        self.concat_save_path = None

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def download(self):
        import yt_dlp
        SAVE_PATH = self.save_path

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

        for (idx, url) in enumerate(self.list_of_urls):
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

    def create_audio(self):
        from pydub import AudioSegment
        playlist_songs = []
        for audio_file in os.listdir(self.save_path):
            if '.mp3' in audio_file:
                playlist_songs.append(AudioSegment.from_mp3(os.path.join(self.save_path, audio_file)))

        first_song = playlist_songs.pop(0)
        playlist = first_song

        for song in playlist_songs:
            # We don't want an abrupt stop at the end, so let's do a 10 second crossfades
            playlist = playlist.append(song, crossfade=(5 * 1000))
        playlist = playlist.fade_out(30)

        playlist_length = len(playlist) / (1000 * 60)
        output_path_name = "%s_minute_playlist.mp3" % playlist_length
        output_path_name = os.path.join(self.save_audio_path, output_path_name)

        # lets save it!
        with open(output_path_name, 'wb') as out_f:
            playlist.export(out_f, format='mp3')
        self.concat_save_path = output_path_name

    def create_video(self):
        videoname = 'debugvideo'
        audiofpath = self.concat_save_path
        imagefpath = self.cover_imgpath
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
        audio_clip = AudioFileClip(audiofpath)
        image_clip = ImageClip(imagefpath)
        video_clip = image_clip.set_audio(audio_clip)
        video_clip.duration = audio_clip.duration
        video_clip.fps = 60
        video_clip.write_videofile(videoname + '_CLIP.mp4')


# def youtube_build():
#     # CLIENT_SECRETS_FILE = "client_secret_647007276977-akf94ejk5o5u848vll5esuhq3qdrb0bv.apps.googleusercontent.com.json"
#     # MISSING_CLIENT_SECRETS_MESSAGE = """
#     # WARNING: Please configure OAuth 2.0
#     #
#     # To make this sample run you will need to populate the client_secrets.json file
#     # found at:
#     #
#     # %s
#     #
#     # with information from the API Console
#     # https://console.cloud.google.com/
#     #
#     # For more information about the client_secrets.json file format, please visit:
#     # https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
#     # """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
#     #                                 CLIENT_SECRETS_FILE))
#     #
#     # flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
#     #   message=MISSING_CLIENT_SECRETS_MESSAGE,
#     #     scope=YOUTUBE_READ_WRITE_SCOPE)
#     #
#     # storage = Storage("%s-oauth2.json" % sys.argv[0])
#     # credentials = storage.get()
#     #
#     # if credentials is None or credentials.invalid:
#     #     flags = argparser.parse_args()
#     #     credentials = run_flow(flow, storage, flags)
#     #
#     # youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
#     #     http=credentials.authorize(httplib2.Http()))\
#     from googleapiclient.discovery import build
#     from oauth2client import client, GOOGLE_TOKEN_URI
#     # Obtain the token using chrome.identity.getAuthToken
#     token = "ya29.a0AWY7CknUMyKUr5ZvIw6zLt6AHHmjafCAV6hXNgNrnqi4npDjVtDgP8MrCr-BikTXKZNkMk5PUW7RS_VfpPjCuxFSJv1WWXB0zC0KIBmVOrO2PQxHBe9h3Cnpxkjj4SOIyqAXsiepT3TdJ-wyWW9-CqP9WEoUaCgYKAe0SARMSFQG1tDrpRxHeIgh4t9Aq2QTOLCtjUg0163"
#
#     # Create credentials from the token
#     credentials = client.AccessTokenCredentials(token, "MY_USER_AGENT")
#
#     # Build the YouTube service with authorized credentials
#     youtube = build("youtube", "v3", credentials=credentials)
#     print("youtube build complete!")
#     return youtube

def youtube_create_playlist(youtube, title, privacyStatus="public"):
    # This code creates a new, private playlist in the authorized user's channel.
    playlists_insert_response = youtube.playlists().insert(
        part="snippet,status",
        body=dict(
            snippet=dict(
                title=title,
                description="generated by Feel Like",
            ),
            status=dict(
                privacyStatus=privacyStatus
            )
        )
    ).execute()

    return playlists_insert_response["id"]

def youtube_insert_music(youtube, playlist_id, id_list):
    for videoId in id_list:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": videoId
                    }
                }
            }
        ).execute()

    return

def youtube_video_upload(youtube, title, file, privacyStatus="public"):
    tags = None

    body=dict(
        snippet=dict(
            title=title,
            description="generated by Feel Like",
            tags=tags,
            categoryId="10" # Music
            ),
            status=dict(
                privacyStatus=privacyStatus
            )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print ("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print ("Video id '%s' was successfully uploaded." % response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if (e.resp.status in RETRIABLE_STATUS_CODES):
                error = ("A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                    e.content))
            else:
                raise
        except RETRIABLE_EXCEPTIONS as  e:
            error = ("A retriable error occurred: %s" % e)

        if error is not None:
            print (error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)
