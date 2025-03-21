from flask import Flask, request, render_template, url_for, jsonify
import os
import requests
from app import app, db
from app.models import WatchList

# authentication for the API
api_key = os.environ["TMD_API_KEY"]
read_key = os.environ["TMD_READ_ACCESS_KEY"]
headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {read_key}"
      }

# get current trending movies currently, day of.
def get_trending_movies():
      url = "https://api.themoviedb.org/3/trending/movie/week?language=en-US"
      response = requests.get(url, headers=headers)
      return response

# original list doesn have genres listed by name so this gets the ids and assigns them to their genre
def get_movies_with_genre(movies):
      genres = "https://api.themoviedb.org/3/genre/movie/list"
      response = requests.get(genres, headers=headers)
      # ge the id list 
      genre_id_list = response.json()["genres"]
      
      # map genre ids to genre names
      genre_map = {genre["id"]: genre["name"] 
                   for genre in genre_id_list}
      
      movie_result = movies.json()["results"]

      # add genre names to each movie
      for movie in movie_result:
            movie_genre_ids = movie.get("genre_ids", [])
            movie["genre_names"] = [genre_map.get(genre_id, "Unknown") 
                                    for genre_id in movie_genre_ids]

      return movie_result
   
# main page 
@app.route("/", methods = ["GET"])
def home():
      return render_template("homepage.html")


# trending page of the week 
@app.route("/trending", methods=["GET"])
def trending_movies():
      trending = get_trending_movies()
      movies_with_genre = get_movies_with_genre(trending)
      
      return render_template("index.html",
                             movies=movies_with_genre)
                             
# Upcoming
@app.route("/upcoming", methods=["GET"])
def upcoming_movies():
     upcoming = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
     response = requests.get(upcoming,headers=headers)
     upcoming_movies_with_genre = get_movies_with_genre(response)

     return render_template("upcoming.html",
                            movies=upcoming_movies_with_genre)


# searched a movie
@app.route("/search", methods = ["GET"])
def search():
      query = request.args.get("q", "")
      url = f'https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page=1'
      response = requests.get(url, headers=headers)
      movies = get_movies_with_genre(response)
      
      return render_template("search.html", 
                             movies=movies, query=query)

# clicked on a movie for more info
@app.route("/movie/<movie_id>", methods=["GET"])
def movie_info(movie_id):
      # GET THE MOVIE MORE INFO     
      url = f'https://api.themoviedb.org/3/movie/{movie_id}'
      response = requests.get(url, headers=headers)
      movie = response.json()

      # GET THE MOVIE CAST
      cast = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US'
      cast_response = requests.get(cast, headers=headers)
      movie_cast = cast_response.json()
      
      # GET THE MOVIE CREW
      crew = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US'
      crew_response = requests.get(crew, headers=headers)
      movie_crew = crew_response.json()


      return render_template("moreinfo.html", movie=movie, cast=movie_cast["cast"],crew=movie_crew["crew"])

# get hidden gems based on movies with low popularity and a rich number of votes
@app.route("/hidden-gems", methods=["GET"])
def get_gems():
      url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.asc&vote_average.gte=7&vote_count.gte=50"

      response = requests.get(url, headers=headers)
      gem_movies_with_genre = get_movies_with_genre(response)

      gems = [
        movie for movie in gem_movies_with_genre
        if movie.get('popularity', 0) <= 50
      ]

      return render_template("hiddengems.html", gems=gems)

# add a movie to the database via http request
@app.route("/watch-list", methods=["POST"])
def add_movie():
    data = request.json
    movie_id = data.get('movie_id')
    # Check if movie already exists
    existing_movie = WatchList.query.filter_by(movie_id=movie_id).first()
    if existing_movie:
        return jsonify({"message": "Movie already in your watchlist!"})
    
    # fetch details of the movie cause the DB doesnt have them :p
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    response = requests.get(url, headers=headers)

    movie_data = response.json()
    
    # Add new movie to the database
    movie = WatchList(
         movie_id=movie_id, 
         title=movie_data.get('title', ''),
         backdrop_path=movie_data.get('backdrop_path', '')
      )
    db.session.add(movie)
    db.session.commit()
    
    return jsonify({"message": "Movie added to your watchlist!"})

# remove the movie from the database
@app.route("/watch-list/<int:id>", methods=["DELETE"])
def remove_movie(id):
    # Look up by database ID, not movie_id (TMDB id)
    movie = WatchList.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie removed from your watchlist!"})
     
# what actually displays the WatchList to the user
@app.route("/watch-list", methods=["GET"])
def view_watchlist():
    movies = WatchList.query.order_by(WatchList.timestamp.desc()).all()
    return render_template("watchlist.html", movies=movies)
