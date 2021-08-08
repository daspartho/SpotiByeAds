# SpotiByeAds

No one likes interruptions! right? So this program detects when an advertisement plays by monitoring the type of the track that is currently playing, using the Spotipy API. 
When an ad is detected, the program restarts Spotify by the os module and plays it via pynput, which skips the ad and starts right where you left off.

### Installation
```
git clone https://github.com/daspartho/SpotiByeAds.git
```
```
cd SpotiByeAds
```
```
pip install pynput spotipy
```


### Setting up

1. Go to https://developer.spotify.com/dashboard and sign in with your Spotify account.
2. Click on the 'CREATE AN APP' option and provide an app name and app description as you'd like.
3. Go to 'EDIT SETTINGS' and fill in the Redirect URIs placeholder with http://localhost:8080/, and click on Save.
4. Copy the Client ID and Client Secret and paste it in the corresponding place holders in main.py.
5. Paste the path to the spotify application on your computer in the PATH placeholder in main.py.
6. Paste your spotify username in the username placeholder in main.py

### Usage
1. Open spotify and start your favourite track.
2. Run the script in background using `python main.py` in the respective directory.
3. And just enjoy music without any interruptions.
