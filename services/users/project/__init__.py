# services/users/project/init.py
import os
import sys
from flask import Flask, jsonify
# from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
# add debug toolbar from flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# init db
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
cors = CORS()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(script_info=None):
    app = Flask(__name__)
    # set config from config.py
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

# set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # register blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)
    from project.api.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # shell context for flask cli to register app,db to shell
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
