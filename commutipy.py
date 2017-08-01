import sys
import spotipy
import spotipy.util as util
import keys

username = keys.username
scope = 'user-library-read'
token = util.prompt_for_user_token(username, scope,
	client_id=keys.client_id,
	client_secret=keys.client_secret,
	redirect_uri=keys.redirect_uri)
sp = spotipy.Spotify(auth=token)

results = sp.current_user_saved_tracks()
for item in results['items']:
    track = item['track']
    print(track['name'] + ' - ' + track['artists'][0]['name'])
