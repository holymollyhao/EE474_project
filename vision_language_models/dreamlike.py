from diffusers import StableDiffusionPipeline
import torch
<<<<<<< HEAD
import os
from datetime import datetime


class DreamLike:
    def __init__(self, log_datetime, model_id="dreamlike-art/dreamlike-photoreal-2.0", result_path="./image_results"):
        # model setup
        self.model_id = model_id
        self.result_path = result_path
        self.date_time = log_datetime

        # pipeline setup
        # commandline_args = os.environ.get('COMMANDLINE_ARGS', "--skip-torch-cuda-test --no-half")
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16)
        self.pipe.to("cuda")

    def single_image_generation(self, prompt, mood, genre):
        # if already exists path, then simply return
        if os.path.exists(self.generate_savepath(mood,genre)) == True:
            return

        image = self.pipe(prompt, height=1080, width=1920).images[0]
        image.save(self.generate_savepath(mood, genre))

    def generate_savepath(self, mood, genre):
        mood = mood.replace(" ", "-")
        genre = genre.replace(" ", "-")
        return f"{self.result_path}/mood-{mood}_genre-{genre}_{self.date_time}_result.jpg"
=======


class DreamLike:
    def __init__(self, model_id="dreamlike-art/dreamlike-photoreal-2.0", result_path="./image_results"):
        # model setup
        self.model_id = model_id
        self.result_path = result_path

        # pipeline setup
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16)
        self.pipe.to("cuda")

    def single_image_generation(self, prompt, mood, genre, date_time):
        image = self.pipe(prompt, height=1080, width=1920).images[0]
        image.save(f"{self.result_path}/mood-{mood}_genre-{genre}_{date_time}_result.jpg")
>>>>>>> 93ea155d85618d739d6c7b252b4776a68117e5fc
