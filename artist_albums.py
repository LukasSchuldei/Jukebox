import argparse
import logging

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

logger = logging.getLogger('examples.artist_albums')
logging.basicConfig(level='INFO')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="f915aa3054c44257953dfa9b6549c2b4", client_secret="22b951caeb024a12a15089f6fbf737d6"))


# def get_args():
#     parser = argparse.ArgumentParser(description='Gets albums from artist')
#     parser.add_argument('-a', '--artist', required=True,
#                         help='Name of Artist')
#     return parser.parse_args()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


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
    args = "Swift"
    artist = get_artist(args)
    if artist:
        show_artist_albums(artist)
    else:
        logger.error("Can't find artist: %s", artist)


if __name__ == '__main__':
    main()