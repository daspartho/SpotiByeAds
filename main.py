import sys, os, time, shutil, subprocess, json  # Base Libs


try:
    import spotipy
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

def playSpotify():
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
    playSpotify()
    previousWindow()

def setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI):
    token = spotipy.util.prompt_for_user_token(username, scope, clientID,
                                               clientSecret, redirectURI)
    return spotipy.Spotify(auth=token)

def main(username, scope, clientID, clientSecret, redirectURI, path):    
    spotify = setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI)

    print("\nAwesome, that's all I needed. I'm watching for ads now <.<")
    restartSpotify(path)

    while True:
        
        try:
            current_track = spotify.current_user_playing_track()
        except spotipy.SpotifyException:
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
    PATH = (shutil.which("spotify")  # For any system with spotify on $PATH
            or ("{HOMEDRIVE}{HOMEPATH}\AppData\Roaming\Spotify\Spotify.exe"
                .format_map(os.environ) if os.name == "nt"  # Windows
                else "/Applications/Spotify.app" if sys.platform == "darwin"  # MacOS
                else ""  # Popen expects a path-like object, `None` results in an error.
               )
           )
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
        
        if save == "Y":
            save_obj = {
                "spotify_username": spotify_username,
                "spotify_client_id": spotify_client_id,
                "spotify_client_secret": spotify_client_secret
            }

            with open("./credentials.json", "w") as creds:
                creds.write(json.dumps(save_obj))
                creds.close()

                print("Saved.")

        else:
            print("Didn't recognize input, defaulted to not saving.")

    main(spotify_username, spotifyAccessScope, spotify_client_id, spotify_client_secret, spotifyRedirectURI, PATH)

