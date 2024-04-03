from flask import Flask, render_template
from run_wsi_tif import mescnn_function

app = Flask(__name__)

@app.route('/')
def home():
    # Utilisez render_template pour servir votre fichier HTML
    return render_template('IG_MESCnn.html')

@app.route('/mescnn')
def run_mescnn():
    mescnn_function()
    return 'MESCnn run complete!'



if __name__ == '__main__':
    app.run(debug=True)
    
