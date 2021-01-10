import os
import pytest

from PIL import Image

from image import Decoration


class TestDecorations:

    def __test_decoration(self, name: str):
        """ Recives a decoration name, and test that it exists and that
        everything is fine! """

        folder = os.path.join(Decoration.DECORATIONS_FOLDER, name)
        decoration = os.path.join(folder, Decoration.DECORATION_IMAGE_NAME)
        mask = os.path.join(folder, Decoration.DECORATION_MASK_NAME)

        is_decoration, is_mask = False, False

        if os.path.isfile(decoration):
            is_decoration = True
            decoration_img = Image.open(decoration)
            self.__test_decoration_img(decoration_img)

        if os.path.isfile(mask):
            is_mask = True
            mask_img = Image.open(mask)
            self.__test_mask_img(mask_img)

        return is_decoration, is_mask

    def __test_decoration_img(self, img: Image.Image):
        """ Actually tests the given decoration image using the PIL library. """

        for decoration_size, profile_size in zip(img.size, Decoration.PROFILE_PICTURE_SIZE):
            assert decoration_size >= profile_size, f"Decoration size must be at least {profile_size}"

    def __test_mask_img(self, img: Image.Image):
        """ Actually tests the given mask image using the PIL library. """

        for mask_size, profile_size in zip(img.size, Decoration.PROFILE_PICTURE_SIZE):
            assert mask_size == profile_size, "Mask size must match profile picture size."

    def test_default_decoration(self,):
        """ Asserts that the default decoration exists. """

        name = Decoration.DEFAULT_DECORATION_NAME
        _, is_mask = self.__test_decoration(name)

        assert is_mask, "Default decoration must contain a default mask"

    def test_decorations(self,):
        """ Tests all of the avaliable decorations. """

        decorations = Decoration.avaliable_decorations()
        for decoration in decorations:
            self.__test_decoration(decoration)
