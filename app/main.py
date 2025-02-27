from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    request = request.get()
    return jsonify(request.json())