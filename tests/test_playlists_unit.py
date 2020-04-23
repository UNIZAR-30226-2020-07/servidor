import unittest

from tests.manager import Manager

# intialize
manager = Manager()
idPlaylist = -1
current_id = 0


class NotLoggedIn(unittest.TestCase):

    def setUp(self):
        """
        Create a example playlists and logged out
        """
        global idPlaylist
        if idPlaylist == -1:
            manager.login('user', 'user')
            idPlaylist = manager.createPlaylist('cuarentena2', [20])
            self.assertIsNot(idPlaylist, -1)
        manager.key = None

    def test_Create(self):
        """
        Create a playlists when you're not login
        """
        self.assertIsNotNone(manager.createPlaylist('cuarentena', 20))

    def test_Edit(self):
        """
        Edit the example playlist when you're not login
        """
        self.assertIsNotNone(manager.editPlaylist(str(idPlaylist), 'cuarentenaNoLogin', [10]))

    def test_Delete(self):
        """
        Delete the example playlists when you're not login
        """
        self.assertIsNotNone(manager.deletePlaylist(str(idPlaylist)))


class LoggedWihtOtherAccount(unittest.TestCase):

    def setUp(self):
        """
        Create a example playlist and log in with other user
        """
        global idPlaylist
        if idPlaylist == -1:
            manager.login('user', 'user')
            idPlaylist = manager.createPlaylist('cuarentena2', [20])
            self.assertIsNot(idPlaylist, -1)
        manager.login('user2', 'user2')
        self.assertIsNotNone(manager.getCurrentUser())

    def test_Edit(self):
        """
        Edit a non personal playlists
        """
        self.assertIsNotNone(manager.editPlaylist(str(idPlaylist), 'cuarentena25', [12]))

    def test_Delete(self):
        """
        Delete a non personal playlist
        """
        self.assertIsNotNone(manager.deletePlaylist(str(idPlaylist)))


class LoggedOwnersAccount(unittest.TestCase):

    def setUp(self):
        """
        Create a exmaple playlist and still with this user
        """
        manager.login('user', 'user')
        global idPlaylist
        global current_id
        if idPlaylist == -1:
            idPlaylist = manager.createPlaylist('cuarentena2', [20])
            self.assertIsNot(idPlaylist, -1)
        c_user = manager.getCurrentUser()
        self.assertIsNotNone(c_user)
        current_id = c_user['id']

    def test_Edit(self):
        """
        Edit name and songs of your own playlist
        """
        self.assertIsNotNone(manager.editPlaylist(str(idPlaylist), 'cuarentena35', [8]))

    def test_Delete(self):
        """
        Delete you own playlist
        """
        self.assertIsNone(manager.deletePlaylist(str(idPlaylist)))


if __name__ == '__main__':
    unittest.main()
