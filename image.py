import typing
import os
import random
import json

import requests
import click
from PIL import Image, ImageDraw

import decoration_types


class Decoration:

    DECORATIONS_FOLDER = 'decorations'
    DECORATION_IMAGE_NAME = 'decoration.png'
    DECORATION_MASK_NAME = 'mask.png'
    DECORATION_CONFIG_FILENAME = 'config.json'

    DEFAULT_DECORATION_NAME = 'default'
    DEFAULT_DECORATION_TYPE = 'default'

    PROFILE_PICTURE_SIZE = (256, 256)  # pixels

    def __init__(self, name: str = None):

        if name is None:
            name = self.DEFAULT_DECORATION_NAME

        if name not in self.avaliable_decorations():
            raise ValueError("Invalid decoration name")

        self.__name = name
        self._config = self.__load_config_data()

        # try running -> should raise an error if somethings wrong
        self.type_cls  # pylint: disable=pointless-statement

    def __load_config_data(self,) -> dict:
        """ Loads the decoration configuration file, and saves the data in
        memory. """

        # Load the decoraion type
        config_path = os.path.join(
            self._this_folder(), self.DECORATION_CONFIG_FILENAME)

        with open(config_path, 'r') as file:
            return json.load(file)

    def _this_folder(self,):
        """ Returns the path to the current decoration folder. """
        return os.path.join(self.DECORATIONS_FOLDER, self.name)

    @property
    def name(self) -> str:
        """ The name of the decoration. """
        return self.__name

    @property
    def type(self,) -> str:
        """ The type of the decoration, as a string. """
        return self._config['type']

    @property
    def type_cls(self,) -> decoration_types.DecorationType:
        """ Returns a pointer to an object (class, not instance of class)
        that represents the type of the current decoration. """

        if self.type not in decoration_types.TYPES_TABLE:
            raise ValueError(
                f"Decoration type '{self.type}' is not currect. Double check the config file!"
            )

        return decoration_types.TYPES_TABLE[self.type]

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

    def __github_profile(self, username: str) -> Image.Image:
        """ Recives the GitHub username, and returns the profile picture of
        the user, as a pillow `Image.Image` instance. """

        url = f'https://github.com/{username}.png'

        response = requests.get(url, stream=True)
        if response.status_code != 200:
            raise ValueError("Invalid GitHub username")

        click.echo(f'Downloaded image of user {username} from GitHub')

        return Image.open(response.raw)

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

    def generate_image(self, profile: Image.Image) -> Image.Image:
        """ Recives a profile picture, and pastes the current decoration
        on top of it. Returns the new decorated image. """

        # Resized the profile picture
        profile = profile.resize(self.PROFILE_PICTURE_SIZE)

        image = self.__cut_mask(profile)
        decoration = self.__paste_decoration(image)

        click.echo('Generated decoration image')

        return decoration

    def generate_github_image(self, username: str) -> Image.Image:
        """ Recives a GitHub username, and pasted the current decoration
        on top of hist profile picture. Returns the decorated image. """

        profile = self.__github_profile(username)
        return self.generate_image(profile)


class Canvas:

    SIZE = (1920, 1440)  # 4:3 ratio
    CANVAS_PATH = 'canvas.png'

    def __init__(self):

        if os.path.isfile(self.CANVAS_PATH):
            canvas = Image.open(self.CANVAS_PATH,)
            self.SIZE = canvas.size

        else:
            canvas = self.__generate_default_canvas()

        self.__canvas = canvas

    def __generate_default_canvas(self,):
        """ Generates and returns the default empty canvas. """

        img = Image.new(
            'RGBA',
            size=self.SIZE,
            color=(0, 0, 0, 0),
        )

        click.echo('Generated new canvas')

        return img

    def clear(self,):
        """ Resets the canvas and deletes the already generated footprints. """
        self.__canvas = self.__generate_default_canvas()

    def add_image(self, img: Image.Image):
        """ Pastes the given image onto the canvas (without resizing). """

        # Generating the pasting location
        max_x = self.SIZE[0] - img.width
        max_y = self.SIZE[1] - img.height
        pasting = random.randint(0, max_x), random.randint(0, max_y)

        self.__canvas.paste(
            img.convert('RGB'),
            box=pasting,
            mask=img.getchannel('A'),
        )

        click.echo(f'Added image to canvas at position {pasting}')

    def save(self,):
        """ Saves the new generated canvas. """

        self.__canvas.save(self.CANVAS_PATH)
        click.echo(f'Saved {self.CANVAS_PATH}')


@click.command()
@click.argument('gh-username')
@click.option('-d', '--decoration')
@click.option('-c', '--clear', is_flag=True)
def main(gh_username: str, clear: bool, decoration: str = None,):

    canvas = Canvas()

    if clear:
        # Reset canvas if requested
        canvas.clear()

    try:
        decoration = Decoration(decoration)

    except ValueError as e:
        # If invalid decoration
        click.echo(e)
        exit(10)

    try:
        img = decoration.generate_github_image(gh_username)

    except ValueError as e:
        # If invalid GitHub username (picture not found)
        click.echo(e)
        exit(20)

    canvas.add_image(img)
    canvas.save()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
