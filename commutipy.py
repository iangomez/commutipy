#!/home/ian/anaconda3/bin/python3.6
# Commutipy
# Ian Gomez, 08/02/17

import spotipy
import spotipy.oauth2
import spotipy.util as util
import keys
import random
import pandas
import sys
from pushbullet import Pushbullet
pb = Pushbullet(keys.pbapi)


###############################################################################
# Setup Spotify                                                               #
###############################################################################

# username = keys.username
# scope = 'playlist-modify-public'
# token = util.prompt_for_user_token(username, scope,
#                                    client_id=keys.client_id,
#                                    client_secret=keys.client_secret,
#                                    redirect_uri=keys.redirect_uri)
# sp = spotipy.Spotify(auth=token)
# sp.trace = False

# https://github.com/sheagcraig/actually_random/blob/master/actually_random.py

auth_token = None
username = keys.username
scope = 'playlist-modify-public'
oauth = spotipy.oauth2.SpotifyOAuth(
        keys.client_id, keys.client_secret, keys.redirect_uri, scope=scope,
        cache_path=".tokens")
token_info = oauth.get_cached_token()
if not token_info and auth_token:
    token_info = oauth.get_access_token(auth_token)
sp = spotipy.Spotify(token_info["access_token"])
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
        albums.extend(results['items'])
        while(results['next']):  # helps with pagination
            results = sp.next(results)
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
    return pandas.read_csv(txtdir, sep='\t')  


def write_csv(txtdir, df):
    df.to_csv(txtdir, sep='\t')

    
def pick_rand(txtdir, df):
    album_num = len(df['Album'])      
    
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

# Platform check
s = sys.platform
txtfile = 'test_albums.txt'
if s == 'linux':
    txtdir = '/home/ian/Dropbox/Python/commutipy/{}'.format(txtfile)
elif s == 'win32':
    txtdir = 'C:\\Users\\ME123\\Dropbox\\Python\\commutipy\\{}'.format(txtfile)
else:
    raise EnvironmentError('Unsupported platform')

# Gather random album from the text file
playlist_id = '5FGOMBsm77sM3WjpdJeD1Z'
df = read_csv(txtdir)
artist_name, album_title = pick_rand(txtdir, df)

# Search artist, get the specific album, populate the playlist with tracks
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

#artist = get_artist(artist_name)
#if artist:
#    album = get_album(artist, album_title)
#    if album:
#        track_ids = get_track_ids(album)
#        repopulate_playlist(username, playlist_id, track_ids)
#        print('Added: {} - {}'.format(artist_name, album_title))
#    else:
#        print('Cannot find album: {} - {}'.format(artist_name, album_title))
#else:
#    print('Cannot find artist: {} - {}'.format(artist_name, album_title))
