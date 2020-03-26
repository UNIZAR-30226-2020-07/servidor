from tests.manager import Manager


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
