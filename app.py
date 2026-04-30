from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')

    if not url:
        return jsonify({"error": "تکایە لینکێک دابنێ"}), 400

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            title = info.get('title', 'Video')

            if 'formats' in info:
                formats = info['formats']
                best = None

                for f in formats[::-1]:
                    if f.get('ext') == 'mp4' and f.get('url'):
                        best = f
                        break

                if not best:
                    best = formats[-1]

                download_url = best.get('url')
            else:
                download_url = info.get('url')

            return jsonify({
                "title": title,
                "download_url": download_url
            })

    except Exception as e:
        print(e)
        return jsonify({"error": "هەڵەیەک ڕوویدا"}), 500


if __name__ == '__main__':
    app.run()