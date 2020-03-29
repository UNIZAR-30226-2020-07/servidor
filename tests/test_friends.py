import sys

from tests.manager import Manager

# intialize
manager = Manager()

if '--local' in sys.argv:
    manager.toggleLocal()

if '--debug' in sys.argv:
    manager.toggleDebug()

# start
manager.register('sin_amigos2', 'unAmigo@porfa.pls', 'AFICASNC@@@relleno', 'AFICASNC@@@relleno')
manager.login('unAmigo@porfa.pls', 'AFICASNC@@@relleno')

c_user = manager.getCurrentUser()
id = c_user['id']

if manager.addFollowed(id, 2) is not None:
    print("Error at adding a user to the Followed list")

if manager.deleteFollowed(id, 2) is not None:
    print("Error at deleting a user to the Followed list")
