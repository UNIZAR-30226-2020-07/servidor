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

for data in manager.getSongs():
    if data['title'] is None or \
            data['duration'] is None or \
            data['stream_url'] is None or \
            data['album'] is None or \
            data['genre'] is None or \
            data['count_valoration'] < 0 or \
            (data['avg_valoration'] is None and data['count_valoration'] != 0) or \
            (data['user_valoration'] is not None and not 1 <= data['user_valoration'] <= 5):
        print("Error en informacion de canciones")

for data in manager.getAlbums():
    if data['name'] is None or data['songs'] is None or data['artist'] is None or data['podcast'] is None:
        print("Error en informacion de album")

for data in manager.getArtists():
    if data['name'] is None or data['albums'] is None:
        print("Error en informacion de artistas")

for data in manager.getAllPlaylist():
    if data['name'] is None:
        print("Error en informacion de playlists")
