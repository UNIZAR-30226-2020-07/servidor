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

if manager.check_song_info('1') is 0:
    print("Error en informacion de canciones")

if manager.check_album_info('1') is 0:
    print("Error en informacion de album")

if manager.check_artist_info('1') is 0:
    print("Error en informacion de artistas")

if manager.check_playlists_info('1') is 0:
    print("Error en informacion de playlists")