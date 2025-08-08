import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, jsonify
import time

def create_app():
    app = Flask(__name__)

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST' and 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return "No selected file", 400
            if not file.filename.lower().endswith('.mp3'):
                return "Only MP3 files are allowed", 400
            # Find latest episode folder
            latest_episode_file = os.path.join(app.config['UPLOAD_FOLDER'], 'latest_episode.txt')
            if os.path.exists(latest_episode_file):
                with open(latest_episode_file, 'r') as f:
                    episode_folder = f.read().strip()
                episode_path = os.path.join(app.config['UPLOAD_FOLDER'], episode_folder)
            else:
                # If no episode, create a default one
                episode_path = app.config['UPLOAD_FOLDER']
            file.save(os.path.join(episode_path, file.filename))
            return redirect(url_for('index'))
        episodes = []
        for folder in sorted(os.listdir(app.config['UPLOAD_FOLDER'])):
            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
            if os.path.isdir(folder_path):
                files = []
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    upload_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(file_path)))
                    files.append({'name': filename, 'time': upload_time})
                episodes.append({
                    'number': folder.split(' ')[0],
                    'title': ' '.join(folder.split(' ')[2:]),
                    'folder': folder,  # Add this line
                    'files': files
                })
        return render_template('index.html', episodes=episodes)
    
    @app.route("/api")
    def serve_api():
        audio_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(('.mp3'))]
        audio_count = len(audio_files)

        return jsonify({
            "audio_count": audio_count,
        })
    
    @app.route('/download/<episode>/<filename>', methods=['GET'])
    def download_file(episode, filename):
        episode_path = os.path.join(app.config['UPLOAD_FOLDER'], episode)
        return send_from_directory(episode_path, filename, as_attachment=True)

    @app.route('/delete/<episode>/<filename>', methods=['POST'])
    def delete_file(episode, filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], episode, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        return redirect(url_for('index'))
    
    @app.route('/create_episode', methods=['POST'])
    def new_episode():
        title = request.form['title']
        episodes = [d for d in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], d))]
        next_number = len(episodes) + 1
        folder_name = f"{next_number:02d} - {title}"
        episode_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        os.makedirs(episode_path, exist_ok=True)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'latest_episode.txt'), 'w') as f:
            f.write(folder_name)
        return redirect(url_for('index'))
            
    return app