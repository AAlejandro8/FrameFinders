from app import app, db
from app.models import WatchList

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'WatchList': WatchList}