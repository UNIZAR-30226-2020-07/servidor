import json
from urllib.error import HTTPError
from urllib.parse import urlencode
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
        :param body: If json data => POST, if None => GET
        :param token: authentication token
        :return: json result
        """

        # url
        if not url.startswith("http"):
            url = (self.BASE_URL_LOCAL if self.uselocal else self.BASE_URL) + url

        # format json body
        if body is None:
            data = None
        else:
            data = urlencode(body).encode()

        # prepare token header
        if token is None:
            headers = {}
        else:
            headers = {'Authorization': 'Token {}'.format(token)}
        # make request
        request = Request(url=url, data=data, headers=headers, method=method)

        try:
            # get response
            result = urlopen(request).read().decode()
        except HTTPError as e:
            # get response in case of error
            result = e.read().decode()

        # parse and return
        jsonObject = json.loads(result)
        if self.debug:
            print(url, "=>", jsonObject)  # debug
        return jsonObject

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
            data = self._fetch(url)
            for song in data['results']:
                yield song
            url = data['next']

    def getPlaylists(self,n_playlist):
        """
        GET playlists
        """
        url = 'playlist/' + n_playlist
        data = self._fetch(url)
        return data

    def createPlaylist(self, p_name, songs):
        """
        CREATE playlist
        """
        url = 'playlist/'
        data = self._fetch(url, {'name': p_name,
                                 'songs': songs}, self.key, 'POST')
        if 'error' in data:
            # error
            return self.formatErrors(data)

    def editPlaylist(self, n_playlist, new_name=None, new_songs=None):
        """
        EDIT playlist
        """
        url = 'playlist/' + n_playlist
        nname = ""
        nsongs = ""
        if new_name is not None:
            nname = new_name
        if new_songs is not None:
            nsongs = new_songs

        data = self._fetch(url, {'name': nname,
                                 'songs': nsongs}, self.key, 'PUT')
        if 'error' in data:
            # error
            return self.formatErrors(data)

    def register(self, username, email, password1, password2):
        """
        Register a new user
        """
        result = self._fetch('rest-auth/registration/', {
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2,
        })
        if 'key' in result:
            # save key
            self.key = result['key']
            return None
        else:
            # error
            return self.formatErrors(result)

    def login(self, username_email, password):
        """
        Log in as a user
        """
        if '@' in username_email:
            username = ''
            email = username_email
        else:
            username = username_email
            email = ''
        result = self._fetch('rest-auth/login/', {
            'email': email,
            'username': username,
            'password': password,
        })
        if 'key' in result:
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
        return self._fetch('rest-auth/user/', token=self.key)

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
            manager.createPlaylist(playlist_name, playlist_songs)

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
            playlist['songs'] = playlist['songs'] + [int(songtoadd)]
            print(playlist['songs'])
            manager.editPlaylist(playlist_name, None, playlist['songs'])


    menu.add("7", "Add song to playlist", addSongToPlaylist)

    menu.separation()

    menu.add("9", lambda: "Use local ({})".format(manager.uselocal), manager.toggleLocal)

    menu.add("10", lambda: "Debug ({})".format(manager.debug), manager.toggleDebug)

    menu.add("11", "Exit", menu.exit)

    menu.run()
