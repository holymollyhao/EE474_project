from vision_language_models.dreamlike import DreamLike
from utils import utils

mood = "sentimental"
genre = "jazz"
hours = 1

# for generating responses
model = utils.set_openai()

message_playlist =  utils.construct_message_playlist(hours=hours, mood=mood, genre=genre)
response_playlist = utils.generate_response(model=model, message=message_playlist)

message_image =     utils.construct_message_image(mood=mood, genre=genre)
response_image =    utils.generate_response(model=model, message=message_image)


print("Response of Playlist: ", response_playlist)
print("Response of Image Prompt: ", response_image)

# for image generation
model = DreamLike()
model.single_image_generation(response_image, mood=mood, genre=genre)
