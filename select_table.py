import os
import typing
import click

from abc import ABC, abstractmethod

import image
import decoration_types


class DecorationTableElement(ABC):

    @staticmethod
    def _shift_right(line: str, amount: int = 4):
        return (' ' * amount) + line

    @abstractmethod
    def to_html(self):
        pass


class DecorationTableCell(image.Decoration, DecorationTableElement):

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
        ).replace('\\', '/')

    @classmethod
    def __load_cell_template(cls,):
        """ Loads the cell template file, and saves its content in the
        memory. """

        path = os.path.join(cls.TEMPLATES_FOLDER, cls.CELL_TEMPLATE)

        with open(path, 'r') as file:
            return file.read().splitlines()

    @staticmethod
    def __remove_from_html_template(template: typing.List[str],
                                    query: str):
        """ Recives an html element template (list of strings,
        each string is a line) and a query. See implementation for more
        information. """

        start_query = f'<!-- IF {query} -->'
        end_query = f'<!-- FI {query} -->'

        deleting = False
        new_template = list()

        for line in template:

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
            '%DECORATIONNAME%', self.name)

        # Converting list to one string
        # the `%0D` char is somewhat like `\n`, and converts the list
        # to a single string.
        body = '%0D'.join(self.ISSUE_BODY_TEMPLATE)

        return f'https://github.com/RealA10N/RealA10N/issues/new?title={title}&body={body}'

    def to_html(self,) -> typing.List[str]:
        """ Returns the cell representation in html, as a list of strings. """

        # Loads the cell template if not loaded yet (static property)
        if self.__cell_template is None:
            self.__cell_template = self.__load_cell_template()
        template = self.__cell_template

        # If current decoration type doesn't have a label
        # removes the label part from the template
        is_label = self.type_cls.is_label()
        if not is_label:
            template = self.__remove_from_html_template(template, 'label')

        result = list()

        # Replace values in the template
        for line in template:

            line = line.replace('{{REDIRECT_URL}}',
                                self.__issue_redirect_url())

            line = line.replace(
                '{{IMAGE_PATH}}', self.__relative_path_to_example())

            line = line.replace('{{NAME}}', self.name.capitalize())

            if is_label:
                line = line.replace('{{LABEL_URL}}', self.type_cls.label_url())

            result.append(line)

        return result


class DecorationTableRow(DecorationTableElement):

    def __init__(self, cells: typing.List[DecorationTableCell] = None):

        if cells is None:
            cells = list()

        self.__cells = list()

        for cell in cells:
            self.add_cell(cell)

    def add_cell(self, cell: DecorationTableCell) -> None:
        """ Adds a single cell to the row. """

        if not isinstance(cell, DecorationTableCell):
            raise TypeError("Incompatible cell type")

        self.__cells.append(cell)

    def to_html(self,) -> typing.List[str]:
        """ Returns the representation of the table row in html, as a 
        list of strings. """

        # sort the cell list
        cells = list(self.__cells)
        cells.sort(key=lambda cell: cell.name)

        # For each cell in the row, generate the html and add to `lines`
        lines = list()
        for cell in cells:
            lines += cell.to_html()

        # Add the <tr> tags, shift lines to the right and return result!
        return ['<tr>'] + [self._shift_right(line) for line in lines] + ['</tr>']


class DecorationTable(DecorationTableElement):

    MAX_CELLS_IN_ROW = 4

    def __init__(self, cells: typing.List[DecorationTableCell] = None):

        if cells is None:
            cells = list()

        self.__types = dict()

        for cell in cells:
            self.add_cell(cell)

    def add_cell(self, cell: DecorationTableCell):
        """ Adds a single cell to the table. It will be sorted and places
        in the currect row automatically. """

        cell_type = cell.type

        if cell_type in self.__types:
            # If the cell type is already known (and has a row dedicated to it)
            self.__types[cell_type].append(cell)

        else:
            # If not, creates a new row and saves it!
            self.__types[cell_type] = [cell]

    def __generate_table_rows(self) -> typing.List[DecorationTableRow]:
        """ Generates and returns instances of `DecorationTableRow`. Each
        row contains a maximum of `MAX_CELLS_IN_ROW` items in it, and the
        items ordered by their types. """

        # Loads the cells to one list, but saves the order of
        # the types inside the general config file.
        cells = list()
        for cur_type in decoration_types.TYPES_TABLE:
            if cur_type in self.__types:
                cells += self.__types[cur_type]

        # Converts the one long list of cells into a list of lists.
        # 'Slice' the cells into rows.

        row_cells = list()
        for index, cell in enumerate(cells):

            row = int(index / self.MAX_CELLS_IN_ROW)
            in_row = index % self.MAX_CELLS_IN_ROW

            if in_row == 0:
                # If it is a start of a new row: creates a new row.
                row_cells.append(list())

            # Adds the current cell to its row.
            row_cells[row].append(cell)

        # Converts the list of list of cells into a list of rows, and returns.
        return [DecorationTableRow(cur_row_cells) for cur_row_cells in row_cells]

    def to_html(self) -> typing.List[str]:
        """ Generates and returns the representation of the table in html,
        as a list of strings. """

        lines = list()
        for row in self.__generate_table_rows():
            lines += row.to_html()

        return ['<table>'] + [self._shift_right(line) for line in lines] + ['</table>']


@click.command()
@click.argument('output-path', default='select_table.html')
def main(output_path):

    # Generating the 'select decoration' table
    table = DecorationTable()
    for dec_name in DecorationTableCell.avaliable_decorations():
        cell = DecorationTableCell(dec_name)
        table.add_cell(cell)

    # Saving the generated table into the given filepath
    to_write = '\n'.join(table.to_html())
    with open(output_path, 'w') as file:
        file.write(to_write)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
