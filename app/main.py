from flask import Flask, requests

app = Flask(__name__)

@app.route("/")
def home():
    request  = requests.get()