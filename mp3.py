from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def convert_video_to_mp3(video_path, output_path):
    # تحويل الفيديو إلى ملف صوتي
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_path)
    video.close()
    print("تم تحويل الفيديو إلى MP3 بنجاح!")
