import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class Manager:
    BASE_URL = 'https://ps-20-server-django-app.herokuapp.com/api/v1/'

    BASE_URL_LOCAL = 'http://127.0.0.1:8000/api/v1/'

    def __init__(self):
        """
        Python things, indicates this object has a key variable
        """
        self.key = None
        self.uselocal = False
        self.debug = False

    def _fetch(self, url, body=None, token=None, method=None):
        """
        Makes the online petition (GET or POST)
        :param url: url to fetch
        :param body: If json data => POST, if None => GET, other method's are specified on the "method" param
        :param token: authentication token
        :return: (json, error) where json is the result as json, and error is a boolean indicating if there was an error
        """

        # url
        if not url.startswith("http"):
            url = (self.BASE_URL_LOCAL if self.uselocal else self.BASE_URL) + url

        # format json body
        if body is None:
            data = None
        else:
            data = bytes(json.dumps(body), encoding='utf8')  # urlencode(body).encode()

        # prepare token header
        if token is None:
            headers = {}
        else:
            headers = {'Authorization': 'Token {}'.format(token)}
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'

        # make request
        request = Request(url=url, data=data, headers=headers, method=method)

        try:
            # get response
            result = urlopen(request).read().decode()
            error = False
        except HTTPError as e:
            # get response in case of error
            if e.code is 500:
                # server error
                print("Server error")
                raise e
            result = e.read().decode()
            error = True

        # parse and return
        jsonObject = json.loads(result) if result is not None and result is not '' else None
        if self.debug:
            print(url, "=>", jsonObject)  # debug
        return jsonObject, error

    def formatErrors(self, result):
        """
        Utility to format dict of list into list
        """
        errors = []
        for field in result:
            for message in result[field]:
                errors.append('{}: {}'.format(field, message))
        return errors

    def getSongs(self):
        """
        GET songs
        """
        url = 'songs/'
        while url is not None:
            data, _ = self._fetch(url)
            for song in data['results']:
                yield song
            url = data['next']

    def getPlaylist(self, n_playlist):
        """
        GET playlist
        :param n_playlist: playlist to fetch
        """
        url = 'playlist/' + n_playlist + '/'
        data, _ = self._fetch(url)
        return data

    def getAllPlaylist(self):
        """
        GET all playlist from the server
        """
        url = 'playlist/'
        while url is not None:
            data, _ = self._fetch(url)
            for playlist in data['results']:
                yield playlist
            url = data['next']

    def createPlaylist(self, p_name, songs):
        """
        CREATE playlist
        :param p_name: name of the playlist
        :param songs: list of songs
        """
        url = 'playlist/'
        data, error = self._fetch(url, {'name': p_name,
                                        'songs': songs}, self.key, 'POST')

        if error:
            # error
            return self.formatErrors(data)
        else:
            return data['id']

    def editPlaylist(self, n_playlist, new_name, new_songs):
        """
        EDIT playlist
        :param n_playlist: playlist to edit
        :param new_name: new name to give to given playlist
        :param new_songs: new list of songs to give to given playlist
        """
        url = 'playlist/' + n_playlist + '/'
        data, error = self._fetch(url, {'name': new_name,
                                        'songs': new_songs}, self.key, 'PUT')
        if error:
            # error
            return self.formatErrors(data)

    def deletePlaylist(self, n_playlist):
        """
        DELETE playlist
        :param n_playlist: playlist to delete
        """
        url = 'playlist/' + n_playlist + '/'
        data, error = self._fetch(url, None, self.key, 'DELETE')
        if error:
            # error
            return self.formatErrors(data)

    def register(self, username, email, password1, password2):
        """
        Register a new user
        """
        result, error = self._fetch('rest-auth/registration/', {
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2,
        })
        if not error:
            # save key
            self.key = result['key']
            return None
        else:
            # error
            return self.formatErrors(result)

    def login(self, username_email, password):
        """
        Log in as a user with email and passwaord
        """
        if '@' in username_email:
            username = ''
            email = username_email
        else:
            username = username_email
            email = ''
        result, error = self._fetch('rest-auth/login/', {
            'email': email,
            'username': username,
            'password': password,
        })
        if not error:
            # save key
            self.key = result['key']
            return None
        else:
            # error
            return self.formatErrors(result)

    def getCurrentUser(self):
        """
        Returns the current user data
        :return:
        """
        if self.key is None:
            # only if registered
            return None
        data, _ = self._fetch('rest-auth/user/', token=self.key)
        return data

    def toggleLocal(self):
        self.uselocal = not self.uselocal

    def toggleDebug(self):
        self.debug = not self.debug
