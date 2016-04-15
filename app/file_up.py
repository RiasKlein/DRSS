import os
from flask import flash, Flask, request, redirect, url_for, render_template
from flask import send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = './'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'DRSS is pronounced duhhrs'
app.run("localhost", 8000, debug = True)
