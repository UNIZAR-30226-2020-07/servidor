import sys

from tests.manager import Manager

# intialize
manager = Manager()

# set
if '--local' in sys.argv:
    manager.toggleLocal()

if '--debug' in sys.argv:
    manager.toggleDebug()

# start
current_id = None
#   Trying to operate with private fields without been logged in
if manager.setLasts() is None:
    print("Error at setting initial last song and second to user without been logged")

if manager.getLastSongPlayed() is None:
    print("Error at reading last song from user without been logged")

if manager.getLastSecondPlayed() is None:
    print("Error at reading last second from user without been logged")

#   Trying to operate with private fields while been logged in
manager.login('user', 'user')
c_user = manager.getCurrentUser()
current_id = c_user['id']

if manager.setLasts() is not None:
    print("Error at setting initial last song and second to user:")
    print(current_id)

if manager.getLastSongPlayed() is None:
    print("Error at reading last song from user while logged in")
    print(current_id)

if manager.getLastSecondPlayed() is None:
    print("Error at reading last second from user while logged in")
    print(current_id)

if manager.setValorations(1, 5) is None:
    print("Error at setting valoration for song 1")

if manager.readValorations(1) is not 5:
    print("Error at setting valoration for song 1")