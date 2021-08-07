# SpotiByeAds

No one likes interruptions! right? So this program detects when an advertisement plays by monitoring the type of the track that is currently playing, using the Spotipy API. 
When an ad is detected, the program restarts Spotify by the os module and plays it via pynput, which skips the ad and starts right where you left off.

### Installation

Clone this repo:
```
git clone https://github.com/daspartho/SpotiByeAds.git
```

Install dependencies:
```
cd SpotiByeAds
pip install -r requirements.txt
```

Run SpotiByeAds:
```
python main.py
```

When you run it the first time, it will ask you for `username`, `clientID` and `clientSecret`.
Follow these instructions to get it:
1. Go to https://developer.spotify.com/dashboard and sign in with your Spotify account.
1. Click on the 'CREATE AN APP' option and provide an app name and app description as you'd like.
1. Go to 'EDIT SETTINGS' and fill in the Redirect URIs placeholder with http://localhost:8080/, and click on Save.
1. Copy the Client ID and Client Secret and paste it in the console where you are running SpotiByeAds.
1. You can find your `username` in the Spotify App. Click in 'Account'. It is a long alphanumeric string, example: `9xk7mnsunkowdi05s8yrm8sfi`

### Usage
1. Open spotify and start your favourite track.
1. Run the script in background using `python main.py` in the respective directory.
1. And just enjoy music without any interruptions.
