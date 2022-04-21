import argparse
import logging

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

logger = logging.getLogger('examples.artist_albums')
logging.basicConfig(level='INFO')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_args():
    parser = argparse.ArgumentParser(description='Gets albums from artist')
    parser.add_argument('-a', '--artist', required=True,
                        help='Name of Artist')
    return parser.parse_args()


def get_artist(name):
    results = sp.search(q=f'artist:{name}', type='artist')
    items = results['artists']['items']
    return items[0] if len(items) > 0 else None


def show_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set()  # to avoid dups
    albums.sort(key=lambda album: album['name'].lower())
    for album in albums:
        name = album['name']
        if name not in seen:
            logger.info('ALBUM: %s', name)
            seen.add(name)


def main():
    args = get_args()
    if artist := get_artist(args.artist):
        show_artist_albums(artist)
    else:
        logger.error("Can't find artist: %s", artist)


if __name__ == '__main__':
    main()
