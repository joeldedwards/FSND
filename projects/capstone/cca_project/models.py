import os
from sqlalchemy import Column, String, Integer, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_name = "movies"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()
migrate = Migrate()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Movies(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Integer, nullable=False)
    stars = db.relationship('Actors', backref='Movies', lazy=True)

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

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
            }

class Actors(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(String, nullable=False)
    films = db.relationship('Movies', backref='Actors', lazy=True)

    def __repr__(self):
        return f'<Actors {self.id}>'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'age': self.age,
            'gender': self.gender
            }
