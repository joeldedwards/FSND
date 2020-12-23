
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "movies"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
            'release_date': '2000-05-05'
        }
        
        res = self.client().post('/add', json=movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_questions(self):
        res = self.client().delete('/questions/24')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 24).one_or_none()
        
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 24)
        
    def test_fail_delete_questions(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_search_questions(self):
        res = self.client().post('/questions/search', json={"searchTerm":"play"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_quiz(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [], 
            "quiz_category": {
                "id": "1", 
                "type": "Science"
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['question'])

    def test_fail_quiz(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [], 
            "quiz_category": {
                "id": "10", "type": "Science"
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()