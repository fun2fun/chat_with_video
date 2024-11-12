# YouTube Video Analysis Tool

This tool allows you to download YouTube videos, extract their transcripts, capture frames at regular intervals, and analyze the content using Claude 3 AI. The project is particularly useful for detailed video content analysis and understanding.

## Features

- Download YouTube videos (maximum 720p quality)
- Extract English transcripts
- Capture frames at 1.5-second intervals
- Analyze video content using Claude 3 AI
- Organized file structure for each video

## Prerequisites

Make sure you have the following dependencies installed:

```bash
pip install yt-dlp youtube-transcript-api opencv-python anthropic
```

You'll also need to set up your Anthropic API key as an environment variable:

```bash
export Anthropic_API_KEY="your-api-key"
```

## Project Structure

```
.
├── download.py          # Handles video and transcript downloads
├── extractframe.py      # Manages frame extraction from videos
├── llm_chat.py         # Implements Claude AI integration
├── main.py             # Main script orchestrating the workflow
└── data/               # Directory for stored videos and processed data
    └── [video_title]/  # Individual video directories
        ├── video file
        ├── transcript
        └── frame/      # Extracted frames
```

## Usage

1. Set the YouTube URL as an environment variable:
```bash
export youtube_url="https://www.youtube.com/watch?v=your-video-id"
```

2. Run the main script:
```python
python main.py
```

## Module Details

### download.py
- `get_video_id(url)`: Extracts video ID from YouTube URL
- `get_video_title(url)`: Gets video title for folder naming
- `download_video(url, video_folder)`: Downloads video (max 720p)
- `download_transcript(url, video_folder, video_title)`: Downloads English transcript
- `download_video_and_transcript(url)`: Main function orchestrating download process

### extractframe.py
- `extract_frames_per_second(video_path)`: Extracts frames every 1.5 seconds
- Saves frames with timestamp-based filenames (format: videoname_HHMMSSMMM.jpeg)

### llm_chat.py
- `create_image_content(image_path)`: Prepares images for Claude API
- `process_images_with_transcript(folder_path, transcript_path, question)`: Processes images and transcript
- `chat_with_images(folder_path, transcript_path, question)`: Interfaces with Claude AI

## Output Structure

For each video, the tool creates a directory structure:
```
data/
└── [Video Title]/
    ├── [video_file].[ext]
    ├── [video_title]_transcript.txt
    └── frame/
        └── [video_name]_HHMMSSMMM.jpeg
```

## Features and Limitations

- Video quality is limited to 720p to manage file sizes
- Supports English transcripts only
- Frames are extracted every 1.5 seconds
- Uses Claude 3 Sonnet model with a 1024 token limit
- File names are sanitized to be filesystem-friendly

## Error Handling

The tool includes error handling for:
- Failed video downloads
- Missing transcripts
- Frame extraction issues
- API communication errors

## Environment Variables Required

- `youtube_url`: URL of the YouTube video to process
- `Anthropic_API_KEY`: Your Anthropic API key for Claude AI integration

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Add your chosen license here]
