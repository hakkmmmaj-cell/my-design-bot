from moviepy.editor import VideoFileClip
import os

def convert_to_mp3(video_path):
    audio_path = video_path.rsplit(".", 1)[0] + ".mp3"

    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

    clip.close()

    return audio_path
