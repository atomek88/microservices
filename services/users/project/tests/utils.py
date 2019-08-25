# utility functions here
import json
import unittest
from project import db
from project.api.models import User
from flask import request

def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def add_admin(username, email, password):
    add_user(username, email, password)
    user = User.query.filter_by(email=email).first()
    user.admin = True
    db.session.commit()
    return user

'''
def auth_user_restful(self):
    resp_login = self.client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'test@test.com',
            'password': 'test'
            }),
        content_type='application/json'
        )
    this.token = json.loads(resp_login.data.decode())['auth_token']
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
    return response
'''
