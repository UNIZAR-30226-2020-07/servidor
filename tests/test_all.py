import sys


if len(sys.argv) == 1:
    print("Run all the tests:")

    print("Running friends test ...")
    from tests import test_friends
    print("Test ended.")

    print("Running playlist test...")
    from tests import test_playlists
    print("Test ended.")


if '--friends' in sys.argv:
    print("Running friends test ...")
    from tests import test_friends
    print("Test ended.")


if '--playlists' in sys.argv:
    print("Running playlist test...")
    from tests import test_playlists
    print("Test ended.")
