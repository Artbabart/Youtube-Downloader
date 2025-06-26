from flask import Flask, request, jsonify, render_template, send_file
import yt_dlp
from io import BytesIO
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ytdownloaderfront.html')

@app.route('/download', methods=['POST'])
def download_video():
    print(">>> /download endpoint meghívva")
    data = request.json
    print(">>> Received data:", data)
    url = data.get('url')

    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'cookiefile': 'cookies.txt',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0',
                }
            }

        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        with open(filename,'rb') as f:
            file_data = BytesIO(f.read())

        file_data.seek(0)
        download_name = os.path.basename(filename)

        return send_file(
                file_data,
                as_attachment=True,
                download_name=download_name,
                mimetype='video/mp4'
            )

    except Exception as e:
        print(">>> Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
