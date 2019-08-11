# users/project/api/users.py
# use blueprints self contained components for encapsulating code and assets
from flask import Blueprint, request, render_template, jsonify
from flask_restful import Resource, Api
from sqlalchemy import exc
from project import db
from project.api.models import User

users_blueprint = Blueprint('users', __name__, template_folder='./templates')
api = Api(users_blueprint)


# get user
class Users(Resource):
    def get(self, user_id):
        """gets single user"""
        response_obj = {
            'status': 'fail',
            'message': 'User does not exist'
        }
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return response_obj, 404
            else:
                response_obj = {
                    'status': 'success',
                    'data': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'active': user.active
                    }
                }
                return response_obj, 200
        except ValueError:
            return response_obj, 404

# add usersList route handler
class UsersList(Resource):

    def get(self):
        """get all users"""
        response_obj = {
            'status': 'success',
            'data': {
                'users': [user.to_json() for user in User.query.all()]
            }
        }
        return response_obj, 200

    def post(self):
        """ post a user """
        post_data = request.get_json()
        response_obj = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        if not post_data:
            return response_obj, 400

        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password') # replace
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                db.session.add(User(username=username, email=email, password=password))
                db.session.commit()
                response_obj['status'] = 'success'
                response_obj['message'] = f'{email} was added!'
                return response_obj, 201
            else:
                response_obj['message'] = 'Sorry, that email already exists'
                return response_obj, 400
        except (exc.IntegrityError):
            db.session.rollback()
            return jsonify(response_obj), 400
        except (exc.IntegrityError, ValueError):
            db.session.rollback()
            return response_obj, 400

class UsersPing(Resource):
    def get(self):
        return {
        "status": 'success',
        'message': 'pong!'
        }
# add route to blueprint
# route handler for index, get
@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db.session.add(User(username=username, email=email, password=password))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)

# routes
api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<user_id>')
api.add_resource(UsersPing, '/users/ping')
