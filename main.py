from vision_language_models.dreamlike import DreamLike
from utils import utils, parsing
from datetime import date, datetime
from apiclient.errors import HttpError
from oauth2client.tools import argparser

mood = "sentimental"
genre = "jazz"
hours = 1

# date for logging
day = date.today().day
current_time = datetime.now().strftime("%H:%M:%S")
date_time = str(day) + '_' + current_time

# for generating responses
model = utils.set_openai()

message_playlist =  utils.construct_message_playlist(hours=hours, mood=mood, genre=genre)
response_playlist = utils.generate_response(model=model, message=message_playlist)

message_image =     utils.construct_message_image(mood=mood, genre=genre)
response_image =    utils.generate_response(model=model, message=message_image)

print("Response of Playlist:\n", response_playlist)
print("Response of Image Prompt:\n", response_image)

# for image generation
model = DreamLike()
model.single_image_generation(response_image, mood=mood, genre=genre, date_time=date_time)

# save playlist respose in to text file
utils.save_playlist_response(response_playlist, mood=mood, genre=genre, date_time=date_time)

# parsing playlist
music_list, len = parsing.parse_playlist(response_playlist)
print(music_list, len)

# youtube api
argparser.add_argument("--q", help="Search term", default="Acid Dreams")
argparser.add_argument("--max-results", help="Max results", default=1)
args = argparser.parse_args()
# print(args)

try:
   search_response = utils.youtube_search(args)
except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))


videos = []
# Add each result to the appropriate list, and then display the lists of
# matching videos, channels, and playlists.
for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["videoId"]))

print(videos)
