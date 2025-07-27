import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import time

def create_app():
    app = Flask(__name__)

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            if 'file' not in request.files:
                return "No file part in the request", 400
            file = request.files['file']
            if file.filename == '':
                return "No selected file", 400
            if not file.filename.lower().endswith('.mp3'):
                return "Only MP3 files are allowed", 400
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('index'))

        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            upload_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(file_path)))
            files.append({'name': filename, 'time': upload_time})
        return render_template('index.html', files=files)
    
    @app.route('/download/<filename>', methods=['GET'])
    def download_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

    @app.route('/delete/<filename>', methods=['POST'])
    def delete_file(filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        return redirect(url_for('index'))
            
    return app