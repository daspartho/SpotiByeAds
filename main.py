import json
import os
import shutil
import subprocess
import sys
import threading
import time
import urllib.request

try:
    import spotipy
    import urllib3
    from pynput import keyboard
    from pynput.keyboard import Key, Controller
except ImportError:
    print("DEPENDENCIES NOT INSTALLED!"
          "\nPlease install the dependencies by running:"
          "\n\t`python -m pip install -r requirements.txt`")
    sys.exit(1)

# Vars
keyboardCon = Controller()
pauseEvent = threading.Event()
pauseEvent.set()
nextTrackEvent = threading.Event()
exitEvent = threading.Event()


def readConfig(config_path: str) -> dict:
    if os.path.isfile(config_path):
        with open(config_path, "r") as conf_json:
            settings = json.load(conf_json)
    else:
        print("Config not found, restore default")
        settings = {"is_hide_in_trey": False,
                    "auto_logging": False,
                    "pause_track": False,
                    "cred_path": "credentials.json",
                    "hotkeys_path": "hotkeys.json"}
        with open(config_path, 'w') as conf_json:
            conf_json.write(json.dumps(settings))
    return settings


def readHotkeys(hotkeys_path: str) -> dict:  # TODO сделать проверку горячих клавишь
    if os.path.isfile(hotkeys_path):
        with open(hotkeys_path, "r") as hot_json:
            hotkeys_tmp = json.load(hot_json)
        hotkeys = {hotkeys_tmp["next_track"]: nextTrackAct,
                   hotkeys_tmp["prev_track"]: prevTrackAct,
                   hotkeys_tmp["stop_script"]: pauseScriptAct,
                   hotkeys_tmp["exit_script"]: exitScriptAct}
    else:
        print(f"Hotkeys not found, {hotkeys_path} correct name?")
        print("Restore default")
        hotkeys = {"<ctrl>++": nextTrackAct,
                   "<ctrl>+-": prevTrackAct,
                   "<ctrl>+*": pauseScriptAct,
                   "<ctrl>+<shift>+*": exitScriptAct}
    return hotkeys


def nextTrackAct():
    nextTrackEvent.set()
    keyboardCon.tap(Key.media_next)
    keyboardCon.tap(Key.media_play_pause)  # To prevent ads from playing during the delay below.
    anti_pause = threading.Timer(0.6, keyboardCon.tap, args=(Key.media_play_pause,))  # Script may stop work ifn
    anti_pause.start()  # spamming nextTrackHotKey, her safer


def prevTrackAct():
    nextTrackEvent.set()
    keyboardCon.tap(Key.media_previous)
    keyboardCon.tap(Key.media_play_pause)
    anti_pause = threading.Timer(0.6, keyboardCon.tap, args=(Key.media_play_pause,))
    anti_pause.start()


def pauseScriptAct():
    if pauseEvent.is_set():
        pauseEvent.clear()
        nextTrackEvent.set()
        if config["pause_track"]:
            keyboardCon.tap(Key.media_play_pause)
        print('Script paused, now you can change track')
    else:
        pauseEvent.set()
        print('Script unpause')


def exitScriptAct():
    print('Exiting... bye')
    nextTrackEvent.set()
    pauseEvent.set()
    exitEvent.set()
    time.sleep(0.2)
    closeSpotify()


def closeSpotify():
    if os.name == "nt":  # windows
        os.system("taskkill /f /im spotify.exe")
    elif os.name == "posix":  # Mac OS
        # Not exactly sure of the process name, so used regex.
        os.system("killall -9 -r [Ss]potify.*")
    else:  # almost everything else
        os.system("killall -9 spotify")


def openSpotify(path):
    subprocess.Popen([path], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)


def restartSpotify(path, close_spotify: bool):
    closeSpotify()
    openSpotify(path)
    time.sleep(5)
    keyboardCon.tap(Key.media_next)
    if close_spotify:
        keyboardCon.press(Key.alt_l)
        keyboardCon.press(Key.f4)
        keyboardCon.release(Key.f4)
        keyboardCon.release(Key.alt_l)
    else:
        keyboardCon.press(Key.alt_l)
        keyboardCon.press(Key.tab)
        keyboardCon.release(Key.alt_l)
        keyboardCon.release(Key.tab)


