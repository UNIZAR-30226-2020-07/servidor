import sys

from tests.manager import Manager

# intialize
manager = Manager()

if '--debug' in sys.argv:
    manager.toggleDebug()

if '--local' in sys.argv:
    manager.toggleLocal()


# start
current_id = None

if manager.addFollowed(current_id, -3) is None:
    print("Error adding, invalid user without log in")

if manager.addFollowed(current_id, 2) is None:
    print("Error adding user without log in")

if manager.addFollowed(current_id, 2) is None:  # Django usually  prevents this error
    print("Error adding, already added users without log in")

if manager.deleteFollowed(current_id, 2) is None:
    print("Error at deleting a user to the Followed list without log in")

if manager.deleteFollowed(current_id, 5) is None:   #Django usually  prevents this error
    print("Error at deleting a user not added yet without log in")

if manager.deleteFollowed(current_id, -3) is None:
    print("Error at deleting a invalid username without log in")


manager.register('sin_amigos21', 'unAmigoODos@porfa.pls', 'AFICASNC@@@relleno33', 'AFICASNC@@@relleno33')
manager.login('unAmigoODos@porfa.pls', 'AFICASNC@@@relleno33')

c_user = manager.getCurrentUser()
current_id = c_user['id']


if manager.addFollowed(current_id, -3) is None:
    print("Error adding, invalid user without log in")

if manager.addFollowed(current_id, 2) is not None:
    print("Error adding user")

if manager.addFollowed(current_id, 3) is not None:
    print("Error adding user")

if manager.addFollowed(current_id, 2) is not None:  #Django usually  prevents this error
    print("Error adding, already added users")

if manager.addFollowed(current_id, 3) is not None:  #Django usually  prevents this error
    print("Error adding, already added users")

if manager.addFollowed(current_id, 2) is not None:  #Django usually  prevents this error
    print("Error adding, already added users")

if manager.deleteFollowed(current_id, 2) is not None:
    print("Error at deleting a user to the Followed list")

if manager.deleteFollowed(current_id, 5) is None:   #Django usually  prevents this error
    print("Error at deleting a user not added yet")

if manager.deleteFollowed(current_id, -3) is None:
    print("Error at deleting a invalid username")


if manager.addFollowed(-3, current_id) is None:
    print("Error adding, invalid user when try to touch another user's friends")

if manager.addFollowed(2, current_id) is None:
    print("Error adding user when try to touch another user's friends")

if manager.addFollowed(2, current_id) is None:  # Django usually  prevents this error
    print("Error adding, already added users when try to touch another user's friends")

if manager.deleteFollowed(2, current_id) is None:
    print("Error at deleting a user to the Followed list when try to touch another user's friends")

if manager.deleteFollowed(5, current_id) is None:   #Django usually  prevents this error
    print("Error at deleting a user not added yet when try to touch another user's friends")

if manager.deleteFollowed(-3, current_id) is None:
    print("Error at deleting a invalid username when try to touch another user's friends")