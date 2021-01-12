import typing
import os
import json

import requests

from select_table import (
    DecorationType,
    DecorationTable,
    DecorationTableCell,
)


class TestDecorationTypes:

    SELECT_TABLE_NAME = 'select_table.html'

    def test_types_general_config(self,):
        """ Tests the main general configuration file, and asserts that
        everything is ok and it contains all of the needed fields. """

        data_path = os.path.join(
            DecorationType.GENERAL_CONFIG_FOLDER,
            DecorationType.GENERAL_CONFIG_FILENAME
        )

        with open(data_path, 'r') as file:
            data = json.load(file)

        for type_data in data:
            assert 'type' in type_data, "All types must contain the `type` field"

            if 'label' in type_data:
                assert 'text' in type_data['label']
                assert 'color' in type_data['label']

    def test_types_labels(self,):
        """ Tests that each configuration file (excluding the main one)
        is ok and contains all of the needed fields. """

        for dec_type_name in DecorationType.avaliable_types():
            dec_type = DecorationType(dec_type_name)

            if dec_type.is_label():

                url = dec_type.label_url()
                response = requests.get(url)

                assert response.status_code == 200, f"Invalid url, label error {response.status_code}"
                assert 'image' in response.headers['content-type'], "Label not an image"

    def test_table_up_to_date(self,):
        """ Generates a new table, and compares it to the table saved
        in the `select_table` file. Test passes only if the tables
        are the same! """

        assert os.path.exists(
            self.SELECT_TABLE_NAME), "Select table isn't generated"

        # If file exists: generates a new table and compares the
        # files.

        # Generating the table
        table = DecorationTable()
        for dec_name in DecorationTableCell.avaliable_decorations():
            cell = DecorationTableCell(dec_name)
            table.add_cell(cell)
        base_lines = table.to_html()

        # Opening the saved table file
        with open(self.SELECT_TABLE_NAME, 'r') as file:
            file_lines = file.read().splitlines()

        # Assets that length of generated and loaded tables is the same
        assert len(base_lines) == len(
            file_lines), "Select table is not up to date"

        # Checking that each line is matching.
        # This check is seperated to lines (instead of checking if both lists
        # are equal without the loop) for more clear error messages
        for base_line, file_line in zip(base_lines, file_lines):
            assert base_line == file_line, "Select table is not up to date"
