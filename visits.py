import os
import json
from datetime import datetime


class VisitContainer:

    def __init__(self, filepath):
        self.__filepath = filepath

        if os.path.isfile(self.__filepath):
            # If file exists, loads data from file.
            with open(self.__filepath, 'r') as file:
                self.__data = json.load(file)

        else:
            # If the file is not yet created, generates an empty data dict.
            self.__data = dict()

    def add(self, username: str):
        """ Registers the given visit into the database. """

        try:
            userdata = self.__data[username]

        except KeyError:
            # If username visits for the first time, generates default userdata
            userdata = {'visits': 0}

        # Update recent visit timestamp to current one
        userdata['timestamp'] = int(datetime.now().timestamp())

        # Increase visits count by one
        userdata['visits'] += 1

        # Save updated (or new) userdata back to database
        self.__data[username] = userdata

    def save(self,) -> None:
        """ Saves the table data back to the file. """

        with open(self.__filepath, 'w') as file:
            json.dump(self.__data, file, indent=4)
