#!/home/ian/anaconda3/bin/python3.6
# Commutipy
# Ian Gomez, 08/02/17

import spotipy
import spotipy.util as util
import spotipy_helpers as sph
import csv_helpers as csvh
import ikeys as keys  # change to import keys

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
# Application                                                                 #
###############################################################################

# Specify the name of the text file (tab delimited csv) & playlist id
txtfile = 'ian_albums.txt'
txtdir = '/home/ian/Dropbox/Python/commutipy/{}'.format(txtfile)
playlist_id = '5FGOMBsm77sM3WjpdJeD1Z'

# Gather random album from the text file
df = csvh.read_csv(txtdir)
artist_name, album_title = csvh.pick_rand(txtdir, df)

# Search artist, get the specific album, populate the playlist with tracks
artist = sph.get_artist(sp, artist_name)
if artist:
	album = sph.get_album(sp, artist, album_title)
	if album:
		track_ids = sph.get_track_ids(sp, album)
		sph.repopulate_playlist(sp, username, playlist_id, track_ids)
		print('Added: {} - {}'.format(artist_name, album_title))
	else:
		print('Cannot find album: {} - {}'.format(artist_name, album_title))
else:
	print('Cannot find artist: {} - {}'.format(artist_name, album_title))
