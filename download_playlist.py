# import subprocess
# import sys

# subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
import yt_dlp
import json
import sys
import requests
import re



def get_channel_id(channel_url):
    # Just extract the channel_id from the channel URL using yt-dlp's metadata extraction,
    # no need to fetch any playlist items or videos.
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'verbose': True,
        'progress': True,
        'yes_playlist': True,
        'playlist_items': '1',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        return info.get('channel_id')



def get_all_channel_video_details(uploads_playlist_url, limit=None):

    channel_id = get_channel_id(uploads_playlist_url)
    print(channel_id)

    uploads_playlist_id = f"https://www.youtube.com/playlist?list={'UU' + channel_id[2:]}"
    print(uploads_playlist_id)

    ydl_opts = {
        'quiet': False,
        'verbose': True,
        'extract_flat': True,
        'skip_download': True,
        'yes_playlist': True,
        'playlist_items': limit,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(uploads_playlist_id, download=False)
    return playlist_info
 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_playlist.py <channel_url>")
        sys.exit(1)
    channel_url = sys.argv[1]
    if len(sys.argv) > 2:
        limit = int(sys.argv[2])
    else:
        limit = None
    playlist_info = get_all_channel_video_details(channel_url, limit)
    # Save to JSON file
    output_file = "uploads_playlist_videos.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(playlist_info, f, indent=2, ensure_ascii=False)
    # print(json.dumps(videos, indent=2, ensure_ascii=False))
    
