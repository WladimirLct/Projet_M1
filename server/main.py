import os
import multiprocessing

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

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
    print('User connected:', request.sid)

@socketio.on('disconnect')
def remove_list():
    users.remove(request.sid)
    print('User disconnected:', request.sid)

waiting_list = []
@socketio.on('match_id')
def match_id(data):
    waiting_list.append({"origin": data['sid'], "dest": request.sid})
    print('Match IDs:', data['sid'], request.sid)

@app.route('/')
def home():
    # Utilisez render_template pour servir votre fichier HTML
    return render_template('index.html')

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

        # Run the MESCnn function
        p = multiprocessing.Process(target=mescnn_function, args=('./current-file/' + filename,))
        p.start()
        return 'Started analyzing the image', 200
    return 'Error while saving the file', 400

@app.route('/waiting', methods=['GET'])
def waiting():
    # Get the sid send in the url
    sid = request.args.get('sid')
    # Return the template waiting.html with the sid
    return render_template('waiting.html', socketid=sid)

if __name__ == '__main__':
    socketio.run(app)