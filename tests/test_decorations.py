import os
import pytest

from PIL import Image

from image import Decoration


class TestDecorations:

    __TEST_ASSETS_FOLDER = 'assets'
    __TEST_PROFILE_IMAGE_NAME = 'test_profile.jpg'

    @classmethod
    def __get_test_image(cls,):
        """ Returns an `Image.Image` instance that will be used for testing. """

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(cur_dir, cls.__TEST_ASSETS_FOLDER)
        image_path = os.path.join(assets_dir, cls.__TEST_PROFILE_IMAGE_NAME)

        return Image.open(image_path)

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

    def test_decoration_assets(self,):
        """ Tests all of the avaliable decorations. """

        decorations = Decoration.avaliable_decorations()
        for decoration in decorations:
            self.__test_decoration(decoration)

    def test_decoratin_generation(self,):
        """ Tries to generate every decoration image that is possible. """

        decorations = Decoration.avaliable_decorations()
        profile = self.__get_test_image()

        for decoration_name in decorations:
            decoration = Decoration(decoration_name)
            assert isinstance(
                decoration.generate_image(profile),
                Image.Image
            ), "Didn't return an image instance."
