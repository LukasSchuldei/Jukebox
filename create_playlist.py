import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# Shows playing devices
res = sp.devices()
pprint(res)

# Change track
sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'], device_id="e4bf0e37382ea8f723cd1ec0d9871cb146744451")

# Change volume
# sp.volume(80)
# sleep(2)
# sp.volume(30)
# sleep(2)
# sp.volume(80)
# sp.transfer_playback(device_id="c12575cd580701b23a2273d1dbdf0baf34f93921")
# sleep(10)
sp.pause_playback()
song= sp.search(type="track", q="Lieblingsworte", limit="5", market="DE")
items = song['tracks']
pprint(song)
for x in range(0,10):
    print(f"{song['album']['name']}")