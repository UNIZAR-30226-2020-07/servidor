import unittest

from test.manager import Manager

manager = Manager()
current_id = 0


class TestFriendsNoLogin(unittest.TestCase):

    def setUp(self):
        """
        Prepare a non-register user
        """
        global current_id
        current_id = 0
        manager.logout()

    def test_AddErrorUser(self):
        """
        Add one friend who doesn't exist when you're not login
        """
        self.assertIsNotNone(manager.addFollowed(current_id, -3))

    def test_AddUser(self):
        """
        Add one friend who exist when you're not login
        """
        self.assertIsNotNone(manager.addFollowed(current_id, 2))

    def test_DelUser(self):
        """
        Delete one friend who exist when you're not login
        """
        self.assertIsNotNone(manager.deleteFollowed(current_id, 2))

    def test_DelErrorUser(self):
        """
        Delete one friend who doesn't exist when you're not login
        """
        self.assertIsNotNone(manager.deleteFollowed(current_id, -3))


class TestFriendsLogin(unittest.TestCase):

    def setUp(self):
        """
        Prepare a register user and check if you're login
        """
        manager.register('sin_amigos21', 'unAmigoODos@porfa.pls', 'AFICASNC@@@relleno33', 'AFICASNC@@@relleno33')
        manager.login('unAmigoODos@porfa.pls', 'AFICASNC@@@relleno33')
        c_user = manager.getCurrentUser()
        global current_id
        current_id = c_user['id']
        self.assertIsNotNone(c_user)

    def test_AddErrorUser(self):
        """
        Add a non-existing user
        """
        self.assertIsNotNone(manager.addFollowed(current_id, -3))

    def test_AddUser(self):
        """
        Add a existing user
        """
        self.assertIsNone(manager.addFollowed(current_id, 2))

    def test_AddSameUser(self):
        """
        Re-add a existing user
        """
        self.assertIsNone(manager.addFollowed(current_id, 2))

    def test_AddOtherUser(self):
        """
        Add another user (more than 1)
        """
        self.assertIsNone(manager.addFollowed(current_id, 3))

    def test_DelUser(self):
        """
        Delete a friend who exist and is your friend
        """
        self.assertIsNone(manager.deleteFollowed(current_id, 2))

    def test_DelOtherUser(self):
        """
        Delete the other friend on your list
        """
        self.assertIsNone(manager.deleteFollowed(current_id, 3))

    def test_DelNoAddedUser(self):
        """
        Delete a non-friend user
        """
        self.assertIsNotNone(manager.deleteFollowed(current_id, 5))

    def test_DelErrorUser(self):
        """
        Delete a non-existing user
        """
        self.assertIsNotNone(manager.deleteFollowed(current_id, -3))


class AddYouToOtherList(unittest.TestCase):

    def setUp(self):
        """
        Prepare a user anc check if you're login
        """
        manager.register('sin_amigos21', 'unAmigoODos@porfa.pls', 'AFICASNC@@@relleno33', 'AFICASNC@@@relleno33')
        manager.login('unAmigoODos@porfa.pls', 'AFICASNC@@@relleno33')
        c_user = manager.getCurrentUser()
        global current_id
        current_id = c_user['id']
        self.assertIsNotNone(c_user)

    def test_ForceAddMeOtherErrorUser(self):
        """
        Force to other non-existing user to add you
        """
        self.assertIsNotNone(manager.addFollowed(-3, current_id))

    def test_ForceAddMeOtherUser(self):
        """
        Force to other existing user to add you
        """
        self.assertIsNotNone(manager.addFollowed(2, current_id))

    def test_ReForceAddMeOtherUser(self):
        """
        Re-force to other existing user to add you
        """
        self.assertIsNotNone(manager.addFollowed(2, current_id))

    def test_ForceDelMeOtherErrorUser(self):
        """
        Force to non-existing user to delete you
        """
        self.assertIsNotNone(manager.deleteFollowed(-3, current_id))

    def test_ForceDelMeOtherUser(self):
        """
        Force to other existing user to delete you
        """
        self.assertIsNotNone(manager.deleteFollowed(2, current_id))


if __name__ == '__main__':
    unittest.main()
