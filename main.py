#NOTE: Most of the other fixes dynamic spotify support came from https://github.com/daspartho/SpotiByeAds/pull/3

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
        os.system("taskkill /f /im spotify.exe") #Windows
    else:
        os.system("killall -9 spotify") #Other

def openSpotify(path:str):
    if not path: #If we did not provide a value for path
        path = shutil.which("spotify")
    
    subprocess.Popen([path], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
    try:
        token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI)
        return spotipy.Spotify(auth=token)
    except Exception: #I dont feel like reading the docs
        exit("Error: Invalid/Incorrect Credentials")

def main(username, scope, clientID, clientSecret, redirectURI, path):    
    spotify = setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI)
    restartSpotify(path)

    while True:
        try:
            if spotify.current_user_playing_track()['currently_playing_type'] == "ad":
                restartSpotify(path)
                print("Ad Skipped")
        except SpotifyException: #I checked the docs and it only throws "spotipy.client.SpotifyException"...weird
            print("Token Expired")
            spotify = setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI)
        

        time.sleep(spotify.current_user_playing_track['duration_ms']/1000) 
        #Instead of checking every second for an ad. We simply get the total length of the song and wait for that ammount of time. 
        #Now spotify returns miliseconds for song length which is weird but this can easily be fixed with some basic math.
        #We get the song duration and divide it by 1000 and we get our time in seconds

if __name__ == '__main__':
    PATH = ""
    spotifyUsername = ""
    spotifyClientID = ""
    spotifyClientSecret = ""
    spotifyAccessScope = "user-read-currently-playing"
    spotifyRedirectURI = "http://localhost:8080/"

    main(spotifyUsername, spotifyAccessScope, spotifyClientID, spotifyClientSecret, spotifyRedirectURI, PATH)

