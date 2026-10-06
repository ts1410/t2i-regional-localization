from abc import ABC, abstractmethod


class ImageGenerationProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, model: str, parameters: dict = None, reference_image: str = None):
        raise NotImplementedError
