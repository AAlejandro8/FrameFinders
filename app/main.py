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

def get_movies_with_genre(movies):
      genres = "https://api.themoviedb.org/3/genre/movie/list"
      response = requests.get(genres, headers=headers)
      genre_id_list = response.json()["genres"]
      
      # map genre ids to genre names
      genre_map = {genre["id"]: genre["name"] for genre in genre_id_list}
      
      movie_result = movies.json()["results"]

      # add genre names to each movie
      for movie in movie_result:
            movie_genre_ids = movie.get("genre_ids", [])
            movie["genre_names"] = [genre_map.get(genre_id, "Unknown") for genre_id in movie_genre_ids]

      return movie_result
      
app = Flask(__name__)

@app.route("/",methods = ["GET", "POST"])
def home():
      trending = get_trending_movies()
      movies_with_genre = get_movies_with_genre(trending)
      
      return render_template("index.html",
                             movies=movies_with_genre)

@app.route("/search", methods = ["GET"])
def search():
      query = request.args.get("q", "")
      url = f'https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page=1'
      response = requests.get(url, headers=headers)
      movies = get_movies_with_genre(response)
      
      return render_template("search.html", 
                             movies=movies)
