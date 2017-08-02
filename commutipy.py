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
	results = sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, track_ids)

################################################################################
# Application																   #
################################################################################

# open list and read
# randomly select an album from a list
# search spotify to populate track ids
track_ids = ['2WGzDLofKXzEUV2cksDk1l']
playlist_id = '5FGOMBsm77sM3WjpdJeD1Z'

# add the songs to the playlist in proper order
results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)

# delete all tracks
results = sp.user_playlist(username, playlist_id=playlist_id)
tracks = results['tracks']
delete_all_tracks(tracks)
