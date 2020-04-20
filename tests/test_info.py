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


data = manager.check_song_info('1');

if data['title'] is None or data['duration'] is None or data['stream_url'] is None or data['album'] is None or \
        data['genre'] is None or data['avg_valoration'] < 0.0 or data['count_valoration'] < 0 or (
        data['user_valoration'] is not None and data['user_valoration'] < 0):
    print("Error en informacion de canciones")

data = manager.check_album_info('1');
if data['name'] is None or data['songs'] is None or data['artist'] is None or data['podcast'] is None:
    print("Error en informacion de album")

data = manager.check_artist_info('1')
if data['name'] is None or data['albums'] is None:
    print("Error en informacion de artistas")

data = manager.check_playlists_info('1');
if data['name'] is None:
    print("Error en informacion de playlists")
