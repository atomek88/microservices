import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user

from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('testuser', 'test@test.com')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        user = add_user('testuser','test@test.com')
        dup_user = User(username='testuser',email='test@test2.com',)
        db.session.add(dup_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = add_user('testuser','test@test.com')

        dup_user = User(
            username='testuser1',
            email='test@test.com',
        )
        db.session.add(dup_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('justatest','test@test.com')
        self.assertTrue(isinstance(user.to_json(), dict))

if __name__ == '__main__':
    unittest.main()
