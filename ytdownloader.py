import yt_dlp
import os

download_folder = "downloads"

url = "https://www.youtube.com/watch?v=0QPq041UhkQ"

ydl_opts = {
    'format': 'best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'noplaylist': True
}
with yt_dlp.YoutubeDL({'quite': True}) as ydl:
    info = ydl.extract_info(url, download=False)
    video_title = info['title']
    file_path = os.path.join(download_folder, f"{video_title}.mp4")

if os.path.exists(file_path):
    print(f"Ez a videó már le van töltve: {file_path}")
else:
    print("A videó még nincs letöltve, elkezdem a letöltést...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    print(f"A videó sikeresen letöltve: {file_path}")