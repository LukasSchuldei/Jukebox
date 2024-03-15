#müsst ihr eventuell runterladen vorher!!
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
load_dotenv()

#setup request
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    
    #encode request
    auth_string = client_id + ":" + client_secret
    auth_bytes =auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url ="https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers =headers, data=data)
    #check for error in result
    if result.status_code != 200:
        print("Error:", result.status_code)
        return None
    #convert json
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer "+ token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers =get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1&market=DE"

    query_url= url + query
    result= get(query_url, headers =headers)
    if result.status_code != 200:
        print("Error:", result.status_code)
        return None
    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result) ==0:
        print("No artist found")
        return None

    
    return json_result[0]
    

#get list of top 10 artist_top_songs    
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=DE"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code != 200:
        print("Error:", result.status_code)
        return None
    json_result = json.loads(result.content)["tracks"]
    return json_result
    
    
def search_for_song(token, song_name):
    url = "https://api.spotify.com/v1/search"
    headers =get_auth_header(token)
    query = f"?q={song_name}&type=track&limit=5&market=DE"

    query_url= url + query
    result= get(query_url, headers =headers)
    if result.status_code != 200:
        print("Error:", result.status_code)
        return None
    json_result = json.loads(result.content)["tracks"]
    
    if len(json_result) ==0:
        print("No song found")
        return None
    
    return json_result
    
    
#get token    
token = get_token()
#artist suchen
result=search_for_artist(token, "BHZ")
print(result["name"])
artist_id = result["id"]
#top songs requesten
artist_top_songs = get_songs_by_artist(token, artist_id)
#top songs ausgeben
for idx, song in enumerate(artist_top_songs):
    print(f"{idx+1}. {song['name']}")
#nach song suchen    
songs = search_for_song(token, "Lieblingsworte  ")
#songs ausgeben, mit namen
if songs is not None:
    for idx, tracks in enumerate(songs["items"]):
        artists = ", ".join(artist["name"] for artist in tracks['album']['artists'])
        print(f"{idx+1}. {tracks['album']['name']}, by {artists}")
    