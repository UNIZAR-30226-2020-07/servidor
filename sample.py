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
        jsonObject = json.loads(result)
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

    def getPlaylists(self, n_playlist):
        """
        GET playlist
        :param n_playlist: playlist to fetch
        """
        url = 'playlist/' + n_playlist + '/'
        data, _ = self._fetch(url)
        return data

    def createPlaylist(self, p_name, songs):
        """
        CREATE playlist
        :param p_name: name of the playlist
        :param url: list of songs
        """
        url = 'playlist/'
        data, error = self._fetch(url, {'name': p_name,
                                        'songs': songs}, self.key, 'POST')
        if error:
            # error
            return self.formatErrors(data)
        else:
            return None

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


class ConsoleMenu:
    def __init__(self):
        self.options = []
        self.running = True

    def add(self, label, description, function):
        self.options.append((label, description, function))

    def separation(self):
        self.add(None, None, None)

    def run(self):
        self.running = True
        while self.running:
            print()
            print("What do you want to do?")
            for label, desc, _ in self.options:
                if label is None:
                    print()
                else:
                    print("{}) {}".format(label, desc() if callable(desc) else desc))

            c = input(">")

            for label, _, func in self.options:
                if label == c:
                    func()
                    break
            else:
                print("unknown option, try again")

    def exit(self):
        self.running = False


if __name__ == '__main__':
    manager = Manager()

    menu = ConsoleMenu()


    def songs():
        print("Example of fetching songs:")
        songs = manager.getSongs()
        for song in songs:
            album = song['album']
            artist = album['artist']
            print("Song '{title}' of genre {genre} has a duration of {duration} seconds".format(**song))
            print("    and it's from the album '{name}'".format(**album))
            print("    made by {name}".format(**artist))


    menu.add("1", "Get list of songs", songs)


    def register():
        print("Example of register user")

        while True:
            username = input('Enter an username:')
            email = input('Enter an email:')
            password1 = input('Enter a password:')
            password2 = input('Repeat the password:')
            result = manager.register(username, email, password1, password2)
            if result is None:
                print('Done')
                break
            else:
                for msg in result:
                    print(msg)


    menu.add("2", "Register new user", register)


    def login():
        print("Example of login user")
        while True:
            username_email = input('Enter the username or email:')
            password = input('Enter the password:')
            result = manager.login(username_email, password)
            if result is None:
                print('Done')
                break
            else:
                for msg in result:
                    print(msg)


    menu.add("3", "Login existing user", login)


    def user():
        print("Example of retrieving auth data")
        user = manager.getCurrentUser()
        if user is None:
            print('You must authenticate first')
        else:
            print("Your username is '{username}' and your email '{email}'".format(**user))


    menu.add("4", "Get current user data", user)


    def createPlaylist():
        print('Example for create playlist')
        user = manager.getCurrentUser()
        if user is None:
            print('You must authenticate first')
        else:
            playlist_name = input('Enter the name of the playlist:')
            playlist_songs = input('Enter the songs of the playlist:')
            result = manager.createPlaylist(playlist_name, playlist_songs)
            if result is None:
                print('Done')
            else:
                for msg in result:
                    print(msg)


    menu.add("5", "Create new Playlist", createPlaylist)


    def viewPlaylist():
        print('List of actual playlists:')
        user = manager.getCurrentUser()
        if user is None:
            print('You must authenticate first')
        else:
            playlists = manager.getPlaylists()

            for playlist in playlists:
                print("Playlist '{name}'".format(**playlist))
                print("     with songs: '{songs}' .".format(**playlist))


    menu.add("6", "View user Playlist NO FUNCIONA", viewPlaylist)


    def addSongToPlaylist():
        print('List of actual playlists:')
        user = manager.getCurrentUser()
        if user is None:
            print('You must authenticate first')
        else:
            playlist_name = input('Enter the id of the playlist:')
            songtoadd = input('Enter the id of the song to add:')
            playlist = manager.getPlaylists(playlist_name)
            print(playlist['songs'])
            playlist['songs'] = playlist['songs'] + [(songtoadd)]
            print(playlist['songs'])
            manager.editPlaylist(playlist_name, None, playlist['songs'])


    menu.add("7", "Add song to playlist", addSongToPlaylist)


    def changeNameToPlaylist():
        print('List of actual playlists:')
        user = manager.getCurrentUser()
        if user is None:
            print('You must authenticate first')
        else:
            playlist_id = input('Enter the id of the playlist:')
            new_name = input('Enter the new name')
            playlist = manager.getPlaylists(playlist_id)
            print(playlist)
            manager.editPlaylist(playlist_id, 'asfr', [20])


    menu.add("8", "Change name to playlist", changeNameToPlaylist)

    menu.separation()

    menu.add("9", lambda: "Use local ({})".format(manager.uselocal), manager.toggleLocal)

    menu.add("10", lambda: "Debug ({})".format(manager.debug), manager.toggleDebug)

    menu.add("11", "Exit", menu.exit)

    menu.run()
