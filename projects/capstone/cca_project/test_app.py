
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors


class CapstoneCastingTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "movies_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.assistant_token = os.environ.get('casting_assistant_token')
        self.director_token = os.environ.get('casting_director_token')
        self.executive_token = os.environ.get('executive_director_token')

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])

    def test_add_movie(self):
        movie = {
            'title': 'Gladiator',
            'release_year': '2000'
        }
        
        res = self.client().post('/add', json=movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_movies(self):
        res = self.client().delete('/movies/3')
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 1).one_or_none()
        
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        
    def test_fail_delete_movies(self):
        res = self.client().delete('/movies/10000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])

    def test_add_actor(self):
        actor = {
            'firstname': 'Dwayne',
            'lastname': 'Johnson',
            'age': 48,
            'gender': 'Male'
        }
        
        res = self.client().post('/add', json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_actors(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 1).one_or_none()
        
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        
    def test_fail_delete_actors(self):
        res = self.client().delete('/actors/10000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

if __name__ == "__main__":
    unittest.main()