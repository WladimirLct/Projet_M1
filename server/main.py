import os
import random
from utils import *

from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO, join_room, leave_room

from werkzeug.utils import secure_filename
from run_wsi_tif import mescnn_function


app = Flask(__name__)
socketio = SocketIO(app, debug=True, cors_allowed_origins='*')

# Set the static folder to the 'client' folder
app._static_folder = os.path.abspath("./static/")


class ProcessInfo:
    in_progress = False
    file_name = None
    time = None
    crop_amount = None
    classification_csv = []
    selected_crops = []
    histogram = {}
    score = {}

process_data = ProcessInfo()


@app.route('/')
def home():
    return render_template('index.html', errored=False)

@app.route('/errored')
def errored():
    return render_template('index.html', errored=True)

currently_analyzing = False
@socketio.on('process_img')
def process_img():
    global currently_analyzing
    if currently_analyzing:
        socketio.emit('message', {"text": 'Already processing an image...', "step": -1}, room=request.sid)
        return
    
    currently_analyzing = True
    mescnn_function(socketio, request.sid, process_data)
    currently_analyzing = False


@app.route('/results')
def results():
    if (process_data.file_name != None):
        select_crops()
        return render_template('results.html',
            score=process_data.score,
            file_name=process_data.file_name, 
            processing_time=process_data.time,
            crop_amount=process_data.crop_amount,
            selected_crops=process_data.selected_crops,
            is_empty=False
        )
    else:
        return render_template('results.html', is_empty=True)
    
@app.route('/about')
def about():
    return render_template('about.html')


def select_crops():
    csv = process_data.classification_csv
    # Convert M-bin, E-bin, S-bin and C-bin to integers
    csv['M-bin'] = csv['M-bin'].astype('int'); csv['E-bin'] = csv['E-bin'].astype('int');
    csv['S-bin'] = csv['S-bin'].astype('int'); csv['C-bin'] = csv['C-bin'].astype('int');
    
    # Keep only crops that have any of their M-bin, E-bin, S-bin or C-bin = 1
    selected_crops = csv[(csv['M-bin'] == 1) | (csv['E-bin'] == 1) | (csv['S-bin'] == 1) | (csv['C-bin'] == 1)]

    # Shuffle the dataframe
    selected_crops = selected_crops.sample(frac=1)
    selected_crops = selected_crops.head(6)

    # Only keep the filename and what bins are 1
    selected_crops = selected_crops[['filename', 'M-bin', 'E-bin', 'S-bin', 'C-bin']]

    # Only keep the final part of the filename
    selected_crops['filename'] = selected_crops['filename'].map(lambda x: x.split('/')[-1])

    # If the file has M-bin, set it's column "detected" to "M" etc
    selected_crops['detected'] = selected_crops.apply(detect_crop, axis=1)

    # Only keep the filename and detected columns
    selected_crops = selected_crops[['filename', 'detected']]
    
    # Convert the dataframe to a list of dictionaries
    selected_crops = selected_crops.to_dict(orient='records')
    process_data.selected_crops = selected_crops


@app.route('/hist')
def hist():
    return {'hist': process_data.histogram}


files_path = "./current-files/"
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    # If there is a process in progress, return an error
    if process_data.in_progress:
        return 'There is already a process in progress', 400
    
    if file:
        # Check if there is already a file in the folder
        files = os.listdir(files_path)

        # Remove the file(s) in the folder
        for f in files:
            # if (".zip" not in f):
            os.remove(files_path + f)

        filename = secure_filename(file.filename)
        file.save(os.path.join(files_path, filename))

        return 'Started analyzing the image', 200
    return 'Error while saving the file', 400


@app.route('/waiting', methods=['GET'])
def waiting():
    return render_template('waiting.html')


tiles_dir = './Data/Export/cascade_R_50_FPN_3x/Temp/tiler-output/Tiles/'
@app.route('/tiles')
def send_tiles():
    wsi_path = os.listdir(tiles_dir)[0] + '/'
    tiles = os.listdir(tiles_dir + wsi_path)

    random.shuffle(tiles)
    tiles = tiles[:10]
    
    for i in range(len(tiles)):
        tiles[i] = "/get_tile/" + tiles[i]
    return {'result': tiles}


@app.route('/get_tile/<tile>')
def get_tile(tile):
    wsi_path = os.listdir(tiles_dir)[0] + '/'
    return send_file(tiles_dir + wsi_path + tile)


masks_dir = './Data/Export/cascade_R_50_FPN_3x/Temp/segment-output/Masks/'
@app.route('/masks')
def send_masks():
    wsi_path = os.listdir(masks_dir)[0] + '/'
    masks = os.listdir(masks_dir + wsi_path)

    random.shuffle(masks)
    masks = masks[:10]
    
    for i in range(len(masks)):
        masks[i] = "/get_mask/" + masks[i]
    return {'result': masks}


@app.route('/get_mask/<mask>')
def get_mask(mask):
    wsi_path = os.listdir(masks_dir)[0] + '/'
    return send_file(masks_dir + wsi_path + mask)


crops_dir = './Data/Export/cascade_R_50_FPN_3x/Temp/json2exp-output/Crop-256/'
@app.route('/crops')
def send_crops():
    wsi_path = os.listdir(crops_dir)[0] + '/'
    crops = os.listdir(crops_dir + wsi_path)

    random.shuffle(crops)
    crops = crops[:10]
    
    for i in range(len(crops)):
        crops[i] = "/get_crop/" + crops[i]
    return {'result': crops}


@app.route('/get_crop/<crop>')
def get_crop(crop):
    wsi_path = os.listdir(crops_dir)[0] + '/'
    return send_file(crops_dir + wsi_path + crop)


full_crops_dir = './Data/Export/cascade_R_50_FPN_3x/Temp/json2exp-output/Original/'
@app.route('/get_full_crop/<crop>')
def get_full_crop(crop):
    wsi_path = os.listdir(crops_dir)[0] + '/'
    return send_file(full_crops_dir + wsi_path + crop)


report_dir = "./Data/Export/cascade_R_50_FPN_3x/Report/M-efficientnetv2-m_E-efficientnetv2-m_S-densenet161_C-mobilenetv2"
@app.route('/download/<dl_type>')
def download(dl_type):
    # Switch case of the download type
    if dl_type == 'report':
        wsi_path = os.listdir(report_dir)
        # Remove the file with Oxford in it
        wsi_path = [w for w in wsi_path if 'Oxford' not in w]
        wsi_path = wsi_path[0]
        return send_file(report_dir + "/" + wsi_path)
    elif dl_type == 'crops':
        wsi_path = os.listdir(crops_dir)[0] + '/'
        os.system(f"zip -r {files_path}crops.zip {crops_dir + wsi_path}")
        return send_file(files_path + 'crops.zip')
    

if __name__ == '__main__':
    socketio.run(app)