from flask import Flask, render_template, request, jsonify
from run_wsi_tif import mescnn_function

app = Flask(__name__)

@app.route('/')
def home():
    # Utilisez render_template pour servir votre fichier HTML
    return render_template('index.html')

@app.route('/mescnn')
def run_mescnn():
    mescnn_function()
    return 'MESCnn run complete!'

#TEST pour les fetchs 
@app.route('/test', methods=['POST'])
def test():
    test = request.json['test']
    return jsonify({'test': test})

if __name__ == '__main__':
    app.run(debug=True)
    
