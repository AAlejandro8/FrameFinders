from datetime import datetime
from app import db

class WatchList(db.model):
      id = db.Column(db.Integer, primary_key=True)
      movie_id = db.Column(db.Integer, unique=True, nullable=False)  # TMDB ID
      title = db.Column(db.String(200), nullable=False)
      added_at = db.Column(db.DateTime, default=db.func.current_timestamp())