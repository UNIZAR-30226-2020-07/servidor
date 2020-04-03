import sys


if len(sys.argv) == 1:
    print("Run all the tests:")

    print("Running friends test ...")
    print("Test ended.")

    print("Running playlist test...")
    print("Test ended.")

    print("Running user lasts listened song and second test...")
    print("Test ended.")


if '--friends' in sys.argv:
    print("Running friends test ...")
    print("Test ended.")


if '--playlists' in sys.argv:
    print("Running playlist test...")
    print("Test ended.")

if '--lastUsersInfo' in sys.argv:
    print("Running user lasts listened song and second test...")
    print("Test ended.")
