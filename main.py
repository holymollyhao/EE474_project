from vision_language_models.dreamlike import DreamLike
from utils import utils

mood = "sentimental"
genre = "jazz"

# for generating responses
model = utils.set_openai()
message = utils.construct_message_image(mood=mood, genre=genre)
response = utils.generate_response(model=model, message=message)
print(response)

# for image generation
model = DreamLike()
model.single_image_generation(response, mood=mood, genre=genre)
