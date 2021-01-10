import typing
import os

from PIL import Image, ImageDraw


class Decoration:

    DECORATIONS_FOLDER = 'decorations'
    DECORATION_IMAGE_NAME = 'decoration.png'
    DECORATION_MASK_NAME = 'mask.png'

    DEFAULT_DECORATION_NAME = 'default'

    PROFILE_PICTURE_SIZE = (256, 256)  # pixels

    def __init__(self, name: str):

        if name not in self.avaliable_decorations():
            raise ValueError("Not a valid decoration name")

        self.__name = name

    @classmethod
    def avaliable_decorations(cls,) -> typing.Set[str]:
        """ Returns a set of strings. Each string is a valid
        decoration name! """

        return {
            name
            for name in os.listdir(cls.DECORATIONS_FOLDER)
            if os.path.isdir(
                os.path.join(cls.DECORATIONS_FOLDER, name)
            )
        }
