from flask import Flask, request, jsonify, render_template
import os
import requests

api_key = os.environ["TMD_API_KEY"]
read_key = os.environ["TMD_READ_ACCESS_KEY"]
headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {read_key}"
      }

def get_trending_movies():
      url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"
      response = requests.get(url, headers=headers)
      return response
      
app = Flask(__name__)

@app.route("/",methods = ["GET", "POST"])
def home():
      trending = get_trending_movies()
      
      return render_template("index.html", movies=trending.json()["results"])