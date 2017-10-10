from abc import ABC, abstractmethod


class Encoder(ABC):

    @abstractmethod
    def encode(self, image_path, message):
        pass

    @abstractmethod
    def decode(self, image_path):
        pass
