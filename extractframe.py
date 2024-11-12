import cv2
import os
from datetime import timedelta
from pathlib import Path

from download import get_video_title

video_title = get_video_title(os.getenv('youtube_url'))


def extract_frames_per_second(video_path):
    """
    Extract one frame per second from a video with detailed timestamp filenames
    Output folder structure will be: /data/video_name/frame
    
    Args:
        video_path (str): Path to the video file
    """
    # Get video name without extension
    video_name = Path(video_path).stem
    
    # Create output directory structure: /data/video_name/frame
    output_dir = os.path.join('data', video_title, 'frame')
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Initialize frame count
    frame_id = 0
    frame_count = 0
    
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            break
            
        # Save one frame per 1.5 second
        if frame_id % (int(fps) * 1.5) == 0:
            
                        # Calculate timestamp
            seconds = frame_id / fps
            td = timedelta(seconds=seconds)
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            milliseconds = int((seconds % 1) * 1000)
            
            # Format filename with timestamp
            filename = f"{video_name}_{hours:02d}{minutes:02d}{secs:02d}{milliseconds:03d}.jpeg"
            output_path = os.path.join(output_dir, filename)

            
            # Save frame
            cv2.imwrite(output_path, frame)
            

            
            frame_count += 1
            
        frame_id += 1
    
    # Release video capture
    cap.release()
    print(f"\nExtracted {frame_count} frames to {output_dir}")
    print(f"Format: {video_name}_HHMMSSMMM.jpeg")

# Example usage
if __name__ == "__main__":
    video_path = "your_video.mp4"  # Replace with your video path
    extract_frames_per_second(video_path)