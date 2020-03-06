from django.core.management import call_command
from django.core.management.base import BaseCommand

from songs.models import Song, Artist, Album


class Command(BaseCommand):
    def handle(self, **options):
        run()


###################################################################################################


def run():
    """
    What will run
    """
    deleteDatabase()
    populateDatabase()


def deleteDatabase():
    """
    Deletes the database
    """
    import os
    import glob

    # delete database file (may not exists, glob will return nothing)
    for file in glob.glob("db.sqlite3"):
        os.remove(file)
        print('Deleted database file')

    # delete migrations files available
    for folder in glob.glob("*/migrations/"):
        for file in os.listdir(folder):
            if not file == '__init__.py' and file.endswith('.py'):
                os.remove(folder + file)
                print('Deleted migration file:', folder + file)

    # make migrations
    call_command('makemigrations')

    # migrate
    call_command('migrate')


def populateDatabase():
    """
    Populates the database with fake data
    """
    from django.contrib.auth import get_user_model

    # create superuser
    User = get_user_model()
    User.objects.create_superuser('user', 'user@user.user', 'user')

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
                    stream_url="debug:{}/{}/{}".format(artist_param, album_param, song_param),
                    album=album,
                )
                song.save()
                print('Created song:', song)
