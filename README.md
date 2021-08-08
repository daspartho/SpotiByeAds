# SpotiByeAds

No one likes interruptions! right? So this program detects when an advertisement plays by monitoring the type of the track that is currently playing, using the Spotipy API. 
When an ad is detected, the program restarts Spotify by the os module and plays it via pynput, which skips the ad and starts right where you left off.

### Installation
```
git clone https://github.com/daspartho/SpotiByeAds.git
cd SpotiByeAds
pip install -r requirements.txt
```

### Setting up

1. Go to https://developer.spotify.com/dashboard and sign in with your Spotify account.
2. Click on the 'CREATE AN APP' option and provide an app name and app description as you'd like.
3. Go to 'EDIT SETTINGS' and fill in the Redirect URIs placeholder with http://localhost:8080/, and click on Save.
4. Make a note of your ClientID and Client Secret. You'll need it in a minute.
5. (Optional) By default SpotiByeAds will detect the location of your Spotify installation. However, if you'd like you can change the `PATH` variable to your Spotify location. 

### Usage
1. Open Spotify and start your favourite track.
2. Run the script in background using `python main.py` in the respective directory.
3. When the program asks you for your ClientID, Client Secret, and username, just type them in or copy/paste them in.
4. And just enjoy music without any interruptions.

### Building
#### MacOS
If you'd like to build for Mac, do the following:
1. To build in a development environment (to make sure it works right), run `python setup.py py2app -A`. Please note: This builds the app in something called *alias mode*. This is NOT a proper build, and will only work on the machine it was run on.
2. To build a proper package, run `python setup.py py2app`. 