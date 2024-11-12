import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import os
from urllib.parse import parse_qs, urlparse

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    query = parse_qs(urlparse(url).query)
    return query["v"][0] if "v" in query else url.split("/")[-1]

def get_video_title(url):
    """Get video title to use as folder name"""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # Clean the title to be filesystem-friendly
        title = "".join(c for c in info['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        return title

def download_video(url, video_folder):
    """Download YouTube video (max 720p) and return the video file path"""
    ydl_opts = {
        'format': 'best[height<=720]',
        'outtmpl': os.path.join(video_folder, '%(title)s.%(ext)s'),
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            # Get the actual filename that yt-dlp used
            video_path = os.path.join(video_folder, f"{info['title']}.{info['ext']}")
            print("Video downloaded successfully!")
            return video_path
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None

def download_transcript(url, video_folder, video_title):
    """Download English transcript and return the transcript file path"""
    try:
        video_id = get_video_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        # Create filename from video title  
        transcript_path = os.path.join(video_folder, f"{video_title}_transcript.txt")
        
        # Write transcript to file
        with open(transcript_path, 'w', encoding='utf-8') as f:
            for entry in transcript:
                f.write(f"[{entry['start']:.2f}s] {entry['text']}\n")
        
        print("Transcript downloaded successfully!")
        return transcript_path
    except Exception as e:
        print(f"Error downloading transcript: {str(e)}")
        return None

def download_video_and_transcript(url):
    """
    Download video and transcript, return tuple of (video_path, transcript_path)
    Returns (None, None) if either download fails
    """
    # Get video title to use as folder name
    video_title = get_video_title(url)
    
    # Create base downloaded directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Create video-specific folder
    video_folder = os.path.join('data', video_title)
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
        
    # Download video and transcript to the video-specific folder
    video_path = download_video(url, video_folder)
    transcript_path = download_transcript(url, video_folder, video_title)
    
    return video_path, transcript_path, video_title