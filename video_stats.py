import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = 'MrBeast'
MAX_RESULTS = 50

def get_playlist_id():

    try:

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url) # send a get request to url using requests library

        response.raise_for_status() # for exception handling

        data = response.json() # parses response as json

        # print(json.dumps(data, indent=4)) #converts a python object into a json formatted string. indent=4 is a common python convention for readability.
        
        channel_items =  data["items"][0]

        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        print(channel_playlist_id)

        return channel_playlist_id

    except requests.exeptions.RequestException as e:
        raise e



def get_video_ids(playlist_id):
    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults={MAX_RESULTS}&playlistId={playlist_id}&key={API_KEY}"

    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}" #if there is a page token, add it to the url

            # make api request
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            #add video ids to list
            for item in data.get('items',[]): # ensures loop still runs if there is no 'item' key in the 'data' object
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break

        return video_ids
    
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    get_video_ids(playlist_id)