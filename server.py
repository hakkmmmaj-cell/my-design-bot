from fastapi import FastAPI
from fastapi.responses import FileResponse
import yt_dlp, uuid, os

app = FastAPI()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download(url, audio=False):
    file_id = str(uuid.uuid4())
    out = f"{DOWNLOAD_DIR}/{file_id}"

    opts = {
        "quiet": True,
        "noplaylist": True,
        "format": "bestaudio/best" if audio else "bestvideo+bestaudio/best",
        "outtmpl": out + (".mp3" if audio else ".mp4"),
    }

    if audio:
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3"
        }]

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

    return out + (".mp3" if audio else ".mp4")


@app.get("/download")
def download_file(url: str, type: str = "video"):
    file_path = download(url, audio=(type == "audio"))
    return FileResponse(file_path)
