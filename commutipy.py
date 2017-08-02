# Commutipy
# Ian Gomez, 08/02/17

import spotipy
import spotipy.util as util
import keys

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


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("%d %32.32s, %s" % (i, track['artists'][0]['name'],
                                  track['name']))


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
    results = sp.artist_albums(artist['id'], album_type='album')
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


###############################################################################
# Application                                                                 #
###############################################################################

# open list and read
# randomly select an album from a list

playlist_id = '5FGOMBsm77sM3WjpdJeD1Z'
name = 'Radiohead'
album_title = 'In Rainbows'

artist = get_artist(name)
album = get_album(artist, album_title)
track_ids = get_track_ids(album)
repopulate_playlist(username, playlist_id, track_ids)
