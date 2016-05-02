from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "DRSS is pronounced duhrss"
from app import views
