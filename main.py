
#%% First cell
import os
import importlib
importlib.reload(os)
#%% download video and transcript

import download 
importlib.reload(download)

video_path, transcript_path, video_title = download.download_video_and_transcript(os.getenv('youtube_url'))



# %% frame extraction
import extractframe
importlib.reload(extractframe)
from extractframe import extract_frames_per_second

extract_frames_per_second(video_path)


# %% chat with images
import importlib  # Add this import at the top
import llm_chat
importlib.reload(llm_chat)

folder_path = os.path.join('data', video_title, 'frame')
question = "did they kiss "
llm_chat.chat_with_images(folder_path, transcript_path, question)


# %%
