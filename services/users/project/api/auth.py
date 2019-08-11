# auth.py

from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from project.api.models import User
from project import db, bcrypt

auth_blueprint = Blueprint('auth', __name__)


# routes for auth
@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    post_data = request.get_json()
    response_obj = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_obj), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email == email)).first()
        if not user:
            # add new user to db
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_obj['status'] = 'success'
            response_obj['message'] = 'Successfully registered.'
            response_obj['auth_token'] = auth_token.decode()
            return jsonify(response_obj), 201
        else:
            response_obj['message'] = 'Sorry. That user already exists.'
            return jsonify(response_obj), 400
    # handler errors
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return jsonify(response_obj), 400

# login route
@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    post_data = request.get_json()
    response_obj = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_obj), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_obj['status'] = 'success'
                response_obj['message'] = "Successfully logged in."
                response_obj['auth_token'] = auth_token.decode()
                return jsonify(response_obj), 200
        else:
            response_obj['message'] = "User does not exist."
            return jsonify(response_obj), 404
    except Exception:
        response_obj['message'] = 'Try again.'
        return jsonify(response_obj), 500

@auth_blueprint.route('/auth/logout', methods=['GET'])
def logout_user():
    # get auth token
    auth_header = request.headers.get("Authorization")
    response = {
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    }
    if auth_header:
        auth_token = auth_header.split(' ')[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            response['status'] = 'success'
            response['message'] = 'Successfully logged out.'
            return jsonify(response), 200
        else:
            response['message'] = resp
            return jsonify(response), 401
    else:
        return jsonify(response), 403

# status
@auth_blueprint.route('/auth/status', methods=['GET'])
def get_user_status():
    #get auth token
    auth_header = request.headers.get('Authorization')
    response_obj = {
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    }
    if auth_header:
        auth_token = auth_header.split(' ')[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user= User.query.filter_by(id=resp).first()
            response_obj['status'] = 'success'
            response_obj['message'] = 'Success.'
            response_obj['data'] = user.to_json()
            return jsonify(response_obj), 200
        response_obj['message'] = resp
        return jsonify(response_obj), 401
    else:
        return jsonify(response_obj), 401
