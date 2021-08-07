import time
import os
import shutil
import subprocess

import spotipy
from spotipy import util
from pynput.keyboard import Key, Controller

def closeSpotify():
    if os.name == 'nt':
        # windows
        os.system("taskkill /f /im spotify.exe")
    else:
        # most everything else
        os.system('killall -9 spotify')

def openSpotify(path):
    if not path:
        path = shutil.which('spotify')

    subprocess.Popen([path], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def playSpotify():
    keyboard = Controller()
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)

def previousWindow():
    keyboard = Controller()
    keyboard.press(Key.alt_l)
    keyboard.press(Key.tab)
    keyboard.release(Key.alt_l)
    keyboard.release(Key.tab)

def restartSpotify(path):
    closeSpotify()
    openSpotify(path)
    time.sleep(5)
    playSpotify()
    previousWindow()

def setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI):
    token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI)
    return spotipy.Spotify(auth=token)

def main(username, scope, clientID, clientSecret, redirectURI, path):
    spotify = setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI)

    restartSpotify(path)

    while True:

        try:
            current_track = spotify.current_user_playing_track()
        except Exception:
            print('token expired')
            spotify = setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI)
            current_track = spotify.current_user_playing_track()

        try:
            if current_track['currently_playing_type'] == 'ad':
                restartSpotify(path)
                print('Ad skipped')
        except TypeError:
            pass

        time.sleep(1)

if __name__ == '__main__':

    PATH = ""
    spotifyUsername = ""
    spotifyClientID = ""
    spotifyClientSecret = ""
    spotifyAccessScope = "user-read-currently-playing"
    spotifyRedirectURI = "http://localhost:8080/"

    main(spotifyUsername, spotifyAccessScope, spotifyClientID, spotifyClientSecret, spotifyRedirectURI, PATH)

