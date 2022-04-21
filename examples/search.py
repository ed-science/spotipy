# shows artist info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint

search_str = sys.argv[1] if len(sys.argv) > 1 else 'Radiohead'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
result = sp.search(search_str)
pprint.pprint(result)
