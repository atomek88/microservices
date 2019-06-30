# servies/users/project/tests

import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User

# helper fucntion for user testing
def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
# refactor tests if needed - include helper fucntion for asserts and success/fail status codes
    def test_users(self):
        """ensure ping route behaves correctly"""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves accordingly"""
        user = add_user("tom", "tom@yahoo.com")
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
        add_user('tom', 'tom@yahoo.com')
        add_user('jon', 'jon@yahoo.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('tom', data['data']['users'][0]['username'])
            self.assertIn('jon@yahoo.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_add_user(self):
        """ test if a user can be added to db """
        with self.client:
            response = self.client.post(
            '/users',
            data=json.dumps({
                'username': 'tom',
                'email': 'tom@yahoo.com'
            }),
            content_type='application/json',
        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('tom@yahoo.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """ ensure error thrown in json obj is empty"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
        )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])
# make sure all messages match returned for test
    def test_add_user_invalid_json_keys(self):
        """ ensure error thrown if wrong keys in json"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'tom@yahoo.com'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """ensure error thrown if email already exists"""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'tom',
                    'email': 'tom@yahoo.com'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'tom',
                    'email': 'tom@yahoo.com'
            }),
            content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry, that email already exists", data['message'])
            self.assertIn("fail", data['status'])

if __name__ == '__main__':
    unittest.main()
