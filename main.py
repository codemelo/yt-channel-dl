import yt_dlp
import subprocess
import os

def get_all_video_urls(channel_url):
    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        video_entries = info['entries']
    
    # Sort by upload date (oldest first)
    video_entries.sort(key=lambda entry: entry.get('upload_date', ''))

    video_urls = [{'url': entry['url'], 'id': entry['id']} for entry in video_entries]
    
    # Reverse the order of the video_urls collection
    video_urls.reverse()

    return video_urls

def download_videos(video_urls):
    # Create download directory if it doesn't exist
    download_dir = 'download'
    os.makedirs(download_dir, exist_ok=True)

    for idx, video in enumerate(video_urls, start=1):
        url = video['url']
        video_id = video['id']
        # Define the output filename template within the download directory
        output_template = os.path.join(download_dir, f'{idx}. %(title)s [{video_id}].%(ext)s')
        
        # Construct the yt-dlp command
        command = ['yt-dlp', '-o', output_template, url]
        
        # Execute the yt-dlp command
        subprocess.run(command)
        
        print(f"Downloaded {idx}. {url}")

# Replace with the URL of the YouTube channel you want to scrape
channel_url = 'https://www.youtube.com/{channel}/videos'
video_urls = get_all_video_urls(channel_url)

# Download the videos
download_videos(video_urls)
