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
