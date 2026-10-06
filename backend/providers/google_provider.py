import os

try:
    import google.generativeai as genai
except Exception:
    genai = None

from backend.providers.base import ImageGenerationProvider


class GoogleImageProvider(ImageGenerationProvider):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is not configured.")
        if genai is None:
            raise RuntimeError("Google dependency is not available.")
        genai.configure(api_key=self.api_key)

    def generate(self, prompt, model, parameters=None, reference_image=None):
        params = parameters or {}
        model_name = model
        generation_config = {"temperature": params.get("temperature", 0.7)}
        model_client = genai.GenerativeModel(model_name, generation_config=generation_config)
        response = model_client.generate_content(prompt)

        image_bytes = None
        if hasattr(response, "parts"):
            for part in response.parts:
                if hasattr(part, "inline_data") and getattr(part.inline_data, "data", None):
                    image_bytes = part.inline_data.data
                    break
        if image_bytes is None:
            raise RuntimeError("Google returned no image data.")

        return {
            "provider": "google",
            "model": model,
            "image_b64": image_bytes,
            "mime_type": "image/png",
        }
