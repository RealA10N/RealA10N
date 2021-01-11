import os
import json
import typing


class DecorationType:

    GENERAL_CONFIG_FOLDER = 'decorations'
    GENERAL_CONFIG_FILENAME = 'types.json'

    _data = None

    def __init__(self, name: str):

        if name not in self.avaliable_types():
            raise ValueError("Invalid decoration type")

        if self._data is None:
            self._data = self.__load_data()

        self.__name = name
        self.__cur_data = next(
            cur_data
            for cur_data in self._data
            if cur_data['type'] == name
        )

    @classmethod
    def __load_data(cls,):
        """ Loads the decoration general configuration file, and returns
        the raw data. """

        path = os.path.join(
            cls.GENERAL_CONFIG_FOLDER,
            cls.GENERAL_CONFIG_FILENAME,
        )

        with open(path, 'r') as file:
            return json.load(file)

    @classmethod
    def avaliable_types(cls,) -> typing.Set[str]:
        """ Returns a set of strings. Each string is a valid decoration
        type. """

        if cls._data is None:
            cls._data = cls.__load_data()

        return {
            type_data['type']
            for type_data in cls._data
        }

    def is_label(self,) -> bool:
        """ Returns `True` if the current decoration type has a special label.
        For example, the 'following' decoration type has a special label,
        that is displayed in the README.md file (: """

        return 'label' in self.__cur_data

    def label_url(self,) -> typing.Optional[str]:
        """ Returns the url that contains the label image. `None` if there
        is no label to the current decoration type. """

        if not self.is_label():
            return None

        text = self.__cur_data['label']['text']
        color = self.__cur_data['label']['color']
        return f'https://img.shields.io/badge/-{text}-{color}'

    def label_html(self,) -> typing.Optional[str]:
        """ Returns a string that represents an html `image` tag. This
        tag, when placed in an html or markdown file, shows the label! """

        if not self.is_label():
            return None

        return f'<img src="{self.label_url()}"/>'
