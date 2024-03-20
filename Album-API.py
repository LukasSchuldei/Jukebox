import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
 
#Get the username form the terminal
username = sys.argv[0]
 
#User ID: 12fccf7657324099
#Erase the Cache and promt for user permission

try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)
    
#create spotifyObject

spotifyObject = spotipy.Spotify(auth=token)