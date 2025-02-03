import yt_dlp

url = "https://youtu.be/cxQxajcOyCI?si=P9nKGFSeGRgk08VD"

ydl_opts = {
    'format': 'best', 
    'outtmpl': 'downloads/%(title)s.%(ext)s', 
    'noplaylist': True
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Letöltés kész!")
