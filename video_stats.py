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


def extract_video_data(video_ids):
    extracted_data = []

    # function to split list of video ids into batches for use in building API url
    def batch_list(video_id_list, batch_size):
        for videoid in range(0,len(video_id_list),batch_size): # for a given range (index in video_id_list + 50)
            yield video_id_list[videoid: videoid + batch_size] # give me back the chunk of the video_id_list
            # yield instead of return so that the function can pick up from where it left off each time it is run in a loop below

    try:
        for batch in batch_list(video_ids, MAX_RESULTS):
            video_ids_str = ",".join(batch)

            url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}'

            # make api request
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']

                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount": statistics.get('viewCount', None),
                    "likeCount": statistics.get('likeCount', None),
                    "commentCount": statistics.get('commentCount', None)
                }

                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e
    

if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_video_data(video_ids)