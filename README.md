# SpotiByeAds
 [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
 [![GitHub license](https://img.shields.io/github/license/daspartho/SpotiByeAds.svg)](https://github.com/daspartho/SpotiByeAds/blob/main/LICENSE)
 [![GitHub stars](https://img.shields.io/github/stars/daspartho/SpotiByeAds.svg?style=social&label=Stars&maxAge=2592000)](https://github.com/daspartho/SpotiByeAds/stargazers/)
 [![GitHub forks](https://img.shields.io/github/forks/daspartho/SpotiByeAds.svg?style=social&label=Forks&maxAge=2592000)](https://github.com/daspartho/SpotiByeAds/stargazers/)


No one likes interruptions! Don't you hate it when you're listening to your favorite jazz track or your EDM playlist and an ad for Old Spice or Pepsi starting playing interrupting your mood? With SpotiByeAds, you can listen ad-free allowing you to concentrating less on those ads and more towards the task at hand!

# How it works?
SpotiByeAds or SBA for short utilizes the SpotiPy and Pynput Libraries as well as the os system modules in order to provide you with a ad free experience.  First, it asks you for your Spotify Username, Client ID and Client Password(which is done by running ```python main.py ```). Of course if you've used this program and have saved credentials, it should load a json file with your credentials in it and if not, it will ask for your credentials(credentials being your Spotify Username, Client ID and Client Password). Note that for your first time, you have the option of either saving your credentials for future use or keeping your credentials just for this session of using SBA.

After SBA has your credentials, it will establish a connection with Spotify by restarting it and setting it to your last known track/playlist. When a ad enters your spotify queue, SBA will detect the current track as a ad and move to restart it. After the restart, SBA will automatically queue up your last track!

# Requirements
- Python(2 or 3. If using Python 3, make sure to replace pip with pip3 and python with python3 in the Installation and Settting sections)
- Pip (Python's Package Manager)

# Installation
### It should be noted that this is a quick way to get SBA (SpotiByeAds) up and running! For more indepth documentation, go [here](https://spotibyeads.readthedocs.io/en/latest/).

- First, clone the repository.
```
git clone https://github.com/daspartho/SpotiByeAds.git 
```
- Then, change your current directory into the SpotiByeAds repository.
```
cd SpotiByeAds
```
- Finally, install the requirements in the requirements file.
```
pip install -r requirements.txt
```
- From here, SpotiByeAds is installed. Continue to the Setting Up section in order to connect SpotiByeAds to Spotify itself.

# Setting up

1. Go to https://developer.spotify.com/dashboard and sign in with your Spotify account.
2. Click on the 'CREATE AN APP' option and provide an app name and app description as you'd like.
3. Go to 'EDIT SETTINGS' and fill in the Redirect URIs placeholder with http://localhost:8080/, and click on Save.
4. Copy the Client ID and Client Secret and paste it in the corresponding place holders in main.py. **Please remember to never share your Client Secret with anyone. This could lead to your account getting stolen or irregular Spotify user behavior that could lead to account termination. Developers of SpotiByeAds will never ask for your Client Secret.**
5. Paste the path to the Spotify application on your computer in the PATH placeholder in main.py.
6. Paste your Spotify username in the username placeholder in main.py


# Usage
1. Open Spotify and start your favourite track.
2. Run the script in background using `python main.py` in the respective directory.
3. Congratulations! You can now listen to Spotify with no ads and the peace of mind you deserve :D.

# Contributing
If you want to contribute code, just write a quick pull request and the developers will look at it. If you want to suggest a idea, just write a issue and the developers will check it out!

# Building
## MacOS / Linux 
If you'd like to build for Mac / Linux, do the following:
1. To build in a development environment (to make sure it works right), run `python setup.py py2app -A`. Please note: This builds the app in something called *alias mode*. This is NOT a proper build, and will only work on the machine it was run on.
2. To build a proper package, run `python setup.py py2app`. 
