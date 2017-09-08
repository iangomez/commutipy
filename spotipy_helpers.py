""" spotify_helpers.py

This module houses all the Spotipy helper functions.

"""

def get_artist(sp, artist_name):
	"""
	Get the first result of an artist search given a Spotify instance and name.

	Args:
		sp (Spotify instance): an authorized instance
		artist_name (str): name of the artist

	Returns:
		returns a Spotify artist json object
			if there is no artist found, returns None
	"""
	results = sp.search(q='artist:' + artist_name, type='artist')
	items = results['artists']['items']
	if len(items) > 0:
		return items[0]
	else:
		return None


def get_album(sp, artist, album_title):
	"""
	Gets the specified album from the artist given.

	Args:
		sp (Spotify instance): an authorized instance
		artist (json): an artist object
		album_title (str): an album title

	Returns:
		returns an album json
			if there is no album found, return None
	"""
	albums = []
	album_types = ['album', 'single', 'compilation']
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

def show_albums(sp, artist, album_title):
	found = False
	albums = []
	album_types = ['album', 'single', 'compilation']
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


def get_track_ids(sp, album):
	"""
	Parse tracks from album and grab the track ids.

	Args:
		sp (Spotify instance): an authorized instance
		album (json): an album object

	Returns:
		returns a Spotify artist json object
			if there is no artist found, returns None
	"""
	track_ids = []
	for item in album['tracks']['items']:
		track_ids.append(item['id'])
	return track_ids


def repopulate_playlist(sp, username, playlist_id, track_ids):
	"""
	Create a playlist object, grab the current tracks and delete them, and add
	tracks using track ids provided.

	Args:
		sp (Spotify instance): an authorized instance
		username (str): Spotify username
		playlist_id (str): the playlist uri
		track_ids ([str]): list of track ids (Spotify uri)

	Returns:
		returns None
	"""
	playlist = sp.user_playlist(username, playlist_id=playlist_id)
	old_tracks = playlist['tracks']
	delete_all_tracks(sp, username, playlist_id, old_tracks)
	sp.user_playlist_add_tracks(username, playlist_id, track_ids)


def delete_all_tracks(sp, username, playlist_id, tracks):
	"""
	Delete the specified tracks from the user's playlist

	Args:
		sp (Spotify instance): an authorized instance
		username (str): Spotify username
		playlist_id (str): the playlist uri
		tracks ([str]): list of spotify tracks to delete

	Returns:
		returns None
	"""
	track_ids = []
	for item in tracks['items']:
		track = item['track']
		track_ids.append(track['id'])
	sp.user_playlist_remove_all_occurrences_of_tracks(username,
													  playlist_id, track_ids)
