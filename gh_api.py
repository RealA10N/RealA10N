import typing
import requests


class AccessGitHub:

    API_ENDPOINT = r'https://api.github.com'
    __auth = None

    @classmethod
    def auth(cls, gb_username: str, token: str,):
        cls.__auth = (gb_username, token)

    def _access(self, url: str, **kwargs):
        url = f'{self.API_ENDPOINT}{url}'

        if self.__auth is not None:
            kwargs['auth'] = self.__auth

        return requests.request(url=url, **kwargs)

    def data(self,):
        return self._access(url='', method='get').json()


class AccessGitHubUser(AccessGitHub):

    def __init__(self, name: str):
        self.__name = name

    def _access(self, url: str, **kwargs):
        url = f'/users/{self.__name}{url}'
        return super()._access(url, **kwargs)

    def starred(self,) -> typing.Set[typing.Tuple[str]]:
        """ Returns a set of items that represent the repositories
        that the user starred. Each item is actually a tuple that has
        two values: the first one is the name of the repository owner,
        and the second one is the repository name itself. """

        return {
            (
                repo_data['owner']['login'].lower(),  # repo owner name
                repo_data['name'].lower(),            # repo name
            )
            for repo_data in self._access('/starred', method='get').json()
        }

    def is_starred(self, owner: str, name: str) -> bool:
        """ Returns `True` only if the given repository appears in the
        list of starred repositories of the user. """

        return (owner.lower(), name.lower()) in self.starred()

    def following(self,) -> typing.Set[str]:
        """ Returns a set of strings that represents the users that this
        user follows. """

        return {
            user_data['login'].lower()
            for user_data in self._access('/following', method='get').json()
        }

    def is_following(self, name: str) -> bool:
        """ Returns `True` only if the current user follows the given user
        on GitHub. """

        return name.lower() in self.following() or name.lower() == self.__name


class AccessGitHubRepo(AccessGitHub):

    def __init__(self, repo: str, owner: str):
        self.__repo = repo
        self.__owner = owner

    def _access(self, url: str, **kwargs):
        url = f'/repos/{self.__owner}/{self.__repo}{url}'
        return super()._access(url=url, **kwargs)


class AccessGitHubIssue(AccessGitHubRepo):

    REPO = 'RealA10N/RealA10N'

    def __init__(self, repo: str, owner: str, number: int):
        """ Recives the issue number and saves it. """
        super().__init__(repo, owner)
        self.__number = number

        self.__update_data = dict()
        self.__comment_data = list()

    def _access(self, url: str, **kwargs):
        url = f'/issues/{self.__number}{url}'
        return super()._access(url, **kwargs)

    def close_issue(self,):
        self.__update_data['state'] = 'closed'

    def open_issue(self,):
        self.__update_data['state'] = 'open'

    def add_label(self, name: str):
        if 'labels' not in self.__update_data:
            self.__update_data['labels'] = list()

        self.__update_data['labels'].append(name)

    def add_comment(self, body: str):
        self.__comment_data.append(body)

    def __push_comment(self, comment: str):
        self._access('/comments', method='post', json={"body": comment})

    def __push_update(self,):
        self._access('', method='patch', json=self.__update_data)

    def push(self,):
        if self.__update_data:
            self.__push_update()

        for comment in self.__comment_data:
            self.__push_comment(comment)
