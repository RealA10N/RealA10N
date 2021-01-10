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

    def _this_folder(self,):
        """ Returns the path to the current decoration folder. """
        return os.path.join(self.DECORATIONS_FOLDER, self.__name)

    @classmethod
    def _default_folder(cls,):
        """ Returns the path to the default decoration folder. """
        return os.path.join(cls.DECORATIONS_FOLDER, cls.DEFAULT_DECORATION_NAME)

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

    def __cut_mask(self, img: Image.Image):
        """ Recives a profile image. Loads the decoration mask (the default
        mask if decoration mask is not provided), and returns the profile
        picture with the mask appended. """

        mask_path = os.path.join(
            self._this_folder(), self.DECORATION_MASK_NAME,)

        if not os.path.isfile(mask_path):
            # If current decoration doesn't contain its own mask,
            # loads the default mask (:
            mask_path = os.path.join(
                self._default_folder(), self.DECORATION_MASK_NAME)

        mask = Image.open(mask_path).convert('L')
        bg = img.copy()
        bg.putalpha(0)

        return Image.composite(img, bg, mask)

    def __paste_decoration(self, img: Image.Image):
        """ Recives a profile picture. Loads the current decoration (if exists)
        and returns the profile picture with the decoration appended. """

        decoration_path = os.path.join(
            self._this_folder(), self.DECORATION_IMAGE_NAME,)

        if not os.path.isfile(decoration_path):
            # If there is no decoration, returns the given image
            return img

        decoration = Image.open(decoration_path)

        # Decoration image is always BIGGER then the profile image.

        bg = Image.new('RGBA', size=decoration.size, color=(255, 255, 255, 0))

        pasting_x = (decoration.width - img.width) / 2
        pasting_y = (decoration.height - img.height) / 2
        pasting_box = int(pasting_x), int(pasting_y)

        bg.paste(
            img.convert('RGB'),
            box=pasting_box,
            mask=img.getchannel('A'),
        )

        bg.alpha_composite(decoration)
        return bg

    def generate_image(self, profile: Image.Image):
        """ Recives a profile picture, and pastes the current decoration
        on top of it. Returns the new decorated image. """

        # Resized the profile picture
        profile = profile.resize(self.PROFILE_PICTURE_SIZE)

        image = self.__cut_mask(profile)
        return self.__paste_decoration(image)
