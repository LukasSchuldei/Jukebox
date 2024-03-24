import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep

scope = "user-read-playback-state,user-modify-playback-state"
spotify_player = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# Shows playing devices
active_devices = spotify_player.devices()
for x in active_devices['devices']:
    print(f"{x['name']} {x['id']}")

#start playback
spotify_player.start_playback(device_id=active_devices['devices'][0]['id'], context_uri='spotify:playlist:37i9dQZF1E39mweBv2LCBw')


