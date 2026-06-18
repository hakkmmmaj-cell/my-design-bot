from moviepy.editor import *
import os

def convert_to_mp3(video_path, output_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_path)
    video.close()
