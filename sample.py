import json
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class Manager:
    BASE_URL = 'https://ps-20-server-django-app.herokuapp.com/api/v1'

    # BASE_URL = 'http://127.0.0.1:8000/api/v1'

    def __init__(self):
        """
        Python things, indicates this object has a key variable
        """
        self.key = None

    def _fetch(self, url, body=None, token=None):
        """
        Makes the online petition (GET or POST)
        :param url: url to fetch
        :param body: If json data => POST, if None => GET
        :param token: authentication token
        :return: json result
        """

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
        request = Request(url=url, data=data, headers=headers)

        try:
            # get response
            result = urlopen(request).read().decode()
        except HTTPError as e:
            # get response in case of error
            result = e.read().decode()

        # parse and return
        jsonObject = json.loads(result)
        # print(url, "=>", jsonObject)  # debug
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
        url = self.BASE_URL + '/songs/'
        while url is not None:
            data = self._fetch(url)
            for song in data['results']:
                yield song
            url = data['next']

    def register(self, username, email, password1, password2):
        """
        Register a new user
        """
        result = self._fetch(self.BASE_URL + '/rest-auth/registration/', {
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
        result = self._fetch(self.BASE_URL + '/rest-auth/login/', {
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
        return self._fetch(self.BASE_URL + '/rest-auth/user/', token=self.key)


if __name__ == '__main__':
    manager = Manager()

    while True:
        option = input("""
What do you want to do?
1) Get list of songs
2) Register new user
3) Login existing user
4) Get current user data
5) Get list of playlists

9) Exit
>""")
        if option == '1':
            print("Example of fetching songs:")
            songs = manager.getSongs()
            for song in songs:
                album = song['album']
                artist = album['artist']
                print("Song '{title}' of genre {genre} has a duration of {duration} seconds".format(**song))
                print("    and it's from the album '{name}'".format(**album))
                print("    made by {name}".format(**artist))

        elif option == '2':
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

        elif option == '3':
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

        elif option == '4':
            print("Example of retrieving auth data")
            user = manager.getCurrentUser()
            if user is None:
                print('You must authenticate first')
            else:
                print("Your username is '{username}' and your email '{email}'".format(**user))

        elif option == '5':
            print("Example of fetching playlists:")
            playlists = manager.getPlaylists()
            for playlist in playlists:
                print("Playlist with title {name} have :".format(**playlist))
                print("    and it's from the album '{name}'".format(**album))
                print("    made by {name}".format(**artist))

        elif option == '9':
            break

        else:
            print("unknown option, try again")
