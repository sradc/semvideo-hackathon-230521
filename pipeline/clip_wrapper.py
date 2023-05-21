from typing import List

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

MODEL_DIM = 512


class ClipWrapper:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def images2vec(self, images: List[Image.Image]) -> torch.Tensor:
        inputs = self.processor(images=images, return_tensors="pt")
        with torch.no_grad():
            model_inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            image_embeds = self.model.vision_model(**model_inputs)
            clip_vectors = self.model.visual_projection(image_embeds[1])
        return clip_vectors / clip_vectors.norm(dim=-1, keepdim=True)

    def texts2vec(self, texts: List[str]) -> torch.Tensor:
        inputs = self.processor(text=texts, return_tensors="pt", padding=True)
        with torch.no_grad():
            model_inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            text_embeds = self.model.text_model(**model_inputs)
            text_vectors = self.model.text_projection(text_embeds[1])
        return text_vectors / text_vectors.norm(dim=-1, keepdim=True)
