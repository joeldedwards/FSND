import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
import json

database_name = "moviesdb"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Movies(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    release_date = db.Column(db.Integer)
    actors = db.relationship('Film', backref='Movies', lazy=True)

    def __repr__(self):
        return f'<Movies {self.id} {self.title}>'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Actors(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer)
    gender = db.Column(db.String())
    films = db.relationship('Film', backref='Actors', lazy=True)

    def __repr__(self):
        return f'<Actors {self.id} {self.name}>'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Film(db.Model):
    __tablename__ = 'Film'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey(Actor.id), nullable=False)

    def __repr__(self):
        return f'<Film {self.id}>'