import spotipy
from spotipy.oauth2 import SpotifyOAuth


scope = "user-modify-playback-state,playlist-modify-private,playlist-modify-public,user-read-currently-playing,user-read-playback-state"
sp_add_track = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

def add_song_to_queue(object_uri):

        #add song to playlist
        
        sp_add_track.add_to_queue(uri=selected_track_uri)
        sp_add_track.playlist_add_items(playlist_id='3ssDReXf4bPQZpc3J39YQc', items=[selected_track_uri])
        return True

def print_queue():
    scope = "user-read-playback-state"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
    
    current_playback = sp.queue()
    if current_playback is not None and 'queue' in current_playback:
        queue_items = current_playback['queue']
        print("Songs in the queue:")
        for index, track in enumerate(queue_items):
            print(f"{index+1}. {track['name']} -- by {track['artists'][0]['name']}")
    else:
        print("No songs in the queue.")
    
def search_track():
    #get search input
    track_search_input = input("Bitte gebe ein Lied ein, dass du zur Queue hinzufügen willst: ")
    #search for track

    track_result=sp_add_track.search(q=track_search_input, limit=10, type='track', market='DE')
    #output options
    for index, track in enumerate(track_result['tracks']['items']):
        print(f"{index+1}. {track['name']} -- by {track['artists'][0]['name']}")
    #get user selection
    try: 
        track_selection= int(input("Wähle einen Track aus, fürs Abbrechen gebe X ein! "))-1
        selected_track_uri=track_result['tracks']['items'][track_selection]['uri']
        print(f"Hinzugefügt: {track_result['tracks']['items'][track_selection]['name']}")
        
    #cancel 
    except ValueError:
        
            print("Kein Song ausgewählt")
            return None

    return selected_track_uri
    
add_more_songs= True
while add_more_songs:
    selected_track_uri=search_track()
    if selected_track_uri is not None:
        add_song_to_queue(selected_track_uri)
    try: 
        menu_input= int(input("Willst du noch einen Song hinzufügen? (1 ist Ja) "))
        if menu_input!=1:
            add_more_songs=False
    except ValueError:
        add_more_songs=False
print_queue()