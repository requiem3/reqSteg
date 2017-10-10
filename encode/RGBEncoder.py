from BitVector import BitVector
from PIL import Image
from encode.Encoder import Encoder


class RGBEncoder(Encoder):

    def __init__(self):
        self.key = "PLACEHOLDER"

    def encode(self, image_path, message):
        image = Image.open(image_path)
        image_rgb = image.convert("RGB")

        if self.__can_fit__(image, message):
            # TODO: Not finished yet, gotta encode message into least significant 2 bits of each color
            message_bits = BitVector(textstring=message)
            message_bits.pad_from_right(16)  # Add 0x0000 as padding to represent NULL
        else:
            raise EncodingError("The image not big enough for message")

    def decode(self, image_path):
        # TODO
        return None

    @staticmethod
    def __can_fit__(image, message):
        """
        Checks if size of image is sufficient to encode message
        :param image: Image instance
        :param message: Target message
        :return: Boolean T/F
        """
        if message.length <= ((image.size / 3) - 1):  # 3 pixels per character and NULL to indicate end of message
            return True
        else:
            return False

    @staticmethod
    def __chunk_list__(target_list, n):
        """
        Creates a iterable that yields chunks of target_list of size n
        :param target_list: List to be made an iterable
        :param n: Sublist size
        :return: Iterable list
        """
        for element in range(0, len(target_list), n):
            yield target_list[element:element + n]


class EncodingError(ValueError):
    pass
