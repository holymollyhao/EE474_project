from vision_language_models.dreamlike import DreamLike
from utils import utils
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

mood = "sentimental"
genre = "jazz"
hours = 1

# for generating responses
model = utils.set_openai()

message_playlist =  utils.construct_message_playlist(hours=hours, mood=mood, genre=genre)
response_playlist = utils.generate_response(model=model, message=message_playlist)

message_image =     utils.construct_message_image(mood=mood, genre=genre)
response_image =    utils.generate_response(model=model, message=message_image)

print("Response of Playlist: \n", response_playlist)
print("Response of Image Prompt: ", response_image)

# for image generation
model = DreamLike()
model.single_image_generation(response_image, mood=mood, genre=genre)

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
