from BitVector import BitVector
from PIL import Image
from encode.Encoder import Encoder
import os


class RGBEncoder(Encoder):

    def __init__(self):
        self.key = "PLACEHOLDER"  # Here until I figure out how encryption could be implemented with class

    def encode(self, image_path, message):
        """
        Encode message into image, save it to same directory, and return modified image
        :param image_path: Path to target image
        :param message: Message to encode
        :return: Modified image converted to RGB values
        """
        if image_path.strip()[-1] is '\\' or image_path.strip()[-1] is '/':  # Strip trailing slashes ( \ or / )
            image_path = image_path[:-1]

        head, tail = os.path.split(image_path)
        image_name, file_type = tail.split(".")
        image = Image.open(image_path)

        if self.__can_fit__(image, message):
            image_rgb = image.convert("RGB")
            message_bits = BitVector(textstring=message)
            message_bits.pad_from_right(16)  # Add 0x0000 as padding to represent NULL

            self.__swap_bits__(image_rgb, message_bits)
            image_rgb.save(head + "/" + image_name + "encoded." + file_type)  # Save new image to original directory
            return image_rgb
        else:
            raise EncodingError("The image not big enough for message")

    def decode(self, image_path):
        """
        Attempts to decode message hidden in the image at given path
        :param image_path: Path to image
        :return: Hidden message string
        """
        image = Image.open(image_path)
        image_rgb = image.convert("RGB")
        bit_string = ""

        width, height = image.size
        for j in range(height):
            for i in range(width):  # Collect message bits until NULL terminator is reached
                (red, green, blue) = image_rgb.getpixel((i, j))
                if len(bit_string) >= 16 and bit_string[-16:] == "0000000000000000":
                    break
                else:
                    bit_string += bin(red)[-2:]

                if len(bit_string) >= 16 and bit_string[-16:] == "0000000000000000":
                    break
                else:
                    bit_string += bin(green)[-2:]

                if len(bit_string) >= 16 and bit_string[-16:] == "0000000000000000":
                    break
                else:
                    bit_string += bin(blue)[-2:]

            else:  # If inner loop breaks, break out of outer loop
                continue
            break

        message_bit_vector = BitVector(bitstring=bit_string)
        return message_bit_vector.get_bitvector_in_ascii()

    @staticmethod
    def __can_fit__(image, message):
        """
        Checks if size of image is sufficient to encode message
        :param image: Image instance
        :param message: Target message
        :return: Boolean T/F
        """
        width, height = image.size
        if len(message) <= int(((width * height) / 3) - 1):  # 3 pixels per char and NULL to indicate end of message
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
        i = j = 0

        split_bit_list = self.__chunk_list__(str(message_bits), 6)
        for bits in split_bit_list:
            (red, green, blue) = rgb_image.getpixel((i, j))
            encode_red, encode_green, encode_blue = bin(red), bin(green), bin(blue)
            encode_red = encode_red[:-2] + str(bits[:2])  # Swap last 2 bits of color with 2 message bits

            if len(bits) >= 4:
                encode_green = encode_green[:-2] + str(bits[2:4])

            if len(bits) == 6:
                encode_blue = encode_blue[:-2] + str(bits[4:6])

            rgb_image.putpixel((i, j), (int(encode_red, 2), int(encode_green, 2), int(encode_blue, 2)))

            i += 1
            if i >= width:
                i = 0
                j += 1

            if j >= height:
                raise EncodingError("Exceeded the maximum height of the image!")


class EncodingError(ValueError):
    pass


if __name__ == "__main__":
    test = RGBEncoder()
    test.encode("D:/Coding Work/Public - For Github/reqSteg/images/stego.png", "Hello World!!")
    t_string = test.decode("D:/Coding Work/Public - For Github/reqSteg/images/stegoencoded.png")
    print(t_string)
