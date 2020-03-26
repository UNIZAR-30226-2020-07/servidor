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
manager.login('user', 'user')
idPlaylist = manager.createPlaylist('cuarentena2', [20])
if not isinstance(idPlaylist, int):
    print("Error at create playlist, already loggin in")
    print(idPlaylist)

if manager.editPlaylist(str(idPlaylist), 'cuarentena3', [30]) is not None:
    print("Error at edit playlist, editing owners playlist")

manager.key = None
if manager.createPlaylist('cuarentena', 20) is None:
    print("Error, create playlist without login")

if manager.editPlaylist(str(idPlaylist), 'cuarentenaNoLogin', [10]) is None:
    print("Error, edit playlist without login")

if manager.deletePlaylist(str(idPlaylist)) is None:
    print("Error, delete playlist without login")

manager.login('user2', 'user2')
if manager.getCurrentUser() is None:
    print("Error at change user")

if manager.editPlaylist(str(idPlaylist), 'cuarentena25', [10]) is None:
    print("Error at edit playlist, editing others playlist")

if manager.deletePlaylist(str(idPlaylist)) is None:
    print("Error at deleting other's playlists")

manager.login('user', 'user')
if manager.getCurrentUser() is None:
    print("Error at change user")
if manager.deletePlaylist(str(idPlaylist)) is not None:
    print("Error at deleting your own playlist")
