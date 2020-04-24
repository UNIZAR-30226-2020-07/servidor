import unittest

from test.manager import Manager

manager = Manager()


class NotLoggedInUsers(unittest.TestCase):

    def setUp(self):
        """
        Prepare a no login user
        """
        manager.logout()

    def test_SetLastSong(self):
        """
        Change the last song of a no login user
        """
        self.assertIsNotNone(manager.setLasts())

    def test_LastSong(self):
        """
        Check the last song listen of a no login user
        """
        self.assertIsNotNone(manager.getLastSongPlayed())

    def test_LastSecond(self):
        """
        Chech the last second listen of a no login user
        """
        self.assertIsNotNone(manager.getLastSecondPlayed())

    def test_SetValoration(self):
        """
        Set a valoration when you're not login
        """
        self.assertIsNone(manager.setValorations(1, 5))


class LoggedInUsers(unittest.TestCase):

    def setUp(self):
        """
        Login with 'user' account
        """
        manager.login('user', 'user')
        c_user = manager.getCurrentUser()
        self.assertIsNotNone(c_user)

    def test_SetLastSong(self):
        """
        Change last song listen for user
        """
        self.assertIsNone(manager.setLasts())

    def test_LastSong(self):
        """
        Check the last song listen for user
        """
        self.assertIsNotNone(manager.getLastSongPlayed())

    def test_LastSecond(self):
        """
        Check the last second listen for user
        """
        self.assertIsNotNone(manager.getLastSecondPlayed())

    def test_SetValortion(self):
        """
        Set a valoration for song 1
        """
        self.assertIsNotNone(manager.setValorations(1, 5))

    def test_ReadValortion(self):
        """
        Read valorations for song 1
        """
        self.assertIsNotNone(manager.readValorations(1))


if __name__ == '__main__':
    unittest.main()
