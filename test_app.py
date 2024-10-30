import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db, Actor, Movie
from settings import ASSISTANT_TOKEN, DIRECTOR_TOKEN, DATABASE_PATH_TEST


assistant_token = ASSISTANT_TOKEN
director_token = DIRECTOR_TOKEN
database_path = DATABASE_PATH_TEST


class MainTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_home_page(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    # Actors
    def test_get_actors(self):
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().get('/actors', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
    def test_post_actor(self):
        new_actor = {
            'name': 'Timothée Chalamet',
            'age': 24,
            'gender': 'M',
            'movie_id': 1
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().post('/actors', json=new_actor, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_missing_post_actor_info(self):
        new_actor = {
            'name': 'TEST',
            'age': '',
            'gender': 'M',
            'movie_id': 1
        }
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().post('/actors', json=new_actor, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_actor(self):
        edit_actor = {
            'name': '',
            'age': 88,
            'gender': '',
            'movie_id': ''
        }
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().patch('/actors/3', json=edit_actor,
                                  headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_patch_actor_not_found(self):
        edit_actor = {
            'name': '',
            'age': 88,
            'gender': '',
            'movie_id': ''
        }
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().patch('/actors/1000', json=edit_actor,
                                  headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_401_unauth_get_actors(self):
        res = self.client().get('/actors', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_delete_actor(self):
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().delete('/actors/20', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 20)

    def test_404_delete_actor_not_found(self):
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().delete('/actors/100000', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Movies
    def test_get_movies(self):
        auth = {
            'Authorization': "Bearer {}".format(assistant_token)
        }
        res = self.client().get('/movies', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_post_movie(self):
        new_movie = {
            'title': 'Call Me by Your Name',
            'release_date': '2017-10-20'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().post('/movies', json=new_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_missing_post_movie_info(self):
        new_movie = {
            'title': '',
            'release_date': '2017-01-01'
        }
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().post('/movies', json=new_movie, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_movie(self):
        edit_movie = {
            'title': '',
            'release_date': '2020-11-01'
        }
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().patch('/movies/3', json=edit_movie,
                                  headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_patch_movie_not_found(self):
        edit_movie = {
            'title': 'testing',
            'release_date': '2020-11-01'
        }
        auth = {
            'Authorization': "Bearer {}".format(director_token) 
        }
        res = self.client().patch('/movies/100', json=edit_movie, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_401_unauth_get_movies(self):
        res = self.client().get('/movies', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_delete_movie(self):
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().delete('/movies/16', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 16)

    def test_404_delete_movie_not_found(self):
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().delete('/movies/100', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
