import time
import os
import spotipy
from spotipy import util
from pynput.keyboard import Key, Controller
import json

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

def setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI):
    token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI)
    return spotipy.Spotify(auth=token)

def main(username, scope, clientID, clientSecret, redirectURI, path):    
    spotify = setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI)

    while True:
        
        try:
            current_track = spotify.current_user_playing_track()
        except:
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
    
    try:
        with open("credentials.json", "r") as credentials_json:
            credentials = json.load(credentials_json)
            PATH = credentials["PATH"]
            spotify_username = credentials["spotify_username"]
            spotify_client_id = credentials["spotify_client_id"]
            spotify_client_secret = credentials["spotify_client_secret"]
            ACCESS_SCOPE = credentials["ACCESS_SCOPE"]
            REDIRECT_URI = credentials["REDIRECT_URI"]
    except FileNotFoundError:
        print("SpotiByeAds setup:")
        
        PATH = input("Where is your Spotify.exe located? ")
        spotify_username = input("What is your Spotify username? ")
        spotify_client_id = input("What is your Client ID? ")
        spotify_client_secret = input("What is your Client Secret? ")
        ACCESS_SCOPE = "user-read-currently-playing"
        REDIRECT_URI = "http://localhost:8080/"

        spotify_credentials = {"PATH":PATH, "spotify_username":spotify_username, "spotify_client_id":spotify_client_id, "spotify_client_secret":spotify_client_secret, "ACCESS_SCOPE":ACCESS_SCOPE, "REDIRECT_URI":REDIRECT_URI}
        
        with open("credentials.json", "w") as credentials:
            credentials.write(json.dumps(spotify_credentials))



    main(spotify_username, ACCESS_SCOPE, spotify_client_id, spotify_client_secret, REDIRECT_URI, PATH)

