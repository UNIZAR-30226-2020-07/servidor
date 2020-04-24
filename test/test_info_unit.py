import unittest

from test.manager import Manager

manager = Manager()


class InfoDataBase(unittest.TestCase):
    def test_Albums(self):
        """
        Check if all albums are ok
        """
        for data in manager.getAlbums():
            self.assertIsNotNone(data['name'])
            self.assertIsNotNone(data['songs'])
            self.assertIsNotNone(data['artist'])
            self.assertIsNotNone(data['podcast'])

    def test_Artists(self):
        """
        Check if all artists are ok
        """
        for data in manager.getArtists():
            self.assertIsNotNone(data['name'])
            self.assertIsNotNone(data['albums'])

    def test_Playlists(self):
        """
        Check if all playlists are ok
        """
        for data in manager.getAllPlaylist():
            self.assertIsNotNone(data['name'])

    def test_Songs(self):
        """
        Test if all songs are ok
        """
        for data in manager.getSongs():
            self.assertIsNotNone(data['title'])
            self.assertIsNotNone(data['duration'])
            self.assertIsNotNone(data['stream_url'])
            self.assertIsNotNone(data['album'])
            self.assertIsNotNone(data['genre'])
            self.assertGreaterEqual(data['count_valoration'], 0)
            if data['avg_valoration'] is None:
                self.assertEqual(data['count_valoration'], 0)
            else:
                self.assertGreater(data['count_valoration'], 0)
            if data['user_valoration'] is not None:
                self.assertLessEqual(data['user_valoration'], 5)
                self.assertGreaterEqual(data['user_valoration'], 1)
            else:
                self.assertIsNone(data['user_valoration'])


if __name__ == '__main__':
    unittest.main()
