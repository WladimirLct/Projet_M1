import os
import multiprocessing

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from werkzeug.utils import secure_filename
from run_wsi_tif import mescnn_function

app = Flask(__name__)
socketio = SocketIO(app, debug=True, cors_allowed_origins='*')

# Set the static folder to the 'client' folder
app._static_folder = os.path.abspath("./static/")

users = []
@socketio.on('connect')
def add_list():
    users.append(request.sid)
    join_room(request.sid)
    print('User connected:', request.sid)


@socketio.on('disconnect')
def remove_list():
    users.remove(request.sid)
    leave_room(request.sid)
    print('User disconnected:', request.sid)


@socketio.on('process_img')
def process_img():
    mescnn_function(socketio, request.sid)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/mescnn')
def run_mescnn(path=None):
    mescnn_function(path)
    return 'MESCnn run complete!'


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    if file:
        # Check if there is already a file in the folder
        files = os.listdir('./current-file/')

        # Remove the file(s) in the folder
        for f in files:
            os.remove('./current-file/' + f)

        filename = secure_filename(file.filename)
        file.save(os.path.join('./current-file/', filename))

        return 'Started analyzing the image', 200
    return 'Error while saving the file', 400


@app.route('/waiting', methods=['GET'])
def waiting():
    return render_template('waiting.html')


if __name__ == '__main__':
    socketio.run(app)