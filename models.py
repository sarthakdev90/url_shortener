from flask.ext.sqlalchemy import SQLAlchemy
from config import app

db = SQLAlchemy(app)

class Click(db.Model):
    key = db.Column(db.String(32), unique = True)
    timestamp = db.Column(db.DateTime)
