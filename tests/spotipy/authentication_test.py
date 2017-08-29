#!/home/ian/anaconda3/bin/python3.6
import spotipy
import spotipy.oauth2
import requests
import ikeys as keys
# attempt to avoid user interaction
# https://github.com/sheagcraig/actually_random/blob/master/actually_random.py

auth_token = None
username = keys.username
scope = 'playlist-modify-public'

oauth = spotipy.oauth2.SpotifyOAuth(
        keys.client_id, keys.client_secret, keys.redirect_uri, scope=scope,
        cache_path=".tokens")

# get auth_token
req_url = oauth.get_authorize_url()
r = requests.get(req_url)

# this requests the spotify login page (sigh)

token_info = oauth.get_cached_token()
if not token_info and auth_token:
    token_info = oauth.get_access_token(auth_token)

sp = spotipy.Spotify(token_info["access_token"])
sp.trace = False
