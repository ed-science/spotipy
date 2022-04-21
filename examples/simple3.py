import sys

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

name = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'Radiohead'
results = sp.search(q=f'artist:{name}', type='artist')
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    print(artist['name'], artist['images'][0]['url'])
