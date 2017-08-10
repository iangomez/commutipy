#!/home/ian/anaconda3/bin/python3.6
# Commutipy
# Ian Gomez, 08/02/17

import spotipy
import spotipy.util as util
import spotipy_helpers as sph
import keys
import random
import pandas
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
# Helper Functions                                                            #
###############################################################################


def to_bool(arg):
	return int(arg) == 1  # interprets the 0 or 1 in heard as True or False


def read_csv(txtdir):
	return pandas.read_csv(txtdir, sep='\t')


def write_csv(txtdir, df):
	df.to_csv(txtdir, sep='\t')


def pick_rand(txtdir, df):
	album_num = len(df['Album'])  # get number of albums in the file

	# pick random entry that hasn't been heard
	r = random.randrange(album_num)
	heard = df['Heard'][r]
	while(to_bool(heard)):
		r = random.randrange(album_num)
		heard = df['Heard'][r]

	# set artist & album and set heard
	artist_name = df['Artist'][r]
	album_title = df['Album'][r]
	df.loc[r, 'Heard'] = 1

	write_csv(txtdir, df)
	return artist_name, album_title


###############################################################################
# Application                                                                 #
###############################################################################

# Specify the name of the text file (tab delimited csv)
txtfile = 'ian_albums.txt'

# Specify playlist id
playlist_id = '5FGOMBsm77sM3WjpdJeD1Z'

# Platform check and directory
# Change the directory to your own
if sys.platform == 'linux':
	txtdir = '/home/ian/Dropbox/Python/commutipy/{}'.format(txtfile)
elif sys.platform == 'win32':
	txtdir = 'C:\\Users\\ME123\\Dropbox\\Python\\commutipy\\{}'.format(txtfile)
else:
	raise EnvironmentError('Unsupported platform')

# Gather random album from the text file
df = read_csv(txtdir)
artist_name, album_title = pick_rand(txtdir, df)

# Search artist, get the specific album, populate the playlist with tracks
artist = sph.get_artist(sp, artist_name)
if artist:
	album = sph.get_album(sp, artist, album_title)
	if album:
		track_ids = sph.get_track_ids(sp, album)
		sph.repopulate_playlist(sp, username, playlist_id, track_ids)
		print('Added: {} - {}'.format(artist_name, album_title))                       album_title))
	else:
		print('Cannot find album: {} - {}'.format(artist_name, album_title))
else:
	print('Cannot find artist: {} - {}'.format(artist_name, album_title))
