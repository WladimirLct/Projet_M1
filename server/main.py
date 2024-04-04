import os
import threading
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from run_wsi_tif import mescnn_function

app = Flask(__name__)

# Set the static folder to the 'client' folder
app._static_folder = os.path.abspath("./static/")
print(os.path.abspath("./static/"))

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
        threading.Thread(target=run_mescnn, args=('./current-file/' + filename,)).start()
        return 200
    return 400
    
    
if __name__ == '__main__':
    app.run(debug=True)