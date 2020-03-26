"""
Command to automatize the recreation of the sqlite database
1) Deletes the sqlite file
2) Deletes all the migrations
3) Runs makemigrations
4) Runs migrate
5) Creates some default objects in the database (users, songs, etc)

Just call it from the command line: $python manage.py recreate_database
"""
from random import sample

from django.core.management import call_command
from django.core.management.base import BaseCommand

from songs.models import Song, Artist, Album, Genre
# Registers the command in Django
from users.models import Playlist


class Command(BaseCommand):
    def handle(self, **options):
        run()


###################################################################################################
import os
import glob
from django.contrib.auth import get_user_model


def run():
    """
    What will run
    """
    print('Deleting db.sqlite3 file...')
    deleteDatabaseFile()
    print('...done')

    print('Deleting migrations files...')
    deleteMigrations()
    print('...done')

    print('Call makemigrations...')
    call_command('makemigrations')
    print('...done')

    print('Call migrate...')
    call_command('migrate')
    print('...done')

    print('Populating database...')
    populateSongs()
    populateUsers()
    print('...done')


def deleteDatabaseFile():
    """
    Deletes the sqlite database file
    """
    # (may not exists, in which case glob will return nothing)
    for file in glob.glob("db.sqlite3"):
        os.remove(file)
        print('Deleted', file)


def deleteMigrations():
    """
    delete existing migrations files
    """
    for folder in glob.glob("*/migrations/"):
        for file in os.listdir(folder):
            if not file == '__init__.py' and (file.endswith('.py') or file.endswith('.pyc')):
                os.remove(folder + file)
                print('Deleted', folder + file)


def populateSongs():
    """
    Populates the database with some songs/albums/artists
    """
    i = 0

    # populate data
    for artist_param in ['Bob', 'Charly', 'DJ', 'Stanley', 'Luna']:
        # create the artist
        artist = Artist(
            name=artist_param,
        )
        artist.save()
        print('Created artist:', artist)
        for album_param in range(5):
            # create an album for that artist
            album = Album(
                name="My awesome album #" + str(album_param + 1),
                artist=artist,
            )
            album.save()
            print('Created album:', album)
            for song_param in range(5):
                # create a song in that album
                song = Song(
                    title="Happy tune #" + str(song_param + 1),
                    duration=10 * (song_param + 1),
                    stream_url="https://docs.google.com/uc?id=1MMJ1YWAxcs-7pVszRCZLGn9-SFReXqsD",
                    # stream_url="debug:{}/{}/{}".format(artist_param, album_param, song_param),
                    album=album,
                    genre=Genre.values[i],
                )
                song.save()
                i = (i + 1) % len(Genre.values)
                print('Created song:', song)


def populateUsers():
    """
    Populates the database with default users
    """
    User = get_user_model()

    # create superuser
    User.objects.create_superuser(username='admin', email='admin@admin.admin', password='admin')
    print('Created superuser')

    # create normal users
    for user_params in ['user', 'user2', 'user3']:
        User.objects.create_user(username=user_params, email='{0}@{0}.{0}'.format(user_params), password=user_params)
        print('Created normal user {}'.format(user_params))

    # create playlists for those users
    songs = Song.objects.all()
    for user in User.objects.all():
        for playlist_param in range(5):
            playlist = Playlist(
                name="{}'s playlist #{}".format(user, playlist_param),
                user=user
            )
            playlist.save()
            playlist.songs.set(sample(list(songs), 5))
            print("Created playlist {}".format(playlist))
