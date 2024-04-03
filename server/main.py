from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Utilisez render_template pour servir votre fichier HTML
    return render_template('IG_MESCnn.html')





if __name__ == '__main__':
    app.run(debug=True)
    