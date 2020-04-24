import unittest

from test.manager import Manager

# intialize
manager = Manager()


class ExistingElements(unittest.TestCase):

    def test_Song(self):
        """
        Search a existing song
        """
        self.assertIsNotNone(manager.searchSong('the'))

    def test_Artist(self):
        """
        Search a existing artist
        """
        self.assertIsNotNone(manager.searchArtists('jojo'))

    def test_Album(self):
        """
        Search a existing album
        """
        self.assertIsNotNone(manager.searchAlbum('jojo'))

    def test_Playlist(self):
        """
        Search a existing playlist
        """
        self.assertIsNotNone(manager.searchPlaylists('world'))

    def test_Episode(self):
        """
        Search a existing episode
        """
        self.assertIsNotNone(manager.searchEpisode('world'))

    def test_Podcast(self):
        """
        Search a existing podcast
        """
        self.assertIsNotNone(manager.searchPodcast('world'))


class ExistingUsers(unittest.TestCase):

    def test_Username(self):
        """
        Search a existing user by username
        """
        self.assertIsNotNone(manager.searchUser('user'))

    def test_Email(self):
        """
        Search a existing user by email
        """
        self.assertIsNotNone(manager.searchUser('user@user.user'))


class NOTExistingElements(unittest.TestCase):

    def test_Song(self):
        """
        Search a non-existing song
        """
        self.assertIsNone(manager.searchSong('hfwebonjnvwmpok1sp'))

    def test_Artist(self):
        """
        Search a non-existing artist
        """
        self.assertIsNone(manager.searchArtists('hfwebonjnvwmpok1sp'))

    def test_Album(self):
        """
        Search a non-existing album
        """
        self.assertIsNone(manager.searchAlbum('hfwebonjnvwmpok1sp'))

    def test_Playlist(self):
        """
        Searcb a non-existing playlist
        """
        self.assertIsNone(manager.searchPlaylists('hfwebonjnvwmpok1sp'))


class NOTExistingUsers(unittest.TestCase):

    def test_Username(self):
        """
        Search a non-existing user by username
        """
        self.assertIsNone(manager.searchUser('uuuuuuser'))

    def test_Email(self):
        """
        Search a non-existing user by email
        """
        self.assertIsNone(manager.searchUser('uuuuuuser@uuuuuuser.uuuuuuser'))


if __name__ == '__main__':
    unittest.main()
