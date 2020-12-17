# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import os
import json
import dateutil.parser
import babel
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from flask_moment import Moment
from flask_migrate import Migrate
from datetime import date
from models import setup_db, Movies, Actors, Film
from auth import AuthError, requires_auth
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
    @requires_auth('post:movies')
    def add_movie():

        try:
            body = request.get_json()
            title = body['title']
            release_date = body['release_date']
            actors = body['actors']
            movie = Movies(title=title, release_date=release_date, actors=actors)
            movie.insert()

            return jsonify({
                'success': True,
                'created': movie.id,
                'total_movies': len(Movies.query.all())
            })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie_id):

        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        actors = body.get('actors', None)
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        
        if movie is None:
            abort(404)

        try:
            movie.title = title
            movie.release_date = release_date
            movie.actors = actors
            movie.update()

            return jsonify({
                'success': True,
                'updated': movie.id,
                'total_movies': len(Movies.query.all())
            })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_drink(movie_id):

        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                'success': True,
                'delete': movie_id
            }), 200

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
    @requires_auth('post:actors')
    def add_actor():
        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            actor = Actors(name=name, age=age, gender=gender)
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

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
