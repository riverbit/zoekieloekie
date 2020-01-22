from flask import Flask
from search import *
app = Flask(__name__)

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

aaaa = [[1, 0.3253, "doc1", "De oudste dochter.."], [2, 0.1623, "doc2", "ja dat was een ding"], [3, 0.0815, "doc3", "het verschil was vooral de Deutz.."], [5, 0.0227, "doc5", "en tot slot"]]

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/results', methods=['POST'])
def results():
    return render_template('results.html', query = request.form["query"], results = aaaa)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.config['DEBUG'] = True
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.run()