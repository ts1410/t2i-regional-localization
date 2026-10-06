import base64
import os
from openai import OpenAI

from backend.providers.base import ImageGenerationProvider


class OpenAIImageProvider(ImageGenerationProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is not configured.")
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str, model: str, parameters: dict = None, reference_image: str = None):
        params = parameters or {}
        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=params.get("size", "1536x1024"),
            quality=params.get("quality", "high"),
        )
        if not getattr(response, "data", None):
            raise RuntimeError("OpenAI returned no image data.")
        image_data = response.data[0].b64_json
        if not image_data:
            raise RuntimeError("OpenAI generated response did not include image bytes.")
        return {
            "provider": "openai",
            "model": model,
            "image_b64": image_data,
            "mime_type": "image/png",
        }
