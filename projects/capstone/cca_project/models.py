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
    release_year = db.Column(db.Integer)
    runtimne = db.Column(db.Integer)
    director = db.Column(db.String())
    description = db.Column(db.String(500))
    genre = db.Column(db.String())
    rating = db.Column(db.Float())
    actors = db.Column(db.String())
    shows = db.relationship('Show', backref='Movies', lazy=True)

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
    date_of_birth = db.Column(db.DateTime, nullable=False)
    shows = db.relationship('Show', backref='Actors', lazy=True)

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