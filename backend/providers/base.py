from abc import ABC, abstractmethod


class ImageGenerationProvider(ABC):
    @abstractmethod
    def generate(self, prompt, model, parameters=None, reference_image=None):
        raise NotImplementedError
