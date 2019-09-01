# servies/users/project/tests

import json
import unittest
from project import db
from project.api.models import User
from project.tests.utils import add_user, add_admin
from project.tests.base import BaseTestCase

# REFACTOR MUCH OF TEST CODE

class TestUserService(BaseTestCase):
# refactor tests if needed - include helper fucntion for asserts and success/fail status codes
    def test_main_no_users(self):
        """ensure main route behaves correctly when no users added to db"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """ show users when main route if users added """
        add_user('tom', 'tom@yahoo.com', 'password')
        add_user('jon', 'jon@yahoo.com', 'password')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'tom', response.data)
            self.assertIn(b'jon', response.data)

    def test_main_add_user(self):
        """ check add user to db via post request"""
        add_user('test', 'test@test.com', 'password')
        with self.client:
            response = self.client.post(
                '/',
                data={
                    'username': 'tom',
                    'email': 'tom@yahoo.com',
                    'password': 'password',
                },
                follow_redirects=True
                #content_type='application/json',
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data) # why check if this included?
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'tom', response.data)

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object
        does not have a password key.
        """
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'tom',
                    'email': 'tom@yahoo.com'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_users(self):
        """ensure ping route behaves correctly"""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves accordingly"""
        user = add_user("tom", "tom@yahoo.com", "password")
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('tom', data['data']['username'])
            self.assertIn('tom@yahoo.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """ensure error if user has no id"""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data['message'])
            self.assertIn("fail", data['status'])

    def test_single_user_wrong_id(self):
        """ensure error when id not found"""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist", data['message'])
            self.assertIn("fail", data['status'])

    def test_all_users(self):
        """ensure get all users behaves correctly"""
        add_user('tom', 'tom@yahoo.com', 'password')
        add_user('jon', 'jon@yahoo.com', 'password1')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('tom', data['data']['users'][0]['username'])
            self.assertTrue(data['data']['users'][0]['active'])
            self.assertFalse(data['data']['users'][0]['admin'])
            self.assertIn('jon@yahoo.com', data['data']['users'][1]['email'])
            self.assertTrue(data['data']['users'][0]['active'])
            self.assertFalse(data['data']['users'][0]['admin'])
            self.assertIn('success', data['status'])

    def test_add_user(self):
        """ test if a user can be added to db """
        add_user('test', 'test@test.com', 'test')
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'test@test.com',
                'password': 'test'
                }),
            content_type='application/json'
            )
        token = json.loads(resp_login.data.decode())['auth_token']
        response = self.client.post(
            '/users',
            data=json.dumps({
                'username': 'tom',
                'email': 'tom@yahoo.com',
                'password': 'password'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('tom@yahoo.com was added!', data['message'])
        self.assertIn('success', data['status'])


    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
# make sure all messages match returned for test
    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'tom@yahoo.com',
                    'password': 'password',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """ensure error thrown if email already exists"""
        add_user('test', 'test@test.com', 'test')
        #response = auth_user_restful()
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'tom',
                    'email': 'tom@yahoo.com',
                    'password': 'password',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            token_two = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'tom',
                    'email': 'tom@yahoo.com',
                    'password': 'password',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token_two}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry, that email already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_inactive(self):
        add_user('test', 'test@test.com', 'test')
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'tom',
                    'email': 'tom@yahoo.com',
                    'password': 'password'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_add_user_not_admin(self):
        #add_admin('test', 'test@test.com', 'test')
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test',
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            resp = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'tom',
                    'email': 'tom@yahoo.com',
                    'password': 'password'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data=json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'You do not have permission to do that.')
            self.assertEqual(resp.status_code, 401)


if __name__ == '__main__':
    unittest.main()
