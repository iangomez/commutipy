# Commutipy
# Ian Gomez, 08/02/17

import sys
import spotipy
import spotipy.util as util
import keys

################################################################################
# Setup Spotify API															   #
################################################################################

username = keys.username
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope,
	client_id=keys.client_id,
	client_secret=keys.client_secret,
	redirect_uri=keys.redirect_uri)
sp = spotipy.Spotify(auth=token)
sp.trace = False

################################################################################
# Helper Functions															   #
################################################################################

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("%d %32.32s, %s" % (i, track['artists'][0]['name'],
            track['name']))

def delete_all_tracks(tracks):
	track_ids = []
	for i, item in enumerate(tracks['items']):
		track = item['track']
		track_ids.append(track['id'])
	results = sp.user_playlist_remove_all_occurrences_of_tracks(username,
				playlist_id, track_ids)

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def show_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set() # to avoid dups
    albums.sort(key=lambda album:album['name'].lower())
    for album in albums:
        name = album['name']
        if name not in seen:
            print((' ' + name))
            seen.add(name)

# IF album is in list, add store and lookup album object
# iterate through album for song ids and place in playlist

################################################################################
# Application																   #
################################################################################

# open list and read
# randomly select an album from a list
# search spotify to populate track ids
result = sp.search('aha shake heartbreak')

name = 'Radiohead'
artist = get_artist(name)
if artist:
    show_artist_albums(artist)
else:
    print("Can't find that artist")

track_ids = []

# # delete all current tracks and add new album to playlist
# playlist_id = '5FGOMBsm77sM3WjpdJeD1Z'
# results = sp.user_playlist(username, playlist_id=playlist_id)
# tracks = results['tracks']
# delete_all_tracks(tracks)
# results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
