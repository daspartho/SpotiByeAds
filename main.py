import sys, os, time, shutil, subprocess, json, urllib
from getpass import getpass

from utils import get_password, store_credentials, load_credentials

try:
    import spotipy
    import urllib3
    from pynput.keyboard import Key, Controller
except ImportError:
    print("DEPENDENCIES NOT INSTALLED!"
          "\nPlease install the depenencies by running:"
          "\n\t`python -m pip install -r requirements.txt`")
    sys.exit(1)

#Vars
keyboard = Controller()

def closeSpotify():
    if os.name == "nt":  # windows
        os.system("taskkill /f /im spotify.exe")
    elif sys.platform == "darwin":  # Mac OS
        # Not exactly sure of the process name, so used regex.
        os.system("killall -9 -r [Ss]potify.*")
    else:  # almost everything else
        os.system("killall -9 spotify")

def openSpotify(path):
    subprocess.Popen([path], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def playPause():
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)

def nextTrack():
    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)
    
def previousWindow():
    keyboard.press(Key.alt_l)
    keyboard.press(Key.tab)
    keyboard.release(Key.alt_l)
    keyboard.release(Key.tab)
    
def restartSpotify(path):
    closeSpotify()
    openSpotify(path)
    time.sleep(5)
    nextTrack()
    previousWindow()

def setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI):
    token = spotipy.util.prompt_for_user_token(username, scope, clientID,
                                               clientSecret, redirectURI)
    return spotipy.Spotify(auth=token)

def main(username, scope, clientID, clientSecret, redirectURI, path):    
    try:
        spotify = setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI)
    except (OSError, urllib3.exceptions.HTTPError) as e:
        print(f"\nSomething went wrong: {e}\n")
        print("Please connect to the internet and run the program again.")
        return

    print("\nAwesome, that's all I needed. I'm watching for ads now <.<")
    restartSpotify(path)

    current_track = None
    last_track = ""
    while True:
        try:
            try:
                try:
                    current_track = spotify.current_user_playing_track()
                except spotipy.SpotifyException:
                    print('Token expired')
                    spotify = setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI)
                    current_track = spotify.current_user_playing_track()

            except (OSError, urllib3.exceptions.HTTPError) as e:
                print(f"\nSomething went wrong: {e}\n")
                print("Waiting for network connection...")
                while True:
                    time.sleep(5)
                    try:  # Test network
                        urllib.request.urlopen("https://spotify.com", timeout=5)
                    except OSError:
                        pass
                    else:
                        print("Connection restored!")
                        break

            if current_track:  # Can either be `None` or JSON data `dict`.
                if current_track['currently_playing_type'] == 'ad':
                    restartSpotify(path)
                    print('Ad skipped')
                    continue  # get new track info

                if current_track['item']['name'] != last_track:  # Next track
                    # Current track's remaining duration
                    wait = current_track["item"]['duration_ms'] - current_track['progress_ms']

                    try:
                        # Reduces API requests to prevent getting rate limited from spotify API
                        time.sleep(wait/1000 - 8)  # until **almost** the end of the current track
                        last_track = current_track['item']['name']
                    except KeyboardInterrupt:
                        print("\n1. Skip track.\n"
                              "2. Want to change playlist/track or pause playback.\n"
                              "3. Exit this program (enter anything else).\n"
                             )
                        choice = input("Choose an option (1/2/?): ")
                        last_track = ""  # In case the track remains the same.
                        if choice == '1':
                            nextTrack()
                            playPause()  # To prevent ads from playing during the delay below.
                            # A short delay is required for the Spotify API to register the
                            # track change, so as to get the correct track info on the next request.
                            time.sleep(0.6)  # 600ms seems to be the shortest possible
                            playPause()
                        elif choice == '2':
                            input("You can go ahead to change the playlist/track"
                                  " or pause the playback on the Spotify app.\n"
                                  "Press ENTER after changing the playlist/track"
                                  " or resuming playback...")
                            print("Resuming my business of skipping ads ;)")
                        else:
                            sys.exit(0)
                        continue  # Skip the one-second sleep

            time.sleep(1)
        except KeyboardInterrupt:
            if input("\nExit? (Y/n) ").lower() != 'n':
                break
            print("Resuming my business of skipping ads ;)")


if __name__ == '__main__':
    # These are kinda constants

    # Popen expects a path-like object, `None` results in an error.
    PATH = (shutil.which("spotify")  # For any system with spotify on $PATH
            or ("{HOMEDRIVE}{HOMEPATH}\AppData\Roaming\Spotify\Spotify.exe"
                .format_map(os.environ) if os.name == "nt"  # Windows
                else "/Applications/Spotify.app" if sys.platform == "darwin"  # MacOS
                else ""  # Custom path if installation is different
               )
           )

    SPOTIFY_ACCESS_SCOPE = "user-read-currently-playing"
    SPOTIFY_REDIRECT_URI = "http://localhost:8080/"

    loaded = False
    if os.access("credentials.bin", os.R_OK):
        load = input("Found previously saved credentials. Want to use them again? (y/n) "
                    ).lower()

        if load == "y":
            tries = 0
            while tries < 3:
                pwd = getpass("Enter your password: ")
                if len(pwd)>=8 and pwd.isascii() and pwd.isprintable() and ' ' not in pwd:
                    try:
                        username, client_id, client_secret = load_credentials(pwd)
                        loaded = True
                        break
                    except TypeError:
                        print("Incorrect password!")
                    except ValueError:
                        print("Can't load stored credentials, must be corrupted!")
                        try:
                            os.remove("credentials.bin")
                        except PermissionError:
                            print("Could not delete 'credentials.bin', "
                                  "please manually delete it.")
                        loaded = False
                        break
                else:
                    print("Invalid password!")
                tries += 1
            else:
                print("3 Wrong Attempts! Exiting...")
                sys.exit(0)
        elif load == "n":
            print("User didn't want to load from save.")
        else:
            print("Unrecognized Input. Exiting...")
            sys.exit(0)

    if not loaded:
        if os.access("credentials.json", os.R_OK):
            with open("credentials.json", "r") as creds_json:
                 username, client_id, client_secret = json.load(creds_json).values()

            try:
                os.remove("credentials.json")
            except PermissionError:
                print("Could not delete 'credentials.json', please manually delete it.")

            save = "y"
            print("\nNOTICE: Old credentials store found!\n"
                  "This script has been updated to now encrypt stored credentials.\n"
                  "Due to this, you now have to enter a password when loading stored "
                  "credentials henceforth.\n"
                  "Please your new password below to encrypt your existing "
                  "credentials.\n")
        else:
            username = input("What's your Spotify username? ")
            client_id = input("Great, now what's the ClientID you're using? ")
            client_secret = input("Beautiful, now how about the Client Secret? ")

            save = input("Awesome, now would you like to save your credentials"
                         " for future sessions? (y/N) "
                        ).lower()
        
        if save == "y":
            password = get_password()
            if not password:
                print("Too many invalid attempts! Credentials not saved.\nExiting...")
                sys.exit(0)

            try:
                store_credentials(password, username, client_id, client_secret)
                print("Credentials saved.")
            except PermissionError:
                print("Credentials could not be stored due to lack of permission\n"
                      "The script will continue anyways...")
        elif save == "n":
            print("Not saving settings.")
        else:
            print("Didn't recognize input, defaulted to not saving.")

    main(username, SPOTIFY_ACCESS_SCOPE, client_id, client_secret, SPOTIFY_REDIRECT_URI, PATH)

