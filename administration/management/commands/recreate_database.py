"""
Command to automatize the recreation of the sqlite database
1) Deletes the sqlite file
2) Deletes all the migrations
3) Runs makemigrations
4) Runs migrate
5) Creates some default objects in the database (users, songs, etc)

Just call it from the command line: $python manage.py recreate_database
"""
import random
from random import sample, choice, randint

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand

from songs.models import Song, Artist, Album, Genre

User = get_user_model()
# Registers the command in Django
from users.models import Playlist, Valoration


class Command(BaseCommand):
    def handle(self, **options):
        run(options['heroku'])

    def add_arguments(self, parser):
        parser.add_argument('--heroku', action='store_true', help='To run in Heroku mode')


###################################################################################################
import os
import glob


def run(heroku):
    """
    What will run
    """
    if heroku:
        for model in [Song, Album, Artist, User, Playlist, Valoration]:
            print(f'Deleting all objects from {model.__name__}...')
            model.objects.all().delete()
            print('...done')
    else:
        print('Deleting db.sqlite3 file...')
        deleteDatabaseFile()
        print('...done')

        # don't delete, heroku needs them, new migrations will append existing ones
        # print('Deleting migrations files...')
        # deleteMigrations()
        # print('...done')

    print('Call makemigrations...')
    call_command('makemigrations')
    print('...done')

    print('Call migrate...')
    call_command('migrate')
    print('...done')

    print('Populating database...')
    createSongsAlbumsAndArtists()
    createUsers()
    createPlaylists(10)
    createValorations()
    print('...done')

    # site
    one = Site.objects.all()[0]
    if one.name == 'example.com':
        one.domain = 'localhost:8000'
        one.name = 'MusicApp'
        one.save()
        Site(domain="ps-20-server-django-app.herokuapp.com", name="MusicApp").save()


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


def createSongsAlbumsAndArtists():
    """
    Foreach song,album,artist in drive, create if not exists
    """
    for song_params, album_params, artist_params in getDriveSongs():
        artist, created = Artist.objects.get_or_create(**artist_params)
        if created: print('Created artist:', artist)
        album, created = Album.objects.get_or_create(**album_params, artist=artist)
        if created: print('Created', 'podcast:' if album.podcast else 'album:', album)
        song, created = Song.objects.get_or_create(**song_params, album=album)
        if created: print('Created', 'episode:' if song.episode else 'song:', song)


def createUsers():
    """
    creates an admin and three normal users with random data
    """

    # create superuser
    superuser = User.objects.create_superuser(username='admin', email='instantmusicapp+admin@gmail.com', password='admin')
    print(f'Created superuser {superuser}')

    # create normal users
    for user_params in ['user', 'user2', 'user3']:
        friends = list(User.objects.all())  # to avoid being friends with yourself
        user = User.objects.create_user(username=user_params, email=f'instantmusicapp+{user_params}@gmail.com', password=user_params)
        user.friends.set(friends)
        user.pause_song = getRandomObject(Song)
        user.pause_second = randint(1, user.pause_song.duration - 1)
        user.albums.set(getRandomObject(Album, randint(1, 5)))
        print('Created normal user:', user)


def createPlaylists(N):
    """
    creates N playlists with random data
    """
    for playlist_param in range(N):
        playlist = Playlist(
            name=getRandomName(),
            user=getRandomObject(get_user_model())
        )
        playlist.save()
        playlist.songs.set(getRandomObject(Song, randint(1, 10)))
        print("Created playlist:", playlist)


def createValorations():
    """
    creates random valorations
    """
    for user in get_user_model().objects.all():
        for song in Song.objects.all():
            if random.random() < 0.6:
                valoration = Valoration.objects.create(user=user, song=song, valoration=randint(1, 5))
                print("Added valoration:", valoration)


