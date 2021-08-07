while True: #If we get no import errors then break from the loop. If we do get an error install the dependencies and do the try/catch block again.
     try:
         import os,time,shutil,subprocess #Base Libs
         import spotipy
         from spotipy import util, SpotifyException
         from pynput.keyboard import Key, Controller
         break
     except ImportError:
         print("Import Error: Downloading off 'requirements.txt'")
         time.sleep(1)
         os.system("pip3 install -r requirements.txt")
         print("Done!")

#Vars
keyboard = Controller() #I noticed how we kept making a new keyboard controller instance so decided to just make it a variable

def closeSpotify():
    if os.name == "nt":
        # windows
            os.system("taskkill /f /im spotify.exe")
    elif os.name == "posix":
        # macos
        os.system("kill -9 13068")
    else:
        # almost everything else
        os.system("killall -9 spotify")

def openSpotify(path):
    if path is None:
        path = shutil.which("spotify")
    if path is None and os.name == "posix":
        path = "/Applications/Spotify.app"

    subprocess.Popen([path], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def playSpotify():
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)
    
def previousWindow():
    keyboard.press(Key.alt_l)
    keyboard.press(Key.tab)
    keyboard.release(Key.alt_l)
    keyboard.release(Key.tab)
    
def restartSpotify(path:str):
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

    print("\nAwesome, that's all I needed. I'm watching for ads now <.<")
    restartSpotify(path)

    while True:
        
        try:
            current_track = spotify.current_user_playing_track()
        except spotipy.exceptions.SpotifyException:
            print('Token expired')
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
    
    PATH = None
    spotifyUsername = input("Ok, what's your Spotify username? ")
    spotifyClientID = input("Great, now what's the ClientID you're using? ")
    spotifyClientSecret = input("Beautiful, now how about the Client Secret? ")
    spotifyAccessScope = "user-read-currently-playing"
    spotifyRedirectURI = "http://localhost:8080/"

    main(spotifyUsername, spotifyAccessScope, spotifyClientID, spotifyClientSecret, spotifyRedirectURI, PATH)

