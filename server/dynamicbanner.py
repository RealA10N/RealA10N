from PIL import Image
from abc import ABC, abstractmethod
from simplejsondb import Database


class DynamicBanner(ABC):

    visits_between_saves = 10

    def __init__(self, db_path: str):
        self.db = Database(db_path, default={
            'visitors': 0,
        })

    def __next__(self,) -> Image.Image:
        self.db.data['visitors'] += 1

        if self.db.data['visitors'] % self.visits_between_saves == 0:
            # If its time to save the database locally, saves it!
            # TODO: can be improved by saving only after response,
            # and not while the user waits.
            self.db.save()

        return self()

    @abstractmethod
    def __call__(self,) -> Image.Image:
        """ An abstract method that generates the banner and returns it.
        Does not change the state of the object - changing the state should
        be done in the `__next__` method. """
