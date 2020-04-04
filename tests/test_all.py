import sys

if not '--no-friends' in sys.argv:
    print("Running friends test ...")

    # noinspection PyUnresolvedReferences
    import tests.test_friends

    print("Test ended.")

if not '--no-playlists' in sys.argv:
    print("Running playlist test...")

    # noinspection PyUnresolvedReferences
    import tests.test_playlists

    print("Test ended.")

if not '--no-lastUsersInfo' in sys.argv:
    print("Running user lasts listened song and second test...")

    # noinspection PyUnresolvedReferences
    # import tests.????

    print("Test ended.")
