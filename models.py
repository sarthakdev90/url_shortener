from api import db

class Click(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ip = db.Column(db.String(32))
    device = db.Column(db.String(100))
    os = db.Column(db.String(50))
    url_key = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime)

db.create_all()
