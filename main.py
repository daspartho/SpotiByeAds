from os import error


while True: #If we get no import errors then break from the loop. If we do get an error install the dependencies and do the try/catch block again.
     try:
         import os,time,shutil,subprocess,json #Base Libs
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
            os.system("taskkill /f /im Spotify.exe")
    elif os.name == "posix":
        # macos
        os.system("kill -9 13068")
    else:
        # almost everything else
        os.system("killall -9 spotify")

def openSpotify(path):
    if path is None:
        path = shutil.which("Spotify")
    if path is None and os.name == "posix":
        path = "/Applications/Spotify.app"

    subprocess.Popen([path], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def playSpotify():
    keyboard = Controller()
    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)
    
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
    # these are kinda constants
    PATH = None;
    spotifyAccessScope = "user-read-currently-playing"
    spotifyRedirectURI = "http://localhost:8080/"

    try:
        with open("./credentials.json", "r") as creds_json:
            creds = json.load(creds_json)

            load = input("Found previously used credentials. Want to use them again? (Y/n) ")

            if load != "Y": 
                raise FileNotFoundError("User didn't want to load from save.");

            spotify_username = creds["spotify_username"]
            spotify_client_id = creds["spotify_client_id"]
            spotify_client_secret = creds["spotify_client_secret"]

            creds_json.close();
    except FileNotFoundError:
        spotify_username = input("Ok, what's your Spotify username? ")
        spotify_client_id = input("Great, now what's the ClientID you're using? ")
        spotify_client_secret = input("Beautiful, now how about the Client Secret? ")

        save = input("Awesome, now would you like to save these settings for future sessions? (Y/n) ")
        
        if save.lower() == "y":
            save_obj = {
                "spotify_username": spotify_username,
                "spotify_client_id": spotify_client_id,
                "spotify_client_secret": spotify_client_secret
            }

            with open("./credentials.json", "w") as creds:
                creds.write(json.dumps(save_obj))
                creds.close()

                print("Saved.")

        elif save.lower() == "n":
            print("Not saving settings.")

        else:
            print("Didn't recognize input, defaulted to not saving.")

    main(spotify_username, spotifyAccessScope, spotify_client_id, spotify_client_secret, spotifyRedirectURI, PATH)

