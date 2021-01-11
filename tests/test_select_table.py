import typing
import os
import json

import requests

from select_table import DecorationType


class TestDecorationTypes:

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
