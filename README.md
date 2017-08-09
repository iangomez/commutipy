# commutipy

## Introduction
In the search for new music, it can often be difficult to find time to listen to new albums completely. Making a giant playlist full of albums I want to listen to, makes it feel like more of a chore than a new experience. Automating the process makes listening to new music of your choice a lot less overwhelming. 


Commutipy automatically updates a user's specified public spotify playlist from a pool of chosen albums every morning. Open the commutipy playlist and listen to a randomly picked album  you want to listen to on your commute. Just setup the script to run daily and add artist and album names to a text file.


This project runs on Windows and Linux. The only platform specific item is the path to the text file (so modifying for Mac should be simple). All code has been written and run on **Python 3.x**. 

## Setup
1. Get Spotify credentials (`username`, `client_id`, `client_secret`, `redirect_uri`)
2. Get pushbullet credentials (`pubapi`)
3. Install dependencies 
4. First run setup

### Spotify Credententials
Register an application with Spotify to obtain `ClientID` and `ClientSecret`.
[Link to Spotify application managment](https://developer.spotify.com/my-applications).
Use `http://127.0.0.1` as your redirect uri (make sure to save if you do any modifications on your application page). Add this information to keys.py.

### Pusbullet Credentials
If you want to use Pushbullet, you must also obtain an api key. Go to [Pushbullet's settings](https://www.pushbullet.com/#settings/account) and request a token. (You can remove the pushbullet calls to avoid using Pusbullet.) Add this information to keys.py.

### Dependencies
`pip install -r requirements.txt` installs the required dependencies. 

- *Spotipy*: Python wrapper for Spotify which allows us to edit playlists
- *Pandas*: Makes it easier to modify csv files (for marking whether we've heard an album)
- *Pushbullet.py*: Used for debugging purposes. I.e. if the script is deployed to a headless raspberry pi, the push is functionally is essentially a `print()` to your phone. 

### First Run Setup
Make sure to get the uri of the playlist you want to edit. Go to Spotify, share a playlist and there should be a uri option. You just need the end (example: `spotify:user:12129446897:playlist:5GHOJEsm77aM3XfdsPeD1Z`. You just want `5GHOJEsm77aM3XfdsPeD1Z`). 


The Spotify instance will ask for a url containing the authorization code ([read the docs to understand the flow](https://spotipy.readthedocs.io/en/latest/#authorization-code-flow)), copy & paste that back into your console, and it should work. 

## To-do
Keep track of which albums were listened to completely (last.fm api?)
