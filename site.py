from flask import Flask
app = Flask(__name__)

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/results', methods=['POST'])
def results():
    return "This is a placeholder"

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.config['DEBUG'] = True
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.run()