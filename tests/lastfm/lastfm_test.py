#!/usr/bin/python3
# Last.fm test
# Ian Gomez
# 08/14/17

import ikeys as keys
import pylast

password_hash = pylast.md5(keys.lastfm_password)

network = pylast.LastFMNetwork(api_key=keys.lastfm_api,
                               api_secret=keys.lastfm_secret,
                               username=keys.lastfm_username,
                               password_hash=password_hash)

top_artists = network.get_top_artists()
print('\nTop Artists:\n')
for item in top_artists:
    print(item[0])

print('\n-----------\n')

top_tracks = network.get_top_tracks()
print('Top Tracks:\n')
for item in top_tracks:
    print(item[0])
