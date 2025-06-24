from flask import Flask, request, jsonify, render_template
import yt_dlp
import os # imports

app = Flask(__name__)
download_folder = "downloads" # create downloads folder
os.makedirs(download_folder, exist_ok=True)

@app.route('/')
def index():
    return render_template('ytdownloaderfront.html')  # load in the ytdownloaderfront.html

@app.route('/download', methods=['POST'])
def download_video():
    print(">>> /download endpoint meghívva")
    data = request.json
    print(">>> Received data:", data)
    url = data.get('url')

    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info['title']
            file_path = os.path.join(download_folder, f"{video_title}.mp4")

        if os.path.exists(file_path):
            return jsonify({'message': 'This video is already downloaded.', 'path': file_path})

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_folder, '%(id)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            },
            'cookiefile': 'getcookies.txt'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({'message': 'Finish.', 'path': file_path})

    except Exception as e:
        print(">>> Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
