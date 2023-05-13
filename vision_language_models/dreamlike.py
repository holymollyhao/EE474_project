from diffusers import StableDiffusionPipeline
import torch
from datetime import date, datetime


class DreamLike:
    def __init__(self, model_id="dreamlike-art/dreamlike-diffusion-1.0", result_path="./image_results"):
        # model setup
        self.model_id = model_id
        self.result_path = result_path

        # pipeline setup
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16)
        self.pipe.to("cuda")

    def single_image_generation(self, prompt, mood, genre):
        day = date.today().day
        current_time = datetime.now().strftime("%H:%M:%S")
        date_time = str(day) + '_' + current_time

        image = self.pipe(prompt).images[0]
        image.save(f"{self.result_path}/mood-{mood}_genre-{genre}_{date_time}_result.jpg")
