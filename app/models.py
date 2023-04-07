from app import app
from app import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(500))
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class MainMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return 'MainMenu {}>'.format(self.title)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    text = db.Column(db.String(500), index=True)
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return 'Posts {}>'.format(self.title)


with app.app_context():
    db.create_all()
