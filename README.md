# SpotiByeAds

No one likes interruptions! right? So this program detects when an advertisement plays by monitoring the type of the track that is currently playing, using the Spotipy API. 
When an ad is detected, the program restarts Spotify by the os module and plays it via pynput, which skips the ad and starts right where you left off.

### Documentation
Installation and setup instructions can be found in the documentation at [www.spotibyeads.readthedocs.io](https://spotibyeads.readthedocs.io/en/latest/).

### Building
#### MacOS
If you'd like to build for Mac, do the following:
1. To build in a development environment (to make sure it works right), run `python setup.py py2app -A`. Please note: This builds the app in something called *alias mode*. This is NOT a proper build, and will only work on the machine it was run on.
2. To build a proper package, run `python setup.py py2app`. 
