import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO
import requests
from time import sleep

# Initialize Tkinter
root = tk.Tk()
root.title("Currently Playing Track")

# Spotify authentication
scope = "user-read-playback-state"
spotify_player = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# Function to update currently playing track and album art
# gets the Spotify class 
def update_current_track(current_track):
    
    if current_track: # if its not zero
        global prev_track_id # global variable, not pretty maybe change
        prev_track_id= spotify_player.current_user_playing_track()['item']['album']['id']# sets global variable
        
        #changes labels displayed
        track_name = current_track['item']['name']
        album_name = current_track['item']['album']['name']
        album_image_url = current_track['item']['album']['images'][0]['url']
        
        # Download album art
        response = requests.get(album_image_url)
        if response.status_code == 200:
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = ImageTk.PhotoImage(img)
            image_label.configure(image=img)
            image_label.image = img  # Keep a reference to prevent garbage collection
            text_widget.image_create(tk.END, image=img)
        # Update track information label
        track_info_label.config(text=f"Track: {track_name}\nAlbum: {album_name}")
    else:
        track_info_label.config(text="No track currently playing")
    

#check, if update is needed
def check_new_track():
    global prev_track_id # import global variable
    
    current_track = spotify_player.current_user_playing_track()
    if current_track is not None:
        current_track_id= current_track['item']['album']['id']
    
        if current_track_id != prev_track_id: # compares track ids
            update_current_track(current_track)
    root.after(1000, check_new_track)  # Schedule the function to run again after 1 second
    
# Create labels for track information and album art
track_info_label = tk.Label(root, text="Waiting for track info...")
track_info_label.pack()

image_label = tk.Label(root)
image_label.pack()

text_widget = tk.Text(root, bg="black", fg="white", font=("Courier", 12))
text_widget.pack(fill="both", expand=True)

# Insert text and images into the text widget
text_widget.insert(tk.END, "Hello, world!\n")

# Start the function to update track information
prev_track_id =''
update_current_track(spotify_player.current_user_playing_track())# sets image in the beginning
check_new_track() # self calling fuction

# Start the Tkinter event loop, contiues for ever
root.mainloop()


#TODO
    #implement text widget
    #show first five songs of queue
    #how to kill process and restart
        #interuption/pause of main loop
        
# # Create text widget to mimic terminal
# text_widget = tk.Text(root, bg="black", fg="white", font=("Courier", 12))
# text_widget.pack(fill="both", expand=True)

# # Insert text and images into the text widget
# text_widget.insert(tk.END, "Hello, world!\n")
# text_widget.image_create(tk.END, image=)
