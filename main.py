from vision_language_models.dreamlike import DreamLike
from utils import utils, parsing
from datetime import date, datetime
from apiclient.errors import HttpError

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
music_list = parsing.parse_playlist(response_playlist)
# print(music_list)

# youtube api
title_list = []
id_list = []
for music in music_list:
    try:
        title, id = utils.youtube_search(music, 1)
        title_list.append(title)
        id_list.append(id)
    except HttpError as e:
        print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

for i in range(len(title_list)):
    print(f"title: {title_list[i]}, url: www.youtube.com/watch?v={id_list[i]}")