from diffusers import StableDiffusionPipeline
import torch
import os
from datetime import datetime


class DreamLike:
    def __init__(self, model_id="dreamlike-art/dreamlike-photoreal-2.0", result_path="./image_results"):
        # model setup
        self.model_id = model_id
        self.result_path = result_path
        self.date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # pipeline setup
        # commandline_args = os.environ.get('COMMANDLINE_ARGS', "--skip-torch-cuda-test --no-half")
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16)
        self.pipe.to("cuda")

    def single_image_generation(self, prompt, mood, genre):
        image = self.pipe(prompt, height=1080, width=1920).images[0]
        image.save(f"{self.result_path}/mood-{mood}_genre-{genre}_{self.date_time}_result.jpg")

    def generate_savepath(self, mood, genre):
        return f"{self.result_path}/mood-{mood}_genre-{genre}_{self.date_time}_result.jpg"
