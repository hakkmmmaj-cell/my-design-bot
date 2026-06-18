from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def convert_to_mp3(video_path, output_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_path)
    video.close()