################## randoms ###############
def getRandomObject(Class, k=None, **kwargs):
    """
    Returns a random object (no k), or a random set of k elements, can be filtered
    """
    items = Class.objects.filter(**kwargs).all()
    return choice(items) if k is None else sample(list(items), k)


def getRandomName():
    """
    Returns a random name
    """
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


################ Drive ##################

def getDriveSongs():
    """
    Returns all the songs (and episodes) in drive, the album where they belong and the artist of the album
    [(song, album, artist),...]
    """
    elements = []

    # convert songs into data
    for name, id, m, s in songs_drive:
        song_name, artist_name = [e.strip() for e in name.replace('[Vlog No Copyright Music]', '').split(" - ")]
        elements.append((False, song_name, f"No Copyright Music of {artist_name}", artist_name, id, m, s))

    # convert episodes into data
    for name, id, m, s in episodes_drive:
        song_name, artist_name = [e.strip() for e in name.split(" - ")]
        elements.append((True, song_name, f"Podcast of {artist_name}", artist_name, id, m, s))

    # return as parameters
    for episode, song_name, album_name, artist_name, id, m, s in elements:
        yield ({
                   'title': song_name,
                   'stream_url': 'https://docs.google.com/uc?id=' + id,
                   'duration': m * 60 + s,
                   'genre': choice(Genre.values),
                   'episode': episode,
               }, {
                   'name': album_name,
                   'podcast': episode,
               }, {
                   'name': artist_name,
               },)


