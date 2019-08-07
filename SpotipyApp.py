import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

with open('secret_data.json', 'r') as f:
    data = json.load(f)
os.environ['SPOTIPY_CLIENT_ID'] = data['Client ID']
os.environ['SPOTIPY_CLIENT_SECRET'] = data['Client Secret']
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
