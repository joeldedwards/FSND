# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import os
import json
import dateutil.parser
import babel
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_moment import Moment
from flask_migrate import Migrate
from datetime import date
from models import setup_db, Movies, Actors, Show
import sys

MOVIES_PER_PAGE = 10
ACTORS_PER_PAGE = 10

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    moment = Moment(app)
    app.config.from_object('config')
    migrate = Migrate(app, setup_db)
    now = datetime.utcnow()
    setup_db(app)
    CORS(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type,Authorization,true'
          )
        response.headers.add(
          'Access-Control-Allow-Methods',
          'GET,PUT,POST,DELETE,OPTIONS'
          )
        return response

    def get_movie_list():
        movies = {}
        for movies in Movies.query.all():
            movies[movies.id] = movies.type
        return movies

    @app.route('/movies')
    def get_movies():
        movies = Movies.query.order_by(Movies.id).all()

        return jsonify({
          'success': True,
          'movies': get_movie_list(),
          'total_movies': len(Movies.query.all())
        })

    @app.route('/add', methods=['POST'])
    def add_movie():
        body = request.get_json()

        title = body.get('title', None)
        release_year = body.get('release_year', None)
        runtimne = body.get('runtimne', None)
        director = body.get('director', None)
        description = body.get('description', None)
        genre = body.get('genre', None)
        rating = body.get('rating', None)
        actors = body.get('actors', None)

        try:
            movie = Movies(title=title, release_year=release_year, runtimne=runtimne, director=director, description=description, genre=genre, rating=rating, actors=actors)
            movie.insert()

            return jsonify({
                'success': True,
                'created': movie.id,
                'total_movies': len(Movies.query.all())
            })

        except:
            abort(422)

    @app.route('/actors')
    def get_actors():
        actors = Actors.query.order_by(Actors.id).all()

        return jsonify({
          'success': True,
          'total_actors': len(Actors.query.all())
        })

    @app.route('/add', methods=['POST'])
    def add_actor():
        body = request.get_json()

        name = body.get('name', None)
        date_of_birth = body.get('date_of_birth', None)

        try:
            actor = Actors(name=name, date_of_birth=date_of_birth)
            actor.insert()

            return jsonify({
                'success': True,
                'created': actor.id,
                'total_actors': len(Movies.query.all())
            })

        except:
            abort(422)

     # ERROR HANDLERS
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
            }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
            }), 500

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
