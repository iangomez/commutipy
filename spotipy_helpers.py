

def delete_all_tracks(sp, username, playlist_id, tracks):
    track_ids = []
    for item in tracks['items']:
        track = item['track']
        track_ids.append(track['id'])
    sp.user_playlist_remove_all_occurrences_of_tracks(username,
                                                      playlist_id, track_ids)


def get_artist(sp, name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def get_album(sp, artist, album_title):
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
            if album_title.lower() == name.lower():  # check for a match
                album_id = album['id']
                return sp.album(album_id)
    return None


def get_track_ids(sp, album):
    track_ids = []
    for item in album['tracks']['items']:
        track_ids.append(item['id'])
    return track_ids


def repopulate_playlist(sp, username, playlist_id, track_ids):
    playlist = sp.user_playlist(username, playlist_id=playlist_id)
    tracks = playlist['tracks']
    delete_all_tracks(username, playlist_id, tracks)
    sp.user_playlist_add_tracks(username, playlist_id, track_ids)
