import requests


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

    def _fetch(self, url, body=None, token=None, method=None, params=None):
        """
        Makes the online petition (GET or POST)
        :param url: url to fetch
        :param body: If json data => POST, if None => GET, other method's are specified on the "method" param
        :param token: authentication token
        :param params: parameters to the url, dictionary of key:values, for example params={"search":"something"}
        :return: (json, error) where json is the result as json, and error is a boolean indicating if there was an error
        """

        # method
        if method is None:
            method = "GET" if body is None else "POST"

        # url
        if not url.startswith("http"):
            url = (self.BASE_URL_LOCAL if self.uselocal else self.BASE_URL) + url + ("/" if not url.endswith("/") else "")

        # headers
        headers = {'Authorization': f'Token {token}'} if token is not None else {}

        # make request
        r = requests.request(method=method, url=url, params=params, json=body, headers=headers)

        # parse and return
        code = r.status_code
        try:
            jsonObject = r.json()
        except ValueError:
            jsonObject = None

        # debug
        if self.debug:
            print(f"{url} => ({code}) => {jsonObject}")

        return jsonObject, not 200 <= code < 300

    def formatErrors(self, result):
        """
        Utility to format dict of list into list
        """
        errors = []
        for field in result:
            for message in result[field]:
                errors.append('{}: {}'.format(field, message))
        return errors

    def depaginate(self, data):
        """
        Yields all the items by performing subsecuent gets for paginated data.
        Errors in subsecuent gets are ignored.
        :param data: an object result of a paginates get, should contain a 'results' with the list of elements to yield and a 'next' with the next page to get.
        """
        while True:
            for result in data['results']:
                yield result
            next = data['next']
            if next is None:
                break
            data, _ = self._fetch(next)

    def getSongs(self):
        """
        GET songs
        """
        data, _ = self._fetch('songs')
        return self.depaginate(data)

    def getArtists(self):
        """
        GET artists
        """
        data, _ = self._fetch('artists')
        return self.depaginate(data)

    def getAlbums(self):
        """
        GET albums
        """
        data, _ = self._fetch('albums')
        return self.depaginate(data)

    def getPlaylist(self, n_playlist):
        """
        GET playlist
        :param n_playlist: playlist to fetch
        """
        url = 'playlists/' + n_playlist
        data, _ = self._fetch(url)
        return data

    def getAllPlaylist(self):
        """
        GET all playlist from the server
        """
        data, _ = self._fetch('playlists')
        return self.depaginate(data)

    def createPlaylist(self, p_name, songs):
        """
        CREATE playlist
        :param p_name: name of the playlist
        :param songs: list of songs
        """
        url = 'playlists'
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
        url = 'playlists/' + n_playlist
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
        url = 'playlists/' + n_playlist
        data, error = self._fetch(url, None, self.key, 'DELETE')
        if error:
            # error
            return self.formatErrors(data)

    def getUserPlaylists(self, user_id):
        url = 'users/' + str(user_id)
        data, error = self._fetch(url, None, self.key, None)
        if error:
            # error
            return self.formatErrors(data)
        # list_p = []
        # for playlist in data['playlists']:
        #    list_p = list_p + playlist

        return data['playlists']

    def register(self, username, email, password1, password2):
        """
        Register a new user
        """
        result, error = self._fetch('rest-auth/registration', {
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
        result, error = self._fetch('rest-auth/login', {
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

    def addFollowed(self, username_id, followed_user):
        """
        ADD a user to the "friend" list of a user
        :param username_id: principal user
        :param followed_user: username of the "friend" to add
        """
        url = 'users/' + str(username_id)
        data, error = self._fetch(url, None, self.key, None)
        if error:
            # error
            return self.formatErrors(data)

        new_friends = [user['id'] for user in data['friends']] + [followed_user]
        data, error = self._fetch(url, {'friends': new_friends}, self.key, 'PATCH')

        if error:
            # error
            return self.formatErrors(data)

    def deleteFollowed(self, username_id, followed_user):
        """
        DELETE a user from the "friend" list of a user
        :param username_id: principal user
        :param followed_user: username of the "friend" to delete
        """
        url = 'users/' + str(username_id)
        data, error = self._fetch(url, None, self.key, None)
        if error:
            # error
            return self.formatErrors(data)

        if followed_user in [user['id'] for user in data['friends']]:
            [user['id'] for user in data['friends']].remove(followed_user)
            data, error = self._fetch(url, {'friends': [user['id'] for user in data['friends']]}, self.key, 'PATCH')

        else:
            return "No friend found"

        if error:
            # error
            return self.formatErrors(data)

    def getFriends(self, user_id):
        url = 'users/' + str(user_id)
        data, error = self._fetch(url, None, self.key, None)
        if error:
            # error
            return self.formatErrors(data)
        return data['friends']

    def getLastSongPlayed(self):
        """
        GET the information of the last song that the user "user_id" played
        :param user_id: user from wich to extract last song played
        """
        url = 'rest-auth/user'
        data, error = self._fetch(url, None, self.key, None)
        if error:
            # error
            return self.formatErrors(data)
        return data['pause_song']

    def getLastSecondPlayed(self):
        """
        GET the information of the last song that the user "user_id" played
        :param user_id: user from wich to extract last song played
        """
        url = 'rest-auth/user'
        data, error = self._fetch(url, None, self.key, None)
        if error:
            # error
            return self.formatErrors(data)
        return data['pause_second']

    def setLasts(self):
        """
        GET the information of the last song that the user "user_id" played
        :param user_id: user from wich to extract last song played
        """
        url = 'rest-auth/user'
        data, error = self._fetch(url, {'pause_song': 1, 'pause_second': 1}, self.key, 'PATCH')
        if error:
            # error
            return self.formatErrors(data)

    def getUserAlbums(self, user_id):
        """
        GET the information of the albums that the user "user_id" has
        :param user_id: user from wich to extract the albums
        """
        url = 'users/' + str(user_id)
        data, error = self._fetch(url, None, self.key, None)
        if error:
            # error
            return self.formatErrors(data)
        # list_a = []
        # for album in data['albums']:
        #   list_a = list_a + album

        return data['albums']

    def searchSong(self, search_parameter):
        """
        GET elements that have the desired parameter in the songs search_fields
        :param seach_parameter: desired match to find on the search
        """
        url = 'songs/'
        data, error = self._fetch(url, None, self.key, None, {"search": search_parameter})
        if error:
            # error
            return self.formatErrors(data)
        if data['count'] == 0:
            return None
        else:
            return data['results']

    def searchEpisode(self, search_parameter):
        """
        GET elements that have the desired parameter in the songs search_fields
        :param seach_parameter: desired match to find on the search
        """
        url = 'songs/'
        data, error = self._fetch(url, None, self.key, None, {"episode": "true"})
        if error:
           # error
           return self.formatErrors(data)
        if data['count'] == 0:
           return None
        else:
           return data['results']

    def searchAlbum(self, search_parameter):
        """
        GET elements that have the desired parameter in the albums search_fields
        :param seach_parameter: desired match to find on the search
        """
        url = 'albums/'
        data, error = self._fetch(url, None, self.key, None, {"search": search_parameter})
        if error:
            # error
            return self.formatErrors(data)
        if data['count'] == 0:
            return None
        else:
            return data['results']

    def searchPodcast(self, search_parameter):
        """
        GET elements that have the desired parameter in the albums search_fields
        :param seach_parameter: desired match to find on the search
        """
        url = 'albums/'
        data, error = self._fetch(url, None, self.key, None, {"podcast": "true"})
        if error:
            # error
            return self.formatErrors(data)
        if data['count'] == 0:
            return None
        else:
            return data['results']

    def searchArtists(self, search_parameter):
        """
        GET elements that have the desired parameter in the Artists search_fields
        :param seach_parameter: desired match to find on the search
        """
        url = 'artists/'
        data, error = self._fetch(url, None, self.key, None, {"search": search_parameter})
        if error:
            # error
            return self.formatErrors(data)
        if data['count'] == 0:
            return None
        else:
            return data['results']

    def searchPlaylists(self, search_parameter):
        """
        GET elements that have the desired parameter in the playlists search_fields
        :param seach_parameter: desired match to find on the search
        """
        url = 'playlists/'
        data, error = self._fetch(url, None, self.key, None, {"search": search_parameter})
        if error:
            # error
            return self.formatErrors(data)
        if data['count'] == 0:
            return None
        else:
            return data['results']

    def searchUser(self, search_parameter):
        """
        GET elements that have the desired parameter in the users search_fields
        :param seach_parameter: desired match to find on the search
        """
        url = 'users/'
        data, error = self._fetch(url, None, self.key, None, {"search": search_parameter})
        if error:
            # error
            return self.formatErrors(data)
        if data['count'] == 0:
            return None
        else:
            return data['results']

    def setValorations(self, song_id, valoration):
        """
        GET elements that have the desired parameter in the users search_fields
        :param seach_parameter: desired match to find on the search
        """
        url = 'songs/' + str(song_id)
        data, error = self._fetch(url, {"user_valoration": valoration}, self.key, 'PATCH', None)
        if error:
            return None
        else:
            return data

    def readValorations(self, song_id):
        """
        GET elements that have the desired parameter in the users search_fields
        :param seach_parameter: desired match to find on the search
        """
        url = 'songs/' + str(song_id)
        data, error = self._fetch(url, None, self.key, None, None)
        if error:
            return None
        else:
            return data['user_valoration']

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
