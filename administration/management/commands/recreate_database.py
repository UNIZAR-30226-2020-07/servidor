from django.core.management import call_command
from django.core.management.base import BaseCommand

from songs.models import Song, Artist, Album, Genre


class Command(BaseCommand):
    def handle(self, **options):
        run()


###################################################################################################


def run():
    """
    What will run
    """
    deleteDatabase()
    populateUsers()
    populateSongs()


def deleteDatabase():
    """
    Deletes the database
    """
    import os
    import glob

    # delete database file (may not exists, glob will return nothing)
    print('Deleting db.sqlite3 file...')
    for file in glob.glob("db.sqlite3"):
        os.remove(file)
        print('Deleted', file)
    print('...done')

    # delete migrations files available
    print('Deleting migrations files...')
    for folder in glob.glob("*/migrations/"):
        for file in os.listdir(folder):
            if not file == '__init__.py' and (file.endswith('.py') or file.endswith('.pyc')):
                os.remove(folder + file)
                print('Deleted', folder + file)
    print('...done')

    # make migrations
    print('Call makemigrations...')
    call_command('makemigrations')
    print('...done')

    # migrate
    print('Call migrate...')
    call_command('migrate')
    print('...done')


def populateUsers():
    """
    Populates the database with a default superuser
    """
    from django.contrib.auth import get_user_model

    # create superuser
    print('Create superuser...')
    User = get_user_model()
    User.objects.create_superuser(username='admin', email='admin@admin.admin', password='admin')
    print('...done')

    # create normal user
    print('Create normal user...')
    User = get_user_model()
    User.objects.create_user(username='user', email='user@user.user', password='user')
    print('...done')


def populateSongs():
    """
    Populates the database with fake data
    """
    print('Creating songs...')
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
                    stream_url="debug:{}/{}/{}".format(artist_param, album_param, song_param),
                    album=album,
                    genre=Genre.values[i],
                )
                song.save()
                i = (i + 1) % len(Genre.values)
                print('Created song:', song)
    print('done')
