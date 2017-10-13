from BitVector import BitVector
from PIL import Image
from encode.Encoder import Encoder
import os


class RGBEncoder(Encoder):

    def __init__(self):
        self.key = "PLACEHOLDER"

    def encode(self, image_path, message):
        """
        Encode message into image, save it to same directory, and return modified image
        :param image_path: Path to target image
        :param message: Message to encode
        :return: Modified image converted to RGB values
        """
        if image_path.strip()[-1] is '\\' or image_path.strip()[-1] is '/':
            image_path = image_path[:-1]

        head, tail = os.path.split(image_path)
        image_name, file_type = tail.split(".")
        image = Image.open(image_path)

        if self.__can_fit__(image, message):
            image_rgb = image.convert("RGB")
            message_bits = BitVector(textstring=message)
            message_bits.pad_from_right(16)  # Add 0x0000 as padding to represent NULL
            self.__swap_bits__(image_rgb, message_bits)
            image_rgb.save(head + image_name + "encoded." + file_type)
            return image_rgb
        else:
            raise EncodingError("The image not big enough for message")

    def decode(self, image_path):
        """
        Attempts to decode message hidden in the image at given path
        :param image_path: Path to image
        :return: Hidden message string
        """
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
        Creates a finite generator that yields chunks of target_list of size n
        :param target_list: List to be made an finite generator
        :param n: Sublist size
        :return: Generator of the target list
        """
        for element in range(0, len(target_list), n):
            yield target_list[element:element + n]

    def __swap_bits__(self, rgb_image, message_bits):
        """
        Changes the last 2 bits of the Red Green and Blue color values to be
        :param rgb_image: Image converted to RGB
        :param message_bits: Message converted to list of bits
        :return: Modified new image
        """
        width, height = rgb_image.size
        pixels = rgb_image.load()
        i = j = 0

        split_bit_list = self.__chunk_list__(message_bits, 6)
        for bits in split_bit_list:
            (red, green, blue) = pixels[i, j]
            encode_red, encode_green, encode_blue = bin(red), bin(green), bin(blue)
            encode_red[-2:] = bits[:2]

            if bits[2:4]:
                encode_green[-2:] = bits[2:4]

            if bits[4:6]:
                encode_blue[-2:] = bits[4:6]

            pixels[i, j] = (encode_red, encode_green, encode_blue)

            i += 1
            if i >= width:
                i = 0
                j += 1

            if j >= height:
                raise EncodingError("Exceeded the maximum height of the image!")


class EncodingError(ValueError):
    pass


if __name__ == "__main__":
    test = [1, 2, 3, 4, 5, 6]
    test[-2:] = [9, 10]
    print(test)
    print(test[0])
    print(test[6:8])