def inputSpotifyInfo(path) -> dict:
    save_dict = {'spotify_username': input("Ok, what's your Spotify username? "),
                 'spotify_client_id': input("Great, now what's the ClientID you're using? "),
                 'spotify_client_secret': input("Beautiful, now how about the Client Secret? ")}

    save = input("Would you like to save these settings for future sessions? (Y/n)").lower()

    if save == "y":
        with open(path, "w") as creds_json:
            creds_json.write(json.dumps(save_dict))
        print("Saved.")
    elif save == "n":
        print("Not saving credentials.")
    else:
        print("Didn't recognize input, defaulted to not saving.")
    return save_dict


def setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI):
    auth_manager = spotipy.SpotifyOAuth(clientID, clientSecret, redirectURI, scope=scope, username=username)
    client = spotipy.Spotify(auth_manager=auth_manager)
    return client


if __name__ == '__main__':
    # constants
    configFile = "config.json"
    spotifyAccessScope = "user-read-currently-playing"
    spotifyRedirectURI = "http://localhost:8080/"
    PATH = (shutil.which("spotify")  # For any system with spotify on $PATH
            or ("{HOMEDRIVE}\{HOMEPATH}\AppData\Roaming\Spotify\Spotify.exe".format_map(os.environ)
                if os.name == "nt"  # Windows
                else "/Applications/Spotify.app" if os.name == "posix"  # MacOS
            else ""  # Custom path if installation is different
                )
            )
    config = readConfig(configFile)
    hotkeys_dict = readHotkeys(config["hotkeys_path"])

    if os.path.isfile(config["cred_path"]):
        if not config["auto_logging"]:
            load = input("Found previously used credentials. Want to use them again? (Y/n)").lower()
        else:
            load = "y"

        if load == "y":
            with open(config["cred_path"], 'r') as creds_json:
                creds = json.load(creds_json)
        elif load == "n":
            print("User didn't want to load from save.")
            creds = inputSpotifyInfo(config["cred_path"])
        else:
            print("Unrecognized Input.")
            sys.exit(0)
    else:
        creds = inputSpotifyInfo(config["cred_path"])

    try:
        spotify = setupSpotifyObject(creds['spotify_username'], spotifyAccessScope,
                                     creds['spotify_client_id'], creds['spotify_client_secret'],
                                     spotifyRedirectURI)
    except (OSError, urllib3.exceptions.HTTPError) as e:
        print(f"\nSomething went wrong: {e}\n")
        print("Please connect to the internet and run the program again.")
        sys.exit(1)

    restartSpotify(PATH, config["is_hide_in_trey"])

    current_track, last_track = None, ""
    print("Now, i'm watching for ads now <.<")
    with keyboard.GlobalHotKeys(hotkeys_dict):
        while not exitEvent.is_set():
            pauseEvent.wait()
            try:
                try:
                    current_track = spotify.current_user_playing_track()
                except spotipy.SpotifyException:
                    print('Token expired')
                    spotify = setupSpotifyObject(creds['spotify_username'], spotifyAccessScope,
                                                 creds['spotify_client_id'], creds['spotify_client_secret'],
                                                 spotifyRedirectURI)
                    current_track = spotify.current_user_playing_track()

            except (OSError, urllib3.exceptions.HTTPError) as e:
                print(f"\nSomething went wrong: {e}")
                print("Waiting for network connection...\n")
                while pauseEvent.is_set():
                    try:  # Test network
                        urllib.request.urlopen("https://spotify.com", timeout=5)
                    except OSError:
                        if not pauseEvent.is_set():  # fuse, maybe can be removed
                            continue
                        else:
                            time.sleep(5)
                    else:
                        print("Connection established! I'm watching for ads now <.<")
                        break
                else:
                    continue

            if current_track:  # Can either be `None` or JSON data `dict`.
                if current_track['currently_playing_type'] == 'ad':
                    restartSpotify(PATH, config["is_hide_in_trey"])
                    print('Ad skipped')
                    continue  # get new track info

                if current_track['item']['name'] != last_track:  # Next track
                    # Current track's remaining duration
                    wait_time = current_track["item"]['duration_ms'] - current_track['progress_ms']
                    nextTrackEvent.wait(wait_time / 1000 - 8)  # until **almost** the end of the current track
                    last_track = current_track['item']['name']
                    nextTrackEvent.clear()
                    if not pauseEvent.is_set():
                        last_track = ""
                        continue
            time.sleep(1)
