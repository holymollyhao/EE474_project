from diffusers import StableDiffusionPipeline
import torch


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
