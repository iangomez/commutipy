# commutipy

## Introduction
In the search for new music, it can often be difficult to find time to listen to new albums completely. Making a giant playlist full of albums I want to listen to, makes it feel like more of a chore than a new experience. Automating the process makes listening to new music of your choice a lot less overwhelming. 


Commutipy automatically updates a user's specified public spotify playlist from a pool of chosen albums every morning. Open the commutipy playlist and listen to a randomly picked album  you want to listen to on your commute. Just setup the script to run daily and add artist and album names to a text file.


This project has been ran on Windows and Linux. The only platform specific item is the path to the text file. All code has been written and run on **Python 3.x**. 

## Setup
Set up keys.py to obtain a Spotify instance. Register an application with Spotify to obtain `ClientID` and `ClientSecret`.
[Link to Spotify application managment](https://developer.spotify.com/my-applications).
Use `http://127.0.0.1` as your redirect uri. 

### Dependencies
`pip install -r requirements.txt` installs the required dependencies. 

- *Spotipy*: Python wrapper for Spotify which allows us to edit playlists
- *Pandas*: Makes it easier to modify csv files (for marking whether we've heard an album)
- *Pushbullet.py*: Used for debugging purposes. I.e. if the script is deployed to a headless raspberry pi, the push is functionally is essentially a `print()` to your phone. 

## To-do
Keep track of which albums were listened to completely (last.fm api?)
