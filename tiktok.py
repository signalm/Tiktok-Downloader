import requests
import json
import re
import os
from art import *

# Made by https://github.com/signalm/

def extract_numbers_from_url(url):
    numbers = re.findall(r'\d+', url)
    return [int(num) for num in numbers]

def getnamett(url):
    print("Starting")
    orgURL = 'https://www.tiktok.com/oembed?url=' + url

    r = requests.get(url=orgURL)

    if r.status_code != 200:
        print("Failed to retrieve video information.")
        return

    data = json.loads(r.text)
    
    title = data.get("title")
    print("Video Title: " + title)
    
    author_name = data.get("author_name")
    print("Author: " + author_name)

    thumbnail_url = data.get("thumbnail_url")
    print("Thumbnail: " + thumbnail_url)

    print("Download video (Y/N)?")
    response = input().strip().lower()
    if response == "y":
        print(f"Downloading {title} by {author_name}")
        video_id = max(extract_numbers_from_url(url))
        print(f"Video ID: {video_id}")
        
        # Replace the below URL with the correct one for downloading videos
        video_download_url = f"https://tikcdn.io/ssstik/{video_id}"
        vid = requests.get(video_download_url, stream=True)
        
        if vid.status_code != 200 or 'content-length' not in vid.headers or int(vid.headers['content-length']) == 0:
            print("Could not download the video by " + author_name)
            return

        print("Enter the directory to download the file (leave blank for current directory)")
        filedir = input().strip()
        if filedir == "":
            filedir = os.curdir
        else:
            if not filedir.endswith(os.sep):
                filedir += os.sep

        print("What would you like to call the file name?")
        filename = input().strip()
        if filename == "":
            print("Please enter a file name")
            filename = input().strip()

        filepath = os.path.join(filedir, filename + ".mp4")
        with open(filepath, 'wb') as file:
            for chunk in vid.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Video downloaded successfully as {filepath}")
    elif response == "n":
        exit(0)
    else:
        print("Invalid input")


tprint("Tiktok  Downloader")

print("Enter the TikTok video URL you would like to download!")
theurl = input().strip()
getnamett(theurl)