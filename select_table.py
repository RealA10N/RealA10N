import os
import json
import typing

import image


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


class DecorationTableCell(image.Decoration):

    DECORATION_EXAMPLE_NAME = 'example.png'

    TEMPLATES_FOLDER = 'templates'
    CELL_TEMPLATE = 'select_decoration_template.html'

    ISSUE_TITLE_TEMPLATE = 'visitREADME|%DECORATIONNAME%'
    ISSUE_BODY_TEMPLATE = [
        'Just click the `Submit new issue` button!',
        'Your profile picture should appear on my README page in about a minute.',
        '(%3B',  # -> (;
    ]

    __cell_template = None

    def __relative_path_to_example(self,):
        """ Returns the relative path to the current decoration example
        image. """

        return os.path.join(
            self._this_folder(),
            self.DECORATION_EXAMPLE_NAME,
        )

    @ classmethod
    def __load_cell_template(cls,):
        """ Loads the cell template file, and saves its content in the
        memory. """

        path = os.path.join(cls.TEMPLATES_FOLDER, cls.CELL_TEMPLATE)

        with open(path, 'r') as file:
            return file.read().splitlines()

    def __remove_from_html_template(self,
                                    template: typing.List[str],
                                    query: str):
        """ Recives an html element template (list of strings,
        each string is a line) and a query. See implementation for more
        information. """

        start_query = f'<!-- IF {query} -->'
        end_query = f'<!-- FI {query} -->'

        deleting = False
        new_template = list()

        for index, line in enumerate(template):

            if start_query in line:
                deleting = not deleting

            if not deleting:
                new_template.append(line)

            if end_query in line:
                deleting = not deleting

        return new_template

    def __issue_redirect_url(self,) -> str:
        """ Returns the url that the user will be redirected to when he clicks
        on the decoration. It's a url to create a new issue, with the name
        of the decoration in the title. """

        title = self.ISSUE_TITLE_TEMPLATE.replace(
            '%DECORATIONNAME%', self._name)

        # Converting list to one string
        # the `%0D` char is somewhat like `\n`, and converts the list
        # to a single string.
        body = '%0D'.join(self.ISSUE_BODY_TEMPLATE)

        return f'https://github.com/RealA10N/RealA10N/issues/new?title={title}&body={body}'

    def decoration_type(self,):
        """ Returns an `DecorationType` instance, that represents the type
        of the current decoration instance. """

        dec_type = self._config['type']
        return DecorationType(dec_type)

    def to_html(self,) -> str:

        # Loads the cell template if not loaded yet (static property)
        if self.__cell_template is None:
            self.__cell_template = self.__load_cell_template()
        template = self.__cell_template

        # If current decoration type doesn't have a label
        # removes the label part from the template
        dec_type = self.decoration_type()
        is_label = dec_type.is_label()
        if not is_label:
            template = self.__remove_from_html_template(template, 'label')

        result = list()

        # Replace values in the template
        for line in template:

            line = line.replace('{{REDIRECT_URL}}',
                                self.__issue_redirect_url())

            line = line.replace(
                '{{IMAGE_PATH}}', self.__relative_path_to_example())

            if is_label:
                line = line.replace('{{LABEL_URL}}', dec_type.label_url())

            result.append(line)

        return result
