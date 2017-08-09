#!/home/ian/anaconda3/bin/python3.6
# Check Spotify
# for the artist and album in question
# Ian Gomez, 08/08/17

# TODO 
# Use regex to suggest the closest album title; useful for remastered or deluxe

import spotipy
import spotipy.util as util
import keys
import sys

###############################################################################
# Setup Spotify                                                               #
###############################################################################

username = keys.username
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope,
                                   client_id=keys.client_id,
                                   client_secret=keys.client_secret,
                                   redirect_uri=keys.redirect_uri)
sp = spotipy.Spotify(auth=token)
sp.trace = False

###############################################################################
# Helper functions                                                            #
###############################################################################

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_albums(artist, album_title):
    found = False
    albums = []
    album_types = ['album']
    for type in album_types:
        results = sp.artist_albums(artist['id'], album_type=type, limit='50')
        albums.extend(results['items'])
        while(results['next']):
            print('next')
            results = sp.next(results)
            albums.extend(results['items'])
    seen = set()  # to avoid dups
    albums.sort(key=lambda album: album['name'].lower())
    for album in albums:
        name = album['name']
        if name not in seen:
            seen.add(name)
            if album_title.lower() == name.lower():
                found = True
    return seen, found 

###############################################################################
# Application                                                                 #
###############################################################################

if len(sys.argv) > 1: 
    info = ""
    for arg in sys.argv[1:]:
        info = '{} {}'.format(info,arg)
    infolist = info.split(':') 
    artist_name = infolist[0].strip()
    album_title = infolist[1].strip()   

else:
	print('usage: check_spotify.py <artst>: <album>')
	sys.exit(2)

artist = get_artist(artist_name)
seen, found = show_albums(artist,album_title)
if found:
	print('{} - {} is in Spotify\'s library'.format(artist_name, album_title))
else:
    print('\n{} was not found'.format(album_title))
    print('----------------------')
    print('\nHere are the albums available:\n')
    for album in seen:
        print(album)