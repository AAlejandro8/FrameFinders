from datetime import datetime
from app import db

class WatchList(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      movie_id = db.Column(db.Integer, unique=True, nullable=False)  # TMDB ID
      title = db.Column(db.String(200), nullable=False)
      backdrop_path = db.Column(db.String(200))
      timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
      
      def __repr__(self):
            return f"Movie: {self.title} was added at: {self.timestamp}"