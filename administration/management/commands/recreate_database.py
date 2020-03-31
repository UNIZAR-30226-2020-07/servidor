"""
Command to automatize the recreation of the sqlite database
1) Deletes the sqlite file
2) Deletes all the migrations
3) Runs makemigrations
4) Runs migrate
5) Creates some default objects in the database (users, songs, etc)

Just call it from the command line: $python manage.py recreate_database
"""
from random import sample, choice, randint

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
    createArtists()
    createAlbums(25)
    createPodcasts(25)
    createSongs(50)
    createEpisodes(50)
    createUsers()
    createPlaylists(10)
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


def createArtists():
    for artist_param in ['Marie', 'Aelita', 'Miku', 'Pop Singer', 'DJ Pon-3']:
        artist = Artist(
            name=artist_param,
        )
        artist.save()


def createAlbums(N):
    for album_param in range(N):
        album = Album(
            name=getRandomName(),
            artist=getRandomObject(Artist),
        )
        album.save()
        print('Created album:', album)


def createPodcasts(N):
    for podcast_param in range(N):
        podcast = Album(
            name=getRandomName(),
            artist=getRandomObject(Artist),
            podcast=True,
        )
        podcast.save()
        print('Created podcast:', podcast)


def createSongs(N):
    for song_param in range(N):
        song = Song(
            title=getRandomName(),
            duration=randint(10, 60 * 5),
            stream_url="https://docs.google.com/uc?id=1MMJ1YWAxcs-7pVszRCZLGn9-SFReXqsD",
            # stream_url=f"debug:{artist_param}/{album_param}/{song_param}",
            album=getRandomObject(Album, podcast=False),
            genre=choice(Genre.values),
        )
        song.save()
        print('Created song:', song)


def createEpisodes(N):
    for episode_param in range(N):
        episode = Song(
            title=getRandomName(),
            duration=randint(60 * 5, 60 * 10),
            stream_url="https://docs.google.com/uc?id=1MMJ1YWAxcs-7pVszRCZLGn9-SFReXqsD",
            # stream_url=f"debug:{artist_param}/{album_param}/{song_param}",
            album=getRandomObject(Album, podcast=True),
            genre=choice(Genre.values),
            episode=True
        )
        episode.save()
        print('Created episode:', episode)


def createUsers():
    """
    creates the database with default users
    """
    User = get_user_model()

    # create superuser
    superuser = User.objects.create_superuser(username='admin', email='admin@admin.admin', password='admin')
    print(f'Created superuser {superuser}')

    # create normal users
    for user_params in ['user', 'user2', 'user3']:
        friends = list(User.objects.all())  # to avoid being friends with yourself
        user = User.objects.create_user(username=user_params, email=f'{user_params}@{user_params}.{user_params}', password=user_params)
        user.friends.set(friends)
        user.pause_song = getRandomObject(Song)
        user.pause_second = randint(1, user.pause_song.duration)
        user.albums.set(getRandomObject(Album, 5))
        print(f'Created normal user {user}')


def createPlaylists(N):
    for playlist_param in range(N):
        playlist = Playlist(
            name=getRandomName(),
            user=getRandomObject(get_user_model())
        )
        playlist.save()
        playlist.songs.set(getRandomObject(Song, 5))
        print(f"Created playlist {playlist}")


################## utils ###############
def getRandomObject(Class, k=1, **kwargs):
    items = Class.objects.filter(**kwargs).all()
    return choice(items) if k == 1 else sample(list(items), k)


def getRandomName():
    return choice([
        "The",
        "One",
        "A very",
    ]) + " " + choice([
        "different",
        "used",
        "important",
        "large",
        "available",
        "popular",
        "basic",
        "known",
        "difficult",
        "united",
    ]) + " " + choice([
        "people",
        "history",
        "way",
        "art",
        "world",
        "information",
        "map",
        "two",
        "family",
        "government",
    ])