###########
episodes_drive = [
    ("Kira's theme - JoJos", "1gCnzSfquYKTiTPc1zrVvAW8C8BnpXlSy", 3, 0),
    ("Il vento d'oro - JoJos", "1gQfiAr8Y8pro8yTYLOCFFo42dgOPv99P", 4, 52),
    ("Segundo Opening - JoJos", "1U3JkCO6YlUpKejfglmX1mdpQrf0jMl0P", 1, 32),
    ("Fulluragirimono no requiemby daisuke hasegawa - JoJos", "1-xn-yT6O9fum8pUq5vag4J_ElLmrwtfI", 3, 59),
    ("You say run - My hero academia", "1hcK8bJIyvHlXgs83S8pq-GfyMpQfTibK", 3, 52),
    ("The best day ever - SpongeBob", "1JJUto_oiiSfqIDKNfKMVIYzrzUQe0Rv6", 3, 2),
]
songs_drive = [
    ("Pixel Pig - Di Young [Vlog No Copyright Music]", "1qUDPUvQxX8am5OMk99Clfn3dAIjUFD6R", 2, 53),
    ("Castle in the sky - Rofeu [Vlog No Copyright Music]", "1PbDXj4OK6adtZSey3EsCRBqWGzEwylKX", 2, 9),
    ("We Are Here - Declan DP [Vlog No Copyright Music]", "1DArTjmAm9NgwmsvxZipF1FESovOXsNt0", 2, 55),
    ("Dreamland - Jonas Schmidt [Vlog No Copyright Music]", "1O0OUeky9pJwSisGMr5szHoEl6390Rm-J", 2, 42),
    ("Coming Home - LiQWYD & Dayfox [Vlog No Copyright Music]", "1w1FR9byey-aKcpXnzyEFtNoOvO02BIZF", 3, 13),
    ("Dolce Vita - Peyruis [Vlog No Copyright Music]", "1zx1AahkQVWIcypK-9JOcx6HyqIhgINHy", 3, 41),
    ("First Class - Peyruis [Vlog No Copyright Music]", "1b1EgXDeKgu-fCUS00OUtn-zPm2_9FMBI", 4, 5),
    ("Still Awake  - Ghostrifter Official [Vlog No Copyright Music]", "1zaJaulBa0XDD-xFtg1-a5ztgb0ditpYf", 2, 48),
    ("Call Me - LiQWYD [Vlog No Copyright Music]", "1QXzEdB3VVNLQZTHMg2hVkuy6SQMi3s8S", 2, 39),
    ("River - MusicbyAden [Vlog No Copyright Music]", "1_weAqhxWVuauw835eDUu33A4RmnSlM63", 2, 14),
    ("I Miss You - Løv li [Vlog No Copyright Music]", "1aX-wgjqTWLjuL5gecKahJ1WXdmlVvkyc", 3, 29),
    ("after the rain - Rexlambo [Vlog No Copyright Music]", "1i9JOGCE85pYa03odefkLRzpPfm1FVYP2", 3, 31),
    ("Dreams - Firefl!es [Vlog No Copyright Music]", "1aCInZ_naYGJZur9Odq-SMmByr4srgTQh", 2, 44),
    ("Merry Bay - Ghostrifter Official [Vlog No Copyright Music]", "1Y5VFFRLlsbuFcE-U4_S6vC13CH58Xgnq", 2, 14),
    ("Lioness (Instrumental) - DayFox [Vlog No Copyright Music]", "1hySIoACrkdGGkJgu_KCuc7ogMrCQ1YjZ", 3, 8),
    ("Dreambye - BraveLion [Vlog No Copyright Music]", "1gv7DkQ-s57tJIvf5cGNp23CP5KFcF4fM", 2, 54),
    ("Let You Go (feat. Tara Flanagan) (Instrumental) - Spectrum [Vlog No Copyright Music]", "1T_b5l9yvEceMOvPUEmFC-1hYyEEr9Ewi", 3, 42),
    ("Take You There (feat. Ria Choony) - Spectrum  [Vlog No Copyright Music]", "1bWlW5bPaNEccp7GI85C_mmT4iB0KA7WR", 2, 56),
    ("Lovely - Amine Maxwell  [Vlog No Copyright Music]", "1S8qUbAlNUSHrW5NlnfdOSHduZeuTM5es", 2, 27),
    ("The Things That Keep Us Here - Scott Buckley [Vlog No Copyright Music]", "17QW7IGWRGcTUL2eCZhYo-ZKbK2wzRCLb", 4, 26),
    ("Bad Love (Vocal Edit) - Niwel  [Vlog No Copyright Music]", "1jj4gfH9INwOuktlaA5zQFNuXD2Pg8O4q", 3, 34),
    ("Birds - Scandinavianz  [Vlog No Copyright Music]", "1nwxA6mAVsO-oHtGtVpQmBmkSUyC_QcZI", 1, 56),
    ("Through My Eyes (Instrumental) - Mike Leite [Vlog No Copyright Music]", "1wmn9i29yJWJBhsYUnrZMiyodEhYtaoh6", 2, 53),
    ("I'm Just Good - Johny Grimes [Vlog No Copyright Music]", "1ME51ObmI63ejW3cYQZm_U6BBrOHTa_y4", 2, 24),
    ("I Saw A Ghost Last Night - Leonell Cassio [Vlog No Copyright Music]", "1KIxXkwDFQCG4FNy5807vhe98yQkIENbD", 2, 32),
    ("Mexicana En Lelé - Le Gang [Vlog No Copyright Music]", "1MPrt6uMBL5CFSB9Ui_t39fOGU7gDiwI2", 2, 48),
    ("Feather - Waywell [Vlog No Copyright Music]", "1eqIe2qK00EjAN0K7zDujbpoonnFjJ_w1", 7, 14),
    ("No Prayers - Pokki Dj [Vlog No Copyright Music]", "14svrQtlWBzFXb-qCySRBJtbGnlcjDp5N", 3, 21),
    ("Fog - DIZARO [Vlog No Copyright Music]", "1R3dbQn7b9-bdqsPa_OmP2mAb_lQEOsEu", 2, 40),
    ("Spiral - KV  [Vlog No Copyright Music]", "1S3MVqifrsRZE1n-X3voC5EcMOHqt_L-8", 3, 1),
    ("Easily - Johny Grimes [Vlog No Copyright Music]", "1X_oRnNjT_1uUEBN8PsrvbgN8gbo3UV5c", 2, 23),
    ("Funky Souls - Amarià [Vlog No Copyright Music]", "1D6i3TIyVxV-9xGuhPOy7z2ezbZ0AZOnc", 2, 42),
    ("City Life - Artificial.Music  [Vlog No Copyright Music]", "1SBOKA7tJ1yNy9VypfcF-wNKp4j6oycnA", 3, 42),
    ("Finally - Loxbeats  [Vlog No Copyright Music]", "1ucQ3x3KW5TmuAthjGQc61bI97iARqxLd", 2, 9),
    ("Be The One (feat. Anaïk) - Vendredi  [Vlog No Copyright Music]", "1TNGg9rdWFhgCT4kpmRuo6L-S_qh98txi", 4, 7),
    ("Chill - sakura Hz  [Vlog No Copyright Music]", "1cgjoPaeg24nJFKJXUaF7qVGy_3827ZgZ", 3, 52),
    ("Keddie - Loxbeats  [Vlog No Copyright Music]", "1ghqOkl7qf2x11ESduqwpca4NI4u-Kt9J", 2, 18),
    ("Help You Out (ft. Jonathon Robins) - Leonell Cassio  [Vlog No Copyright Music]", "1GEgIakWvtog7chIoHiBFyp2B4lubvi7M", 3, 2),
    ("Good morning - Amine Maxwell  [Vlog No Copyright Music]", "1k6RTQojlCV8QAlKGp_4X1ZgfjYvy2jYe", 2, 34),
    ("Tropical Traveller - Del. [Vlog No Copyright Music]", "1t74rJir3IR33lPPJAGFe58FZhv7LMe5Q", 3, 41),
    ("I Don't Need U 2 Say Anything - Le Gang  [Vlog No Copyright Music]", "1Th9S21Sun1r2RRrCoALC83DC24ZOPkoL", 2, 23),
    ("Mrs. Zazzara - Loxbeats  [Vlog No Copyright Music]", "1mtw43ErrnjxT7g9Fyk5sVabL69EK8JKB", 1, 48),
    ("MOSAIC - Lahar  [Vlog No Copyright Music]", "1Ut5jZq0rWqYPsW5tbgeXbML-VWqqyyev", 3, 17),
    ("Sunset tree - Amine Maxwell  [Vlog No Copyright Music]", "10v4dMcvd_GCVUBYD4zy_gTpqMTI5O6Cw", 2, 42),
    ("Hot Coffee - Ghostrifter Official [Vlog No Copyright Music]", "1GyByrg3TwkyACgX-MPQNL1dS8T5I-Fny", 2, 19),
    ("With You - Declan DP  [Vlog No Copyright Music]", "1YWO0I9irnctojTheskcJkReSxNR2itvk", 3, 48),
    ("All Night - Ikson  [Vlog No Copyright Music]", "1TR-fZhfTA8npBVZ6Vn6DSh9jkvWHGzfX", 3, 5),
    ("Atlantis - Scandinavianz  [Vlog No Copyright Music]", "1nvRBnEAQHf8bCg8esVBDMp908q8G2tiO", 2, 29),
    ("Fantasy - Declan DP  [Vlog No Copyright Music]", "11zk7JDE-UmnkGMeAf1A0FGZRhszvWn1l", 3, 14),
    ("Polaroid - extenz  [Vlog No Copyright Music]", "1YrYFnIO-sN1boHB7c3-9X983cxgaScqE", 3, 22),
    ("Snowfall - Scott Buckley  [Vlog No Copyright Music]", "1-461_ckUUgjYvxS7noVYUJRhPJHfJc3y", 4, 8),
    ("Night Out - LiQWYD  [Vlog No Copyright Music]", "1Juwrgaahl0HHPr_OEJlO5YAbO130_yuQ", 3, 12),
]
