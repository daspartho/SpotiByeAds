import time
import os
import configparser

import spotipy
from spotipy import util
from pynput.keyboard import Key, Controller

CONFIG_FILE = 'config.properties'
CONFIG_BASE = 'spotify'

def closeSpotify():
    os.system("taskkill /f /im spotify.exe")

def openSpotify(path):
    os.startfile(path)

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

def setupSpotifyObject(config):
    token = util.prompt_for_user_token(
            config.get(CONFIG_BASE, 'username'),
            config.get(CONFIG_BASE, 'acessScope'),
            config.get(CONFIG_BASE, 'clientID'),
            config.get(CONFIG_BASE, 'clientSecret'),
            config.get(CONFIG_BASE, 'redirectURI'))
    return spotipy.Spotify(auth=token)

def create_config_file():
    config = configparser.ConfigParser()


    config[CONFIG_BASE] = {
        'accessScope': 'user-read-currently-playing',
        'redirectURI': 'http://localhost:8080/',
        'path': ''
    }

    for n in ('username', 'clientID', 'clientSecret'):
        config[CONFIG_BASE][n] = input(f'Enter Spotify {n}: ')

    with open(CONFIG_FILE, 'w') as cf:
        config.write(cf)

    print(f'Config file {CONFIG_FILE} created. Remove it to reconfigure.')

def load_config_file():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def main():
    config = load_config_file()
    spotify = setupSpotifyObject(config)

    while True:

        try:
            current_track = spotify.current_user_playing_track()
        except:
            print('token expired')
            spotify = setupSpotifyObject(config)
            current_track = spotify.current_user_playing_track()

        try:
            if current_track['currently_playing_type'] == 'ad':
                restartSpotify(path)
                print('Ad skipped')
        except TypeError:
            pass

        time.sleep(1)

if __name__ == '__main__':
    if not os.path.isfile(CONFIG_FILE):
        create_config_file()
    main()
