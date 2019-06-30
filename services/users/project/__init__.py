# services/users/project/init.py
import os
import sys
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()

def create_app(script_info=None):
    app = Flask(__name__)
    # set config from config.py
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
# set up extensions to db
    db.init_app(app)
    # register blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # shell context for flask cli to register app,db to shell
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
