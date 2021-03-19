import typing

from abc import ABC, abstractclassmethod
from gh_api import AccessGitHubUser


class DecorationType(ABC):

    LABEL: typing.Optional[dict]  # abstract

    @abstractclassmethod
    def check_username(cls, username: str):
        """ Checks and returns `True` only if the given github username
        is allowed to use decorations from the current type. Abstract
        method. """

    @classmethod
    def is_label(cls,) -> bool:
        """ Returns `True` if the current decoration type has a special label.
        For example, the 'following' decoration type has a special label,
        that is displayed in the README.md file (: """

        return bool(cls.LABEL)

    @classmethod
    def label_url(cls,) -> typing.Optional[str]:
        """ Returns the url that contains the label image. `None` if there
        is no label to the current decoration type. """

        if not cls.is_label():
            return None

        text, color = cls.LABEL['TEXT'], cls.LABEL['COLOR']
        return f'https://img.shields.io/badge/-{text}-{color}'


class DefaultDecorationType(DecorationType):

    LABEL = None

    @classmethod
    def check_username(cls, _):
        """ Everyone can use the decoration in the default type,
        so this method always returns `True`. """
        return True


class FollowingDecorationType(DecorationType):

    LABEL = {
        "COLOR": 'orange',
        "TEXT": 'followers only'
    }

    @classmethod
    def check_username(cls, username: str):
        """ Checks if the given username actually follows me on GitHub,
        and returns `True` only if he is . """

        user = AccessGitHubUser(username)
        return user.is_following('RealA10N')  # My GitHub username (:


TYPES_TABLE = {
    'default': DefaultDecorationType,
    'following': FollowingDecorationType,
}
