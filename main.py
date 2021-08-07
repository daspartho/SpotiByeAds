import time
import os
import sys
import configparser
import psutil

import spotipy
from spotipy import util
from pynput.keyboard import Key, Controller

CONFIG_FILE = 'config.properties'
CONFIG_BASE = 'spotify'

def close_spotify():
    find_spotify_process().kill()

def open_spotify(path):
    import webbrowser
    webbrowser.open(path)

def play_spotify():
    keyboard = Controller()
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)
    
def previous_window():
    keyboard = Controller()
    keyboard.press(Key.alt_l)
    keyboard.press(Key.tab)
    keyboard.release(Key.alt_l)
    keyboard.release(Key.tab)
    
def restart_spotify():
    path = find_spotify_absolute_path()
    close_spotify()
    open_spotify(path)
    time.sleep(5)
    play_spotify()
    previous_window()

def setup_spotify_object(config):
    token = util.prompt_for_user_token(
            config.get(CONFIG_BASE, 'username'),
            config.get(CONFIG_BASE, 'access_scope'),
            config.get(CONFIG_BASE, 'client_id'),
            config.get(CONFIG_BASE, 'client_secret'),
            config.get(CONFIG_BASE, 'redirect_uri'))
    return spotipy.Spotify(auth=token)

def find_spotify_process():
    for proc in psutil.process_iter():
        if 'spotify' in proc.name().lower():
            return proc
    return None

def find_spotify_absolute_path():
    proc = find_spotify_process()
    if proc is None:
        print('Please, run the Spotify app and try again')
        sys.exit(-1)
    return proc.cmdline()[0]

def create_config_file():
    config = configparser.ConfigParser()

    config[CONFIG_BASE] = {
        'access_scope': 'user-read-currently-playing',
        'redirect_uri': 'http://localhost:8080/',
    }

    for n in ('username', 'client_id', 'client_secret'):
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
    spotify = setup_spotify_object(config)

    while True:

        try:
            current_track = spotify.current_user_playing_track()
        except:
            print('token expired')
            spotify = setup_spotify_object(config)
            current_track = spotify.current_user_playing_track()

        try:
            if current_track['currently_playing_type'] == 'ad':
                restart_spotify()
                print('Ad skipped')
        except TypeError:
            pass

        time.sleep(1)

if __name__ == '__main__':
    if not os.path.isfile(CONFIG_FILE):
        create_config_file()
    main()
