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

# Existing elements
if manager.searchSong('the') is None:
    print("Error, no songs with that title")

if manager.searchArtists('jojo') is None:
    print("Error, no artist with that name")

if manager.searchAlbum('jojo') is None:
    print("Error, no album with that name")

if manager.searchPlaylists('world') is None:
    print("Error, no playlist with that name")

if manager.searchEpisode('world') is None:
    print("Error, no episodes on BBDD")

if manager.searchPodcast('world') is None:
    print("Error, no podcast on BBDD")

# search user by username
if manager.searchUser('user') is None:
    print("Error, no username with that username")

# search user by mail
if manager.searchUser('user@user.user') is None:
    print("Error, no user with that email")

# NOT Existing elements
if manager.searchSong('hfwebonjnvwmpok1sp') is not None:
    print("Error, existing songs with that title")

if manager.searchArtists('hfwebonjnvwmpok1sp') is not None:
    print("Error, existing artist with that name")

if manager.searchAlbum('hfwebonjnvwmpok1sp') is not None:
    print("Error, existing album with that name")

if manager.searchPlaylists('hfwebonjnvwmpok1sp') is not None:
    print("Error, existing playlist with that name")

# search user by username
if manager.searchUser('uuuuuuser') is not None:
    print("Error, existing user with that username")

# search user by mail
if manager.searchUser('uuuuuuuuser@user.user') is not None:
    print("Error, existing user with that email")
