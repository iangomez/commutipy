#!/home/ian/anaconda3/bin/python3.6
# Commutipy
# Ian Gomez, 08/02/17

import spotipy
import spotipy.util as util
import keys
import csv
import random
import pandas
import sys
from pushbullet import Pushbullet
pb = Pushbullet(keys.pbapi)


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

def delete_all_tracks(username, playlist_id, tracks):
    track_ids = []
    for item in tracks['items']:
        track = item['track']
        track_ids.append(track['id'])
    sp.user_playlist_remove_all_occurrences_of_tracks(username,
                                                      playlist_id, track_ids)


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def get_album(artist, album_title):
    albums = []
    album_types = ['album', 'compilation']
    for type in album_types:
	    results = sp.artist_albums(artist['id'], album_type=type, limit='50')
	    for album in results:
	        albums.extend(results['items'])

    seen = set()  # to avoid dups
    albums.sort(key=lambda album: album['name'].lower())
    for album in albums:
        name = album['name']
        if name not in seen:
            seen.add(name)
            if album_title.lower() == name.lower():
                album_id = album['id']
                return sp.album(album_id)
    return None


def get_track_ids(album):
    track_ids = []
    for item in album['tracks']['items']:
        track_ids.append(item['id'])
    return track_ids


def repopulate_playlist(username, playlist_id, track_ids):
    playlist = sp.user_playlist(username, playlist_id=playlist_id)
    tracks = playlist['tracks']
    delete_all_tracks(username, playlist_id, tracks)
    sp.user_playlist_add_tracks(username, playlist_id, track_ids)


def to_bool(arg):
    return int(arg) == 1


def read_csv(txtdir):
    artists = []; albums = []; heard = []
    with open(txtdir, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            artists.append(row[0])
            albums.append(row[1])
            heard.append(row[2])
    return artists, albums, heard


def pick_rand(artists, albums, heard):
    r = random.randrange(len(artists))
    while(to_bool(heard[r])):
        r = random.randrange(len(artists))
    artist_name = artists[r].strip()
    album_title = albums[r].strip()
    record_listened(r)
    return artist_name, album_title


def record_listened(r):
    # use the random number to write to the csv that we listened to the album
    # or use last.fm to confirm that we listened to the whole album before
    # changing it to a new one
    print()

###############################################################################
# Application                                                                 #
###############################################################################

# Platform check
s = sys.platform
if s=='linux':
	txtdir = '/home/ian/Dropbox/Python/commutipy/ian_albums.txt'
elif s=='win32':
	txtdir = 'C:\\Users\\ME123\\Dropbox\\Python\\commutipy\\ian_albums.txt'
else:
	raise EnvironmentError('Unsupported platform')

# Gather album from the text file
playlist_id = '5FGOMBsm77sM3WjpdJeD1Z'
artists, albums, heard = read_csv(txtdir)
artist_name, album_title = pick_rand(artists, albums, heard)

# Search artist, get the specific anitedlbum, populate the playlist with tracks
artist = get_artist(artist_name)
if artist:
    album = get_album(artist, album_title)
    if album:
        track_ids = get_track_ids(album)
        repopulate_playlist(username, playlist_id, track_ids)
        push = pb.push_note('Commutipy', 'Added: {} - {}'.format(artist_name,
                            album_title))
    else:
        push = pb.push_note('Commutipy', 'Cannot find album: {} - {}'
                            .format(artist_name, album_title))
else:
    push = pb.push_note('Commutipy', 'Cannot find artist: {} - {}'
                        .format(artist_name, album_title))
