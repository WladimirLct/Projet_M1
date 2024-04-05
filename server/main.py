import os
import random
import multiprocessing

from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO, join_room, leave_room

from werkzeug.utils import secure_filename

# from run_wsi_tif import mescnn_function
def mescnn_function(socketio, sid):
    return 0

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

@app.route('/tiles')
def send_tiles():
    tiles = os.listdir('./Data/Export/cascade_R_50_FPN_3x/Temp/tiler-output/Tiles/C2321120-1-A-PAS/')

    random.shuffle(tiles)
    tiles = tiles[:10]
    
    for i in range(len(tiles)):
        tiles[i] = "/get_tile/" + tiles[i]
    return {'result': tiles}

@app.route('/get_tile/<tile>')
def get_tile(tile):
    return send_file('./Data/Export/cascade_R_50_FPN_3x/Temp/tiler-output/Tiles/C2321120-1-A-PAS/' + tile)


@app.route('/masks')
def send_masks():
    masks = os.listdir('./Data/Export/cascade_R_50_FPN_3x/Temp/segment-output/Masks/C2321120-1-A-PAS/')

    random.shuffle(masks)
    masks = masks[:10]
    
    for i in range(len(masks)):
        masks[i] = "/get_mask/" + masks[i]
    return {'result': masks}

@app.route('/get_mask/<mask>')
def get_mask(mask):
    return send_file('./Data/Export/cascade_R_50_FPN_3x/Temp/segment-output/Masks/C2321120-1-A-PAS/' + mask)


@app.route('/crops')
def send_crops():
    crops = os.listdir('./Data/Export/cascade_R_50_FPN_3x/Temp/json2exp-output/Crop-256/C2321120-1-A-PAS/')

    random.shuffle(crops)
    crops = crops[:10]
    
    for i in range(len(crops)):
        crops[i] = "/get_crop/" + crops[i]
    return {'result': crops}

@app.route('/get_crop/<crop>')
def get_crop(crop):
    return send_file('./Data/Export/cascade_R_50_FPN_3x/Temp/json2exp-output/Crop-256/C2321120-1-A-PAS/' + crop)


@app.route('/mescnn')
# def run_mescnn(path=None):
#     mescnn_function(path)
#     return 'MESCnn run complete!'


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