from fastapi import FastAPI
from fastapi.responses import FileResponse
import yt_dlp, uuid, os

app = FastAPI()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_file(url):
    file_id = str(uuid.uuid4())
    out = f"{DOWNLOAD_DIR}/{file_id}.mp4"

    ydl_opts = {
        "format": "best",
        "outtmpl": out,
        "noplaylist": True,
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "retries": 5
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return out


@app.get("/download")
def download(url: str):
    try:
        file_path = download_file(url)
        return FileResponse(file_path, media_type="video/mp4")

    except Exception as e:
        print("SERVER ERROR:", e)
        return {"error": "download failed"}
