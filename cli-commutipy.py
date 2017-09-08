#!/usr/bin/python3
# Commutipy Status Check
# Ian Gomez, 09/02/17

import spotipy
import spotipy.util as util
import spotipy_helpers as sph
import csv_helpers as csvh
import keys

# Spotify login
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(keys.username, scope,
								client_id=keys.client_id,
								client_secret=keys.client_secret,
								redirect_uri=keys.redirect_uri)
sp = spotipy.Spotify(auth=token)
sp.trace = False

# User and playlist information
username = keys.username
playlist_ids = ['5FGOMBsm77sM3WjpdJeD1Z', '6R2BOuKmqyUjQ9qaPPbATH']
txtfiles = ['ian_albums.txt', 'ruqayya_albums.txt']
playlist_names = []

for playlist_id, txtfile in zip(playlist_ids, txtfiles):
	# Get current playlist name, album, and artist; identify the csv file
	playlist = sp.user_playlist(username, playlist_id=playlist_id)  # spotify obj
	playlist_name = playlist['name']
	playlist_names.append(playlist_name)
	album_name = playlist['tracks']['items'][0]['track']['album']['name']
	artist_name = playlist['tracks']['items'][0]['track']['artists'][0]['name']
	txtdir = '/home/ian/Dropbox/Python/commutipy-prod/{}'.format(txtfile)

	# csv reading. grabs unheard albums and places them in a list
	unheard_albums = []
	df = csvh.read_csv(txtdir)
	for album, heard in zip(df['Album'], df['Heard']):
		if heard != 1:
			unheard_albums.append(album)

	if len(unheard_albums) < 1:
		unheard_albums = 'All listened to. Add some more albums'

	info = ('----------------------------------\n'
			'Username:      {}\n'
			'Playlist:      {}\n'
			'Current album: {}\n'
			'----------------------------------\n'
			'{}\n'
			'----------------------------------'
			.format(username, playlist_name, album_name, df))

	print(info)

# CLI to add albums by searching artist.
while(1):
	print('\nList of commutipy playlists:')
	for i, name in enumerate(playlist_names):
		print(i, name)
	select_playlist_str = input('\nSelect index of playlist to modify: ')
	if select_playlist_str =='q':
		break

	if select_playlist_str.isdigit():
		select_playlist = int(select_playlist_str)
	else:
		print('Please choose a valid number')
		continue

	if select_playlist < len(playlist_names):
		txtfile = txtfiles[select_playlist]
		txtdir = '/home/ian/Dropbox/Python/commutipy-prod/{}'.format(txtfile)
		df = csvh.read_csv(txtdir)

	else:
		print('Please pick a valid playlist')
		continue

	while(1):
		search = input('\nEnter artist query or q to quit: ')
		search_artist = search.strip()
		if search_artist == 'q':
			break

		artist = sph.get_artist(sp, search_artist)
		artist_name = artist['name']
		if artist is not None:
			seen, found = sph.show_albums(sp, artist, '')
			print('\nHere are the albums available from {}:'.format(artist_name))

			ordered_seen = []
			for i, album in enumerate(seen):
				ordered_seen.append(album)
				print(i, album)
			number = input('\nPick an album by # or press q to go back to artist search: ')
			if number == 'q':
				continue
			else:
				# write the selected album and artist into the txt file
				album_name = ordered_seen[int(number)]
				df = csvh.append_csv(df, artist_name, album_name)
				csvh.write_csv(txtdir, df)
				print('{} - {} added to csv\n'.format(artist_name, album_name))
				print(df)

		else:
			print('Cannot find artist')
		print('----------------------------------\n')
